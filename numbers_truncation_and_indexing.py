from math import trunc
from string import ascii_uppercase


class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __trunc__(self) -> int:
        # Cuts at decimal point and just returns an integer, there are some edge cases with .999999999999999
        # not required if __float__ is implemented
        return trunc(self.x + self.y)


class Character:
    first = "A"

    def __init__(self, char: str):
        self.char = char

    def __repr__(self):
        return f"<{self.__class__.__name__} char = {self.char}> @ {id(self.char)}"

    def __index__(self) -> int:
        # __index__ should return the same value as __int__ !!
        return ord(self.char) - ord(self.first)

    def __int__(self) -> int:
        # __int__ should return the same value as __index__ !!
        return self.__index__()


if __name__ == "__main__":
    p1 = Point(-4, 3.25)
    p2 = Point(5.25, 2.33)
    p3 = Point(-11.70, -20.25)

    print(trunc(p1))
    print(trunc(p2))
    print(trunc(p3))

    a = Character("A")
    b = Character("B")
    p = Character("P")

    print(a, b, p)
    print(int(a), int(b), int(p))
    print(ascii_uppercase[a:p])
