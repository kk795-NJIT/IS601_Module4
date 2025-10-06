"""
Comprehensive unit tests for calculation classes.
"""

import pytest
from app.calculation.calculation import Calculation, CalculationFactory
from app.operation.operations import Addition, Subtraction, Multiplication, Division


class TestCalculation:
    """Comprehensive tests for Calculation class."""
    
    def test_calculation_initialization(self, addition_operation):
        """Test calculation initialization."""
        calc = Calculation(5.0, 3.0, addition_operation)
        assert calc.operand_a == 5.0
        assert calc.operand_b == 3.0
        assert calc.operation is addition_operation
        assert calc._result is None
    
    def test_calculation_initialization_with_result(self, addition_operation):
        """Test calculation initialization with pre-computed result."""
        calc = Calculation(5.0, 3.0, addition_operation, 8.0)
        assert calc.operand_a == 5.0
        assert calc.operand_b == 3.0
        assert calc.operation is addition_operation
        assert calc._result == 8.0
    
    @pytest.mark.parametrize("operand_a,operand_b,operation_class,expected", [
        (5, 3, Addition, 8),
        (5, 3, Subtraction, 2),
        (5, 3, Multiplication, 15),
        (6, 3, Division, 2),
        (0, 5, Addition, 5),
        (0, 5, Multiplication, 0),
        (-5, 3, Addition, -2),
        (3.5, 2.1, Addition, 5.6),
        (10.5, 2.5, Subtraction, 8.0),
    ])
    def test_calculation_result_property(self, operand_a, operand_b, operation_class, expected):
        """Test calculation result property with various operations."""
        operation = operation_class()
        calc = Calculation(operand_a, operand_b, operation)
        result = calc.result
        assert abs(result - expected) < 1e-10  # Handle floating point precision
        # Test that result is cached
        assert calc._result == result
    
    def test_calculation_result_caching(self, addition_operation):
        """Test that calculation result is properly cached."""
        calc = Calculation(5.0, 3.0, addition_operation)
        
        # First access computes result
        result1 = calc.result
        assert calc._result == result1
        
        # Second access uses cached result
        result2 = calc.result
        assert result1 == result2
        assert calc._result == result2
    
    def test_calculation_str_representation(self, addition_operation):
        """Test string representation of calculation."""
        calc = Calculation(5.0, 3.0, addition_operation)
        expected = "5.0 + 3.0 = 8.0"
        assert str(calc) == expected
    
    def test_calculation_repr_representation(self, addition_operation):
        """Test detailed string representation of calculation."""
        calc = Calculation(5.0, 3.0, addition_operation)
        repr_str = repr(calc)
        assert "Calculation(" in repr_str
        assert "operand_a=5.0" in repr_str
        assert "operand_b=3.0" in repr_str
        assert "operation=Addition" in repr_str
        assert "result=None" in repr_str
    
    def test_calculation_repr_with_result(self, addition_operation):
        """Test repr with pre-computed result."""
        calc = Calculation(5.0, 3.0, addition_operation, 8.0)
        repr_str = repr(calc)
        assert "result=8.0" in repr_str
    
    def test_calculation_with_zero_division(self, division_operation):
        """Test calculation with division by zero."""
        calc = Calculation(5.0, 0.0, division_operation)
        with pytest.raises(ZeroDivisionError):
            _ = calc.result


class TestCalculationFactory:
    """Comprehensive tests for CalculationFactory class."""
    
    def test_factory_create_calculation_success(self, addition_operation):
        """Test successful calculation creation."""
        calc = CalculationFactory.create_calculation(5.0, 3.0, addition_operation)
        assert isinstance(calc, Calculation)
        assert calc.operand_a == 5.0
        assert calc.operand_b == 3.0
        assert calc.operation is addition_operation
    
    @pytest.mark.parametrize("operand_a,operand_b,operation_class", [
        (5, 3, Addition),
        (5.5, 3.2, Subtraction),
        (0, 1, Multiplication),
        (-5, -3, Division),
        (1e6, 1e-6, Addition),
    ])
    def test_factory_create_calculation_various_inputs(self, operand_a, operand_b, operation_class):
        """Test factory with various valid inputs."""
        operation = operation_class()
        calc = CalculationFactory.create_calculation(operand_a, operand_b, operation)
        assert isinstance(calc, Calculation)
        assert calc.operand_a == float(operand_a)
        assert calc.operand_b == float(operand_b)
        assert calc.operation is operation
    
    def test_factory_invalid_first_operand_type(self, addition_operation):
        """Test factory with invalid first operand type."""
        with pytest.raises(TypeError) as exc_info:
            CalculationFactory.create_calculation("invalid", 3.0, addition_operation)
        assert "First operand must be a number" in str(exc_info.value)
        assert "got str" in str(exc_info.value)
    
    def test_factory_invalid_second_operand_type(self, addition_operation):
        """Test factory with invalid second operand type."""
        with pytest.raises(TypeError) as exc_info:
            CalculationFactory.create_calculation(5.0, "invalid", addition_operation)
        assert "Second operand must be a number" in str(exc_info.value)
        assert "got str" in str(exc_info.value)
    
    def test_factory_invalid_operation_no_compute(self):
        """Test factory with operation missing compute method."""
        class InvalidOperation:
            symbol = "?"
        
        with pytest.raises(TypeError) as exc_info:
            CalculationFactory.create_calculation(5.0, 3.0, InvalidOperation())
        assert "Operation must have a 'compute' method" in str(exc_info.value)
    
    def test_factory_invalid_operation_no_symbol(self):
        """Test factory with operation missing symbol attribute."""
        class InvalidOperation:
            def compute(self, a, b):
                return a + b
        
        with pytest.raises(TypeError) as exc_info:
            CalculationFactory.create_calculation(5.0, 3.0, InvalidOperation())
        assert "Operation must have a 'symbol' attribute" in str(exc_info.value)
    
    def test_factory_operand_conversion(self, addition_operation):
        """Test that factory properly converts operands to float."""
        calc = CalculationFactory.create_calculation(5, 3, addition_operation)
        assert isinstance(calc.operand_a, float)
        assert isinstance(calc.operand_b, float)
        assert calc.operand_a == 5.0
        assert calc.operand_b == 3.0
    
    @pytest.mark.parametrize("invalid_operand", [
        None,
        [],
        {},
        "not_a_number",
        complex(1, 2),
    ])
    def test_factory_invalid_operand_types(self, addition_operation, invalid_operand):
        """Test factory with various invalid operand types."""
        with pytest.raises(TypeError):
            CalculationFactory.create_calculation(invalid_operand, 3.0, addition_operation)
        
        with pytest.raises(TypeError):
            CalculationFactory.create_calculation(5.0, invalid_operand, addition_operation)
    
    def test_factory_static_method(self):
        """Test that create_calculation is a static method."""
        # Should be able to call without instantiating factory
        operation = Addition()
        calc = CalculationFactory.create_calculation(5.0, 3.0, operation)
        assert isinstance(calc, Calculation)