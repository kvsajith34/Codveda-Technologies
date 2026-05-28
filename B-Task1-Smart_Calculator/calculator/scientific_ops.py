"""
Scientific operations for SmartCalc Pro.
All trig functions accept degrees as input.
"""

import math


def square_root(n: float) -> float:
    if n < 0:
        raise ValueError("Square root of a negative number is undefined in real numbers.")
    return math.sqrt(n)


def power(base: float, exp: float) -> float:
    return base ** exp


def percentage(part: float, total: float) -> float:
    if total == 0:
        raise ZeroDivisionError("Total/base cannot be zero when calculating percentage.")
    return (part / total) * 100


def log_base(n: float, base: float = 10) -> float:
    if n <= 0:
        raise ValueError("Logarithm is undefined for non-positive values.")
    if base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive and not equal to 1.")
    return math.log(n, base)


def natural_log(n: float) -> float:
    if n <= 0:
        raise ValueError("Natural log is undefined for non-positive values.")
    return math.log(n)


def sine(degrees: float) -> float:
    return math.sin(math.radians(degrees))


def cosine(degrees: float) -> float:
    return math.cos(math.radians(degrees))


def tangent(degrees: float) -> float:
    # Undefined at 90, 270, etc.
    if (degrees % 180) == 90:
        raise ValueError("Tangent is undefined at 90° and 270°.")
    return math.tan(math.radians(degrees))


def factorial(n: float) -> int:
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")
    if n != int(n):
        raise ValueError("Factorial is only defined for whole numbers.")
    if n > 170:
        raise ValueError("Input too large for factorial (max 170).")
    return math.factorial(int(n))
