"""
Calculator module containing the main Calculator class with history management.
"""

from typing import List, Optional, Tuple
import sys
from app.calculation.calculation import Calculation, CalculationFactory
from app.operation.operations import OPERATIONS


class CalculationHistory:
    """
    Manages the history of calculations performed during the session.
    
    This class provides functionality to store, retrieve, and manage
    calculation history with proper encapsulation.
    """
    
    def __init__(self):
        """Initialize an empty calculation history."""
        self._history: List[Calculation] = []
    
    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to the history.
        
        Args:
            calculation (Calculation): The calculation to add
        """
        if not isinstance(calculation, Calculation):
            raise TypeError("Must provide a Calculation instance")
        self._history.append(calculation)
    
    def get_history(self) -> List[Calculation]:
        """
        Get a copy of the calculation history.
        
        Returns:
            List[Calculation]: Copy of the calculation history
        """
        return self._history.copy()
    
    def get_last_calculation(self) -> Optional[Calculation]:
        """
        Get the most recent calculation.
        
        Returns:
            Optional[Calculation]: The last calculation or None if history is empty
        """
        return self._history[-1] if self._history else None
    
    def clear_history(self) -> None:
        """Clear all calculations from history."""
        self._history.clear()
    
    def __len__(self) -> int:
        """Return the number of calculations in history."""
        return len(self._history)
    
    def __bool__(self) -> bool:
        """Return True if history contains calculations."""
        return bool(self._history)


class InputValidator:
    """
    Handles validation of user inputs.
    
    This class provides static methods for validating different types
    of user input using both LBYL and EAFP paradigms.
    """
    
    @staticmethod
    def validate_number(value: str) -> float:
        """
        Validate and convert a string to a number.
        
        Args:
            value (str): The string to validate
            
        Returns:
            float: The converted number
            
        Raises:
            ValueError: If the value cannot be converted to a number
        """
        # Using EAFP (Easier to Ask Forgiveness than Permission) paradigm
        try:
            result = float(value.strip())
            # Check for special float values that we want to reject
            if result == float('inf') or result == float('-inf') or result != result:  # NaN check
                raise ValueError(f"'{value}' is not a valid number")
            return result
        except ValueError:
            raise ValueError(f"'{value}' is not a valid number")
    
    @staticmethod
    def validate_operation(operation: str) -> bool:
        """
        Validate if an operation is supported.
        
        Args:
            operation (str): The operation to validate
            
        Returns:
            bool: True if operation is valid
        """
        # Using LBYL (Look Before You Leap) paradigm
        return operation.lower().strip() in OPERATIONS
    
    @staticmethod
    def validate_command(command: str) -> bool:
        """
        Validate if a command is a special command.
        
        Args:
            command (str): The command to validate
            
        Returns:
            bool: True if command is valid
        """
        valid_commands = {'help', 'history', 'exit', 'quit', 'clear'}
        return command.lower().strip() in valid_commands


class Calculator:
    """
    Main calculator class implementing REPL interface.
    
    This class provides the main interface for the calculator application,
    handling user interaction, calculation execution, and history management.
    """
    
    def __init__(self):
        """Initialize the calculator with empty history."""
        self.history = CalculationHistory()
        self.validator = InputValidator()
        self.running = False
    
    def run(self) -> None:
        """
        Start the calculator REPL (Read-Eval-Print Loop).
        
        This method implements the main loop for user interaction,
        handling commands and calculations until the user exits.
        """
        self.running = True
        self._display_welcome()
        
        while self.running:
            try:
                user_input = input("\nCalculator> ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle special commands
                if self._is_command(user_input):
                    self._handle_command(user_input.lower())
                    continue
                
                # Parse and execute calculation
                self._handle_calculation_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break
            except Exception as e:  # pragma: no cover
                print(f"Unexpected error: {e}")
                print("Please try again or type 'help' for assistance.")
    
    def _display_welcome(self) -> None:
        """Display welcome message and basic instructions."""
        print("=" * 50)
        print("   Professional Calculator Application")
        print("=" * 50)
        print("Type 'help' for instructions, 'exit' to quit")
        print("Supported operations: +, -, *, /")
        print("Example: 5 + 3 or add 5 3")
    
    def _is_command(self, user_input: str) -> bool:
        """
        Check if user input is a special command.
        
        Args:
            user_input (str): The user input to check
            
        Returns:
            bool: True if input is a command
        """
        return self.validator.validate_command(user_input.split()[0])
    
    def _handle_command(self, command: str) -> None:
        """
        Handle special commands.
        
        Args:
            command (str): The command to handle
        """
        if command in ['exit', 'quit']:
            print("Goodbye!")
            self.running = False
        elif command == 'help':
            self._display_help()
        elif command == 'history':
            self._display_history()
        elif command == 'clear':
            self._clear_history()
    
    def _display_help(self) -> None:
        """Display help information."""
        print("\n" + "=" * 40)
        print("CALCULATOR HELP")
        print("=" * 40)
        print("Usage:")
        print("  <number> <operation> <number>")
        print("  Example: 5 + 3, 10.5 * 2")
        print("\nSupported Operations:")
        print("  Addition: +, add")
        print("  Subtraction: -, sub, subtract")
        print("  Multiplication: *, mul, multiply")
        print("  Division: /, div, divide")
        print("\nSpecial Commands:")
        print("  help     - Show this help message")
        print("  history  - Show calculation history")
        print("  clear    - Clear calculation history")
        print("  exit     - Exit the calculator")
        print("=" * 40)
    
    def _display_history(self) -> None:
        """Display calculation history."""
        if not self.history:
            print("No calculations in history.")
            return
        
        print("\n" + "=" * 30)
        print("CALCULATION HISTORY")
        print("=" * 30)
        for i, calc in enumerate(self.history.get_history(), 1):
            print(f"{i:2d}. {calc}")
        print("=" * 30)
    
    def _clear_history(self) -> None:
        """Clear calculation history."""
        self.history.clear_history()
        print("Calculation history cleared.")
    
    def _handle_calculation_input(self, user_input: str) -> None:
        """
        Parse and execute a calculation from user input.
        
        Args:
            user_input (str): The user input to parse
        """
        try:
            operand_a, operation_str, operand_b = self._parse_input(user_input)
            calculation = self._perform_calculation(operand_a, operation_str, operand_b)
            
            if calculation:
                self.history.add_calculation(calculation)
                print(f"Result: {calculation}")
                
        except ValueError as e:
            print(f"Input error: {e}")
            print("Please use format: <number> <operation> <number>")
            print("Example: 5 + 3")
        except Exception as e:  # pragma: no cover
            print(f"Error: {e}")
    
    def _parse_input(self, user_input: str) -> Tuple[float, str, float]:
        """
        Parse user input into operands and operation.
        
        Args:
            user_input (str): The input to parse
            
        Returns:
            Tuple[float, str, float]: The parsed operands and operation
            
        Raises:
            ValueError: If input format is invalid
        """
        parts = user_input.split()
        
        if len(parts) != 3:
            raise ValueError("Please provide exactly three parts: number operation number")
        
        operand_a_str, operation_str, operand_b_str = parts
        
        # Validate operands
        operand_a = self.validator.validate_number(operand_a_str)
        operand_b = self.validator.validate_number(operand_b_str)
        
        # Validate operation
        if not self.validator.validate_operation(operation_str):
            available_ops = list(set(OPERATIONS.keys()))
            raise ValueError(f"Unsupported operation: {operation_str}. "
                           f"Available: {', '.join(sorted(available_ops))}")
        
        return operand_a, operation_str.lower(), operand_b
    
    def _perform_calculation(self, operand_a: float, operation_str: str, operand_b: float) -> Optional[Calculation]:
        """
        Perform a calculation using the factory pattern.
        
        Args:
            operand_a (float): First operand
            operation_str (str): Operation string
            operand_b (float): Second operand
            
        Returns:
            Optional[Calculation]: The calculation result or None if error
        """
        try:
            operation = OPERATIONS[operation_str]
            calculation = CalculationFactory.create_calculation(operand_a, operand_b, operation)
            # Test the calculation to catch any computation errors
            _ = calculation.result
            return calculation
        except ZeroDivisionError as e:
            print(f"Math error: {e}")
            return None
        except Exception as e:  # pragma: no cover
            print(f"Calculation error: {e}")
            return None


def main():  # pragma: no cover
    """Main entry point for the calculator application."""
    calculator = Calculator()
    calculator.run()


if __name__ == "__main__":  # pragma: no cover
    main()