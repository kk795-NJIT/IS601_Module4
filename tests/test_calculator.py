"""
Comprehensive unit tests for calculator module.
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from app.calculator.calculator import (
    Calculator, CalculationHistory, InputValidator
)
from app.calculation.calculation import Calculation
from app.operation.operations import Addition, Division


class TestCalculationHistory:
    """Comprehensive tests for CalculationHistory class."""
    
    def test_history_initialization(self):
        """Test history initialization."""
        history = CalculationHistory()
        assert len(history) == 0
        assert not bool(history)
        assert history.get_history() == []
        assert history.get_last_calculation() is None
    
    def test_add_calculation(self):
        """Test adding calculations to history."""
        history = CalculationHistory()
        operation = Addition()
        calc = Calculation(5.0, 3.0, operation)
        
        history.add_calculation(calc)
        assert len(history) == 1
        assert bool(history)
        assert history.get_last_calculation() is calc
    
    def test_add_multiple_calculations(self):
        """Test adding multiple calculations."""
        history = CalculationHistory()
        operation = Addition()
        
        calc1 = Calculation(5.0, 3.0, operation)
        calc2 = Calculation(10.0, 2.0, operation)
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        assert len(history) == 2
        assert history.get_last_calculation() is calc2
        
        history_list = history.get_history()
        assert len(history_list) == 2
        assert history_list[0] is calc1
        assert history_list[1] is calc2
    
    def test_add_invalid_calculation(self):
        """Test adding invalid calculation type."""
        history = CalculationHistory()
        with pytest.raises(TypeError) as exc_info:
            history.add_calculation("not_a_calculation")
        assert "Must provide a Calculation instance" in str(exc_info.value)
    
    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy."""
        history = CalculationHistory()
        operation = Addition()
        calc = Calculation(5.0, 3.0, operation)
        
        history.add_calculation(calc)
        history_copy = history.get_history()
        
        # Modifying the copy should not affect original
        history_copy.clear()
        assert len(history) == 1
        assert len(history.get_history()) == 1
    
    def test_clear_history(self):
        """Test clearing history."""
        history = CalculationHistory()
        operation = Addition()
        calc = Calculation(5.0, 3.0, operation)
        
        history.add_calculation(calc)
        assert len(history) == 1
        
        history.clear_history()
        assert len(history) == 0
        assert not bool(history)
        assert history.get_last_calculation() is None


class TestInputValidator:
    """Comprehensive tests for InputValidator class."""
    
    @pytest.mark.parametrize("input_str,expected", [
        ("5", 5.0),
        ("3.14", 3.14),
        ("-5", -5.0),
        ("0", 0.0),
        ("  5.5  ", 5.5),  # Test with whitespace
        ("1e6", 1000000.0),
        ("1.5e-3", 0.0015),
    ])
    def test_validate_number_success(self, input_str, expected):
        """Test successful number validation."""
        result = InputValidator.validate_number(input_str)
        assert result == expected
    
    @pytest.mark.parametrize("invalid_input", [
        "not_a_number",
        "5.5.5",
        "abc",
        "",
        "5 + 3",
        "infinity",
    ])
    def test_validate_number_failure(self, invalid_input):
        """Test number validation failures."""
        with pytest.raises(ValueError) as exc_info:
            InputValidator.validate_number(invalid_input)
        assert f"'{invalid_input}' is not a valid number" in str(exc_info.value)
    
    @pytest.mark.parametrize("operation", [
        "+", "-", "*", "/",
        "add", "sub", "mul", "div",
        "addition", "subtraction", "multiplication", "division",
    ])
    def test_validate_operation_success(self, operation):
        """Test successful operation validation."""
        assert InputValidator.validate_operation(operation) is True
        # Test case insensitive
        assert InputValidator.validate_operation(operation.upper()) is True
        # Test with whitespace
        assert InputValidator.validate_operation(f"  {operation}  ") is True
    
    @pytest.mark.parametrize("invalid_operation", [
        "invalid", "++", "mod", "%", "^", "**"
    ])
    def test_validate_operation_failure(self, invalid_operation):
        """Test operation validation failures."""
        assert InputValidator.validate_operation(invalid_operation) is False
    
    @pytest.mark.parametrize("command", [
        "help", "history", "exit", "quit", "clear"
    ])
    def test_validate_command_success(self, command):
        """Test successful command validation."""
        assert InputValidator.validate_command(command) is True
        # Test case insensitive
        assert InputValidator.validate_command(command.upper()) is True
        # Test with whitespace
        assert InputValidator.validate_command(f"  {command}  ") is True
    
    @pytest.mark.parametrize("invalid_command", [
        "invalid", "run", "save", "load"
    ])
    def test_validate_command_failure(self, invalid_command):
        """Test command validation failures."""
        assert InputValidator.validate_command(invalid_command) is False


class TestCalculator:
    """Comprehensive tests for Calculator class."""
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        calc = Calculator()
        assert isinstance(calc.history, CalculationHistory)
        assert isinstance(calc.validator, InputValidator)
        assert calc.running is False
    
    def test_parse_input_success(self):
        """Test successful input parsing."""
        calc = Calculator()
        
        # Test basic operations
        result = calc._parse_input("5 + 3")
        assert result == (5.0, "+", 3.0)
        
        result = calc._parse_input("10.5 * 2")
        assert result == (10.5, "*", 2.0)
        
        result = calc._parse_input("7 div 2")
        assert result == (7.0, "div", 2.0)
    
    def test_parse_input_invalid_format(self):
        """Test input parsing with invalid format."""
        calc = Calculator()
        
        # Too few parts
        with pytest.raises(ValueError) as exc_info:
            calc._parse_input("5 +")
        assert "exactly three parts" in str(exc_info.value)
        
        # Too many parts
        with pytest.raises(ValueError) as exc_info:
            calc._parse_input("5 + 3 + 2")
        assert "exactly three parts" in str(exc_info.value)
    
    def test_parse_input_invalid_operands(self):
        """Test input parsing with invalid operands."""
        calc = Calculator()
        
        with pytest.raises(ValueError) as exc_info:
            calc._parse_input("abc + 3")
        assert "'abc' is not a valid number" in str(exc_info.value)
        
        with pytest.raises(ValueError) as exc_info:
            calc._parse_input("5 + def")
        assert "'def' is not a valid number" in str(exc_info.value)
    
    def test_parse_input_invalid_operation(self):
        """Test input parsing with invalid operation."""
        calc = Calculator()
        
        with pytest.raises(ValueError) as exc_info:
            calc._parse_input("5 % 3")
        assert "Unsupported operation: %" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)
    
    def test_perform_calculation_success(self):
        """Test successful calculation performance."""
        calc = Calculator()
        
        result = calc._perform_calculation(5.0, "+", 3.0)
        assert isinstance(result, Calculation)
        assert result.result == 8.0
    
    def test_perform_calculation_division_by_zero(self):
        """Test calculation with division by zero."""
        calc = Calculator()
        
        with patch('builtins.print') as mock_print:
            result = calc._perform_calculation(5.0, "/", 0.0)
            assert result is None
            mock_print.assert_called()
            call_args = str(mock_print.call_args)
            assert "Math error" in call_args
    
    def test_is_command(self):
        """Test command detection."""
        calc = Calculator()
        
        assert calc._is_command("help") is True
        assert calc._is_command("history") is True
        assert calc._is_command("exit") is True
        assert calc._is_command("5 + 3") is False
        assert calc._is_command("help me please") is True  # First word is command
    
    @patch('builtins.print')
    def test_handle_command_help(self, mock_print):
        """Test help command handling."""
        calc = Calculator()
        calc._handle_command("help")
        
        # Check that help was printed
        mock_print.assert_called()
        call_args_list = [str(call) for call in mock_print.call_args_list]
        combined_output = " ".join(call_args_list)
        assert "CALCULATOR HELP" in combined_output
    
    @patch('builtins.print')
    def test_handle_command_history_empty(self, mock_print):
        """Test history command with empty history."""
        calc = Calculator()
        calc._handle_command("history")
        
        mock_print.assert_called_with("No calculations in history.")
    
    @patch('builtins.print')
    def test_handle_command_history_with_calculations(self, mock_print):
        """Test history command with calculations."""
        calc = Calculator()
        operation = Addition()
        calc1 = Calculation(5.0, 3.0, operation)
        calc2 = Calculation(10.0, 2.0, operation)
        
        calc.history.add_calculation(calc1)
        calc.history.add_calculation(calc2)
        
        calc._handle_command("history")
        
        # Check that history was printed
        mock_print.assert_called()
        call_args_list = [str(call) for call in mock_print.call_args_list]
        combined_output = " ".join(call_args_list)
        assert "CALCULATION HISTORY" in combined_output
    
    @patch('builtins.print')
    def test_handle_command_clear(self, mock_print):
        """Test clear command handling."""
        calc = Calculator()
        operation = Addition()
        calc.history.add_calculation(Calculation(5.0, 3.0, operation))
        
        calc._handle_command("clear")
        
        assert len(calc.history) == 0
        mock_print.assert_called_with("Calculation history cleared.")
    
    def test_handle_command_exit(self):
        """Test exit command handling."""
        calc = Calculator()
        calc.running = True
        
        with patch('builtins.print') as mock_print:
            calc._handle_command("exit")
            
        assert calc.running is False
        mock_print.assert_called_with("Goodbye!")
    
    def test_handle_command_quit(self):
        """Test quit command handling."""
        calc = Calculator()
        calc.running = True
        
        with patch('builtins.print') as mock_print:
            calc._handle_command("quit")
            
        assert calc.running is False
        mock_print.assert_called_with("Goodbye!")
    
    @patch('builtins.print')
    def test_handle_calculation_input_success(self, mock_print):
        """Test successful calculation input handling."""
        calc = Calculator()
        
        calc._handle_calculation_input("5 + 3")
        
        assert len(calc.history) == 1
        assert calc.history.get_last_calculation().result == 8.0
        
        # Check that result was printed
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list[-1])
        assert "Result:" in call_args and "8.0" in call_args
    
    @patch('builtins.print')
    def test_handle_calculation_input_invalid_format(self, mock_print):
        """Test calculation input with invalid format."""
        calc = Calculator()
        
        calc._handle_calculation_input("5 +")
        
        assert len(calc.history) == 0
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        assert "Input error" in call_args
    
    @patch('builtins.print')
    def test_handle_calculation_input_division_by_zero(self, mock_print):
        """Test calculation input with division by zero."""
        calc = Calculator()
        
        calc._handle_calculation_input("5 / 0")
        
        assert len(calc.history) == 0
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        assert "Math error" in call_args
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_basic_calculation(self, mock_print, mock_input):
        """Test running calculator with basic calculation."""
        mock_input.side_effect = ["5 + 3", "exit"]
        
        calc = Calculator()
        calc.run()
        
        assert len(calc.history) == 1
        assert calc.history.get_last_calculation().result == 8.0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_help_command(self, mock_print, mock_input):
        """Test running calculator with help command."""
        mock_input.side_effect = ["help", "exit"]
        
        calc = Calculator()
        calc.run()
        
        # Check that help was displayed
        call_args_list = [str(call) for call in mock_print.call_args_list]
        combined_output = " ".join(call_args_list)
        assert "CALCULATOR HELP" in combined_output
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_empty_input(self, mock_print, mock_input):
        """Test running calculator with empty input."""
        mock_input.side_effect = ["", "   ", "exit"]
        
        calc = Calculator()
        calc.run()
        
        # Should handle empty input gracefully
        assert len(calc.history) == 0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_keyboard_interrupt(self, mock_print, mock_input):
        """Test running calculator with keyboard interrupt."""
        mock_input.side_effect = KeyboardInterrupt()
        
        calc = Calculator()
        calc.run()
        
        # Should handle keyboard interrupt gracefully
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        assert "Goodbye!" in call_args
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_eof_error(self, mock_print, mock_input):
        """Test running calculator with EOF error."""
        mock_input.side_effect = EOFError()
        
        calc = Calculator()
        calc.run()
        
        # Should handle EOF error gracefully
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        assert "Goodbye!" in call_args
    
    @patch('builtins.print')
    def test_display_welcome(self, mock_print):
        """Test welcome message display."""
        calc = Calculator()
        calc._display_welcome()
        
        mock_print.assert_called()
        call_args_list = [str(call) for call in mock_print.call_args_list]
        combined_output = " ".join(call_args_list)
        assert "Professional Calculator Application" in combined_output
        assert "Type 'help' for instructions" in combined_output