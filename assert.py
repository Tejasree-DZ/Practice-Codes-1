class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value):
        self.value = value


def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


assert add(2, 3) == 5, "Test failed: 2 + 3 should be 5"
assert add(-1, 1) == 0, "Test failed: -1 + 1 should be 0"
assert add(0, 0) == 0, "Test failed: 0 + 0 should be 0"

assert divide(10, 2) == 5, "Test failed: 10 / 2 should be 5"
try:
    divide(5, 0)
    assert False, "Test failed: division by zero should raise ValueError"
except ValueError:
    pass

obj1 = Singleton(100)
obj2 = Singleton(200)

assert obj1 is obj2, "Test failed: obj1 and obj2 should be the same instance"
assert obj2.value == 200, "Test failed: value should reflect last __init__ call"

print("All test cases passed successfully!")