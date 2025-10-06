"""
Base operation class and specific arithmetic operation implementations.
"""

from abc import ABC, abstractmethod


class Operation(ABC):
    """
    Abstract base class for all arithmetic operations.
    
    This class defines the interface that all operations must implement,
    following the Template Method and Strategy patterns.
    """
    
    @property
    @abstractmethod
    def symbol(self) -> str:
        """
        The mathematical symbol for this operation.
        
        Returns:
            str: The operation symbol
        """
        pass  # pragma: no cover
    
    @abstractmethod
    def compute(self, operand_a: float, operand_b: float) -> float:
        """
        Perform the arithmetic operation.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            
        Returns:
            float: The result of the operation
            
        Raises:
            ArithmeticError: If the operation cannot be performed
        """
        pass  # pragma: no cover


class Addition(Operation):
    """Addition operation implementation."""
    
    @property
    def symbol(self) -> str:
        """Return the addition symbol."""
        return "+"
    
    def compute(self, operand_a: float, operand_b: float) -> float:
        """
        Perform addition.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            
        Returns:
            float: The sum of the operands
        """
        return operand_a + operand_b


class Subtraction(Operation):
    """Subtraction operation implementation."""
    
    @property
    def symbol(self) -> str:
        """Return the subtraction symbol."""
        return "-"
    
    def compute(self, operand_a: float, operand_b: float) -> float:
        """
        Perform subtraction.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            
        Returns:
            float: The difference of the operands
        """
        return operand_a - operand_b


class Multiplication(Operation):
    """Multiplication operation implementation."""
    
    @property
    def symbol(self) -> str:
        """Return the multiplication symbol."""
        return "*"
    
    def compute(self, operand_a: float, operand_b: float) -> float:
        """
        Perform multiplication.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            
        Returns:
            float: The product of the operands
        """
        return operand_a * operand_b


class Division(Operation):
    """Division operation implementation."""
    
    @property
    def symbol(self) -> str:
        """Return the division symbol."""
        return "/"
    
    def compute(self, operand_a: float, operand_b: float) -> float:
        """
        Perform division.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            
        Returns:
            float: The quotient of the operands
            
        Raises:
            ZeroDivisionError: If attempting to divide by zero
        """
        # Using EAFP (Easier to Ask Forgiveness than Permission) paradigm
        try:
            return operand_a / operand_b
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero")


# Create singleton instances for each operation
_addition = Addition()
_subtraction = Subtraction()
_multiplication = Multiplication()
_division = Division()

# Operation registry for easy access
OPERATIONS = {
    '+': _addition,
    'add': _addition,
    'addition': _addition,
    '-': _subtraction,
    'sub': _subtraction,
    'subtract': _subtraction,
    'subtraction': _subtraction,
    '*': _multiplication,
    'mul': _multiplication,
    'multiply': _multiplication,
    'multiplication': _multiplication,
    '/': _division,
    'div': _division,
    'divide': _division,
    'division': _division,
}