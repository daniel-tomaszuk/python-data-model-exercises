import contextlib
from datetime import datetime


class Date(datetime):

    def __pos__(self):
        return self.timestamp()

    def __neg__(self):
        return -self.timestamp()


class FloatString(str):

    def __pos__(self):
        with contextlib.suppress(ValueError):
            return float(self)
        return self

    def __neg__(self):
        with contextlib.suppress(ValueError):
            return -float(self)
        return self


class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __pos__(self) -> "Point":
        # `+` - positive operator
        return self

    def __neg__(self) -> "Point":
        # `-` - negative operator
        return Point(-self.x, -self.y)


if __name__ == "__main__":
    p1 = Point(-4, 3)
    p2 = Point(5, 2)
    p3 = Point(-3, -4)

    print(p1)
    print(-p1)

    d = Date.now()
    print(+d)
    print(-d)

    f1 = FloatString("abcd")
    print(+f1)
    print(-f1)

    f2 = FloatString("3.14")
    print(+f2)
    print(-f2)
