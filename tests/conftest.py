"""
Test configuration and fixtures for pytest.
"""

import pytest
from app.operation.operations import Addition, Subtraction, Multiplication, Division
from app.calculation.calculation import Calculation, CalculationFactory


@pytest.fixture
def addition_operation():
    """Fixture for addition operation."""
    return Addition()


@pytest.fixture
def subtraction_operation():
    """Fixture for subtraction operation."""
    return Subtraction()


@pytest.fixture
def multiplication_operation():
    """Fixture for multiplication operation."""
    return Multiplication()


@pytest.fixture
def division_operation():
    """Fixture for division operation."""
    return Division()


@pytest.fixture
def sample_calculation(addition_operation):
    """Fixture for a sample calculation."""
    return Calculation(5.0, 3.0, addition_operation)


@pytest.fixture
def calculation_factory():
    """Fixture for calculation factory."""
    return CalculationFactory()