"""
Basic arithmetic operations for SmartCalc Pro.
"""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Division by zero is undefined. Please enter a non-zero divisor.")
    return a / b
