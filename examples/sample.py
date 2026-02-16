def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def calculate_sum(numbers):
    total = 0
    for num in numbers:
        if num > 0:
            total += num
    return total


def check_status(value):
    if value > 100:
        return "High"
    elif value > 50:
        return "Medium"
    else:
        return "Low"


class Calculator:
    def __init__(self, initial):
        self.value = initial

    def add(self, x):
        self.value += x
        return self.value

    def multiply(self, x):
        self.value *= x
        return self.value
