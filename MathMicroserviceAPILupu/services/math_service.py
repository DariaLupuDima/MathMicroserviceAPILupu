# services/math_service.py

def compute_factorial(n: int) -> int:
    """Compute the factorial of a non-negative integer n."""
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def compute_power(a: float, b: float) -> float:
    """Compute a raised to the power of b."""
    return a ** b

def compute_fibonacci(n: int) -> int:
    """Compute the n-th Fibonacci number (0-indexed)."""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
