"""
Calculation module containing the Calculation class and CalculationFactory.
"""

from typing import Any


class Calculation:
    """
    Represents a single calculation with operands, operation, and result.
    
    This class encapsulates the data and behavior for a mathematical calculation,
    implementing object-oriented principles for clean code organization.
    """
    
    def __init__(self, operand_a: float, operand_b: float, operation: Any, result: float = None):
        """
        Initialize a calculation instance.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            operation: The operation object that performs the calculation
            result (float, optional): The result of the calculation
        """
        self.operand_a = operand_a
        self.operand_b = operand_b
        self.operation = operation
        self._result = result
    
    @property
    def result(self) -> float:
        """
        Get the result of the calculation.
        
        Returns:
            float: The calculation result
        """
        if self._result is None:
            self._result = self.operation.compute(self.operand_a, self.operand_b)
        return self._result
    
    def __str__(self) -> str:
        """
        String representation of the calculation.
        
        Returns:
            str: Human-readable representation of the calculation
        """
        return f"{self.operand_a} {self.operation.symbol} {self.operand_b} = {self.result}"
    
    def __repr__(self) -> str:
        """
        Detailed string representation for debugging.
        
        Returns:
            str: Detailed representation of the calculation
        """
        return (f"Calculation(operand_a={self.operand_a}, operand_b={self.operand_b}, "
                f"operation={self.operation.__class__.__name__}, result={self._result})")


class CalculationFactory:
    """
    Factory class for creating Calculation instances.
    
    This class implements the Factory design pattern to create calculations
    based on operation type and operands, promoting loose coupling and
    extensibility.
    """
    
    @staticmethod
    def create_calculation(operand_a: float, operand_b: float, operation: Any) -> Calculation:
        """
        Create a new calculation instance.
        
        Args:
            operand_a (float): The first operand
            operand_b (float): The second operand
            operation: The operation object
            
        Returns:
            Calculation: A new calculation instance
            
        Raises:
            ValueError: If operands are invalid
            TypeError: If operation is invalid
        """
        # Input validation using LBYL (Look Before You Leap) paradigm
        if not isinstance(operand_a, (int, float)):
            raise TypeError(f"First operand must be a number, got {type(operand_a).__name__}")
        
        if not isinstance(operand_b, (int, float)):
            raise TypeError(f"Second operand must be a number, got {type(operand_b).__name__}")
        
        if not hasattr(operation, 'compute'):
            raise TypeError("Operation must have a 'compute' method")
        
        if not hasattr(operation, 'symbol'):
            raise TypeError("Operation must have a 'symbol' attribute")
        
        return Calculation(float(operand_a), float(operand_b), operation)