

class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __invert__(self) -> "Point":
        return Point(-self.x, -self.y)


class Fraction:

    def __init__(self, numerator: int, denumerator: int):
        self.num = numerator
        self.denom = denumerator

    def __invert__(self) -> "Fraction":
        return Fraction(self.denom, self.num)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.num} / {self.denom}> @ {id(self)}"


if __name__ == "__main__":
    p1 = Point(-4, 3)
    p2 = Point(5, 2)
    p3 = Point(-3, -4)

    print(abs(p1))
    print(abs(p2))
    print(abs(p3))

    print(~p1)
    print(~~p1)
    print(~p2)
    print(~p3)

    f1 = Fraction(3, 4)
    f2 = Fraction(4, 10)

    print(~f1)
    print(~f2)
