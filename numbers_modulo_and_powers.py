from typing import Union


class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __mod__(self, other: "Point") -> "Point":
        # operator `%` - return rest from truediv
        return Point(self.x % other.x, self.y % other.y)

    def __rmod__(self, other: "Point") -> "Point":
        print("<RMOD>")
        return self

    def __imod__(self, other: "Point") -> "Point":
        self.x %= other.x
        self.y %= other.y
        return self

    def __pow__(self, other: "Point", modulo=None) -> "Point":
        return Point(self.x ** other.x, self.y ** other.y)

    def __rpow__(self, other: "Point") -> "Point":
        print("<RPOW>")
        return self

    def __ipow__(self, other: "Point") -> "Point":
        self.x **= other.x
        self.y **= other.y
        return self


if __name__ == "__main__":
    p1 = Point(-4, 3)
    p2 = Point(5, 2)
    p3 = Point(-3, -4)

    print(p1 % p2)
    print(p2 % p3)
    print(p3 % p1)

    print(2 % p1)

    p1 %= p2
    print(p1)

    p3 %= p2
    print(p3)

    p1 = Point(5, 6)
    p2 = Point(3, 5)
    print(p1 ** p2)
    print(3 ** p3)

    p1 **= p2
    print(p1)
