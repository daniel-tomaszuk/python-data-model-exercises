from typing import Union


class Point:
    def __init__(self, x: int = 1, y: int = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __mul__(self, other: "Point") -> "Point":
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)

        if isinstance(other, int):
            return Point(self.x * other, self.y * other)

        return Point()

    def __rmul__(self, other: Union[int, "Point"]) -> "Point":
        # handle right side of the multiplication
        return self.__mul__(other)

    def __imul__(self, other: Union[int, "Point"]) -> "Point":
        # In place multiplication, if not defined will use regular __mul__
        if isinstance(other, Point):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int):
            self.x *= other
            self.y *= other
        return self


if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(5, 2)
    p3 = Point(-3, -4)

    print(p1 * p2)
    print(p2 * p3)
    print(p3 * p2)

    print(p1 * 2)
    print(5 * p1)
    print(p1 * 2.5)  # returns default Point(0, 0)
    print(p1 * "abc")  # returns default Point(0, 0)

    p1 *= p2
    print("P1: ", p1)

    p2 *= 5
    print("P2: ", p2)
