"""
Comprehensive unit tests for operation classes.
"""

import pytest
from app.operation.operations import (
    Addition, Subtraction, Multiplication, Division,
    OPERATIONS, Operation
)


class TestOperationInterface:
    """Test the operation interface and abstract base class."""
    
    def test_operation_is_abstract(self):
        """Test that Operation class cannot be instantiated."""
        with pytest.raises(TypeError):
            Operation()


class TestAddition:
    """Comprehensive tests for Addition operation."""
    
    def test_addition_symbol(self, addition_operation):
        """Test addition symbol."""
        assert addition_operation.symbol == "+"
    
    @pytest.mark.parametrize("operand_a,operand_b,expected", [
        (5, 3, 8),
        (0, 0, 0),
        (-5, 3, -2),
        (5, -3, 2),
        (-5, -3, -8),
        (3.5, 2.1, 5.6),
        (0.1, 0.2, 0.3),
        (1000000, 2000000, 3000000),
        (-1.5, 2.7, 1.2),
    ])
    def test_addition_compute(self, addition_operation, operand_a, operand_b, expected):
        """Test addition computation with various inputs."""
        result = addition_operation.compute(operand_a, operand_b)
        assert abs(result - expected) < 1e-10  # Handle floating point precision
    
    def test_addition_compute_large_numbers(self, addition_operation):
        """Test addition with very large numbers."""
        result = addition_operation.compute(1e15, 1e15)
        assert result == 2e15
    
    def test_addition_compute_small_numbers(self, addition_operation):
        """Test addition with very small numbers."""
        result = addition_operation.compute(1e-15, 1e-15)
        assert result == 2e-15


class TestSubtraction:
    """Comprehensive tests for Subtraction operation."""
    
    def test_subtraction_symbol(self, subtraction_operation):
        """Test subtraction symbol."""
        assert subtraction_operation.symbol == "-"
    
    @pytest.mark.parametrize("operand_a,operand_b,expected", [
        (5, 3, 2),
        (0, 0, 0),
        (-5, 3, -8),
        (5, -3, 8),
        (-5, -3, -2),
        (3.5, 2.1, 1.4),
        (0.3, 0.1, 0.2),
        (1000000, 500000, 500000),
        (-1.5, -2.7, 1.2),
    ])
    def test_subtraction_compute(self, subtraction_operation, operand_a, operand_b, expected):
        """Test subtraction computation with various inputs."""
        result = subtraction_operation.compute(operand_a, operand_b)
        assert abs(result - expected) < 1e-10  # Handle floating point precision


class TestMultiplication:
    """Comprehensive tests for Multiplication operation."""
    
    def test_multiplication_symbol(self, multiplication_operation):
        """Test multiplication symbol."""
        assert multiplication_operation.symbol == "*"
    
    @pytest.mark.parametrize("operand_a,operand_b,expected", [
        (5, 3, 15),
        (0, 5, 0),
        (5, 0, 0),
        (-5, 3, -15),
        (5, -3, -15),
        (-5, -3, 15),
        (3.5, 2, 7.0),
        (0.5, 0.4, 0.2),
        (100, 0.01, 1.0),
        (1.5, 2.5, 3.75),
    ])
    def test_multiplication_compute(self, multiplication_operation, operand_a, operand_b, expected):
        """Test multiplication computation with various inputs."""
        result = multiplication_operation.compute(operand_a, operand_b)
        assert abs(result - expected) < 1e-10  # Handle floating point precision
    
    def test_multiplication_identity(self, multiplication_operation):
        """Test multiplication by identity (1)."""
        assert multiplication_operation.compute(42, 1) == 42
        assert multiplication_operation.compute(1, 42) == 42


class TestDivision:
    """Comprehensive tests for Division operation."""
    
    def test_division_symbol(self, division_operation):
        """Test division symbol."""
        assert division_operation.symbol == "/"
    
    @pytest.mark.parametrize("operand_a,operand_b,expected", [
        (6, 3, 2),
        (5, 2, 2.5),
        (-6, 3, -2),
        (6, -3, -2),
        (-6, -3, 2),
        (3.6, 1.2, 3.0),
        (1, 4, 0.25),
        (7, 2, 3.5),
        (100, 25, 4),
    ])
    def test_division_compute(self, division_operation, operand_a, operand_b, expected):
        """Test division computation with various inputs."""
        result = division_operation.compute(operand_a, operand_b)
        assert abs(result - expected) < 1e-10  # Handle floating point precision
    
    def test_division_by_zero(self, division_operation):
        """Test division by zero raises appropriate error."""
        with pytest.raises(ZeroDivisionError) as exc_info:
            division_operation.compute(5, 0)
        assert "Cannot divide by zero" in str(exc_info.value)
    
    def test_division_zero_dividend(self, division_operation):
        """Test division of zero."""
        result = division_operation.compute(0, 5)
        assert result == 0
    
    def test_division_identity(self, division_operation):
        """Test division by identity (1)."""
        assert division_operation.compute(42, 1) == 42


class TestOperationsRegistry:
    """Test the operations registry functionality."""
    
    def test_operations_registry_contains_all_operations(self):
        """Test that all operations are in the registry."""
        assert '+' in OPERATIONS
        assert '-' in OPERATIONS
        assert '*' in OPERATIONS
        assert '/' in OPERATIONS
    
    def test_operations_registry_aliases(self):
        """Test that operation aliases work correctly."""
        # Addition aliases
        assert isinstance(OPERATIONS['add'], Addition)
        assert isinstance(OPERATIONS['addition'], Addition)
        
        # Subtraction aliases
        assert isinstance(OPERATIONS['sub'], Subtraction)
        assert isinstance(OPERATIONS['subtract'], Subtraction)
        assert isinstance(OPERATIONS['subtraction'], Subtraction)
        
        # Multiplication aliases
        assert isinstance(OPERATIONS['mul'], Multiplication)
        assert isinstance(OPERATIONS['multiply'], Multiplication)
        assert isinstance(OPERATIONS['multiplication'], Multiplication)
        
        # Division aliases
        assert isinstance(OPERATIONS['div'], Division)
        assert isinstance(OPERATIONS['divide'], Division)
        assert isinstance(OPERATIONS['division'], Division)
    
    def test_operations_registry_instances(self):
        """Test that registry contains correct operation instances."""
        assert isinstance(OPERATIONS['+'], Addition)
        assert isinstance(OPERATIONS['-'], Subtraction)
        assert isinstance(OPERATIONS['*'], Multiplication)
        assert isinstance(OPERATIONS['/'], Division)
    
    def test_operations_registry_consistency(self):
        """Test that same operations return same instances."""
        assert OPERATIONS['+'] is OPERATIONS['add']
        assert OPERATIONS['-'] is OPERATIONS['sub']
        assert OPERATIONS['*'] is OPERATIONS['mul']
        assert OPERATIONS['/'] is OPERATIONS['div']