# test_math_service.py

from services.math_service import compute_factorial, compute_power, compute_fibonacci

def test_compute_factorial():
    assert compute_factorial(0) == 1
    assert compute_factorial(1) == 1
    assert compute_factorial(5) == 120

def test_compute_power():
    assert compute_power(2, 3) == 8
    assert compute_power(5, 0) == 1
    assert compute_power(9, 0.5) == 3

def test_compute_fibonacci():
    assert compute_fibonacci(0) == 0
    assert compute_fibonacci(1) == 1
    assert compute_fibonacci(7) == 13
