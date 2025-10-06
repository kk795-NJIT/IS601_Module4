#!/usr/bin/env python3
"""
Main entry point for the calculator application.
"""

from app.calculator.calculator import Calculator

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()