from typing import Union


class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    @staticmethod
    def __validate(value: Union[int, "Point"]) -> None:
        if isinstance(value, Point) and (value.x == 0 or value.y == 0):
            raise ValueError("Can not divide by 0")

        if isinstance(value, int) and value == 0:
            raise ValueError("Can not divide by 0")

    def __truediv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(other)

        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)

        if isinstance(other, int):
            return Point(self.x / other, self.y / other)

        return Point()

    def __rtruediv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(self)

        if isinstance(other, Point):
            return Point(other.x / self.x, other.y / self.y)

        if isinstance(other, int):
            return Point(other / self.x, other / self.y)

        return Point()

    def __itruediv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(other)

        if isinstance(other, Point):
            self.x /= other.x
            self.y /= other.y

        if isinstance(other, int):
            self.x /= other
            self.y /= other

        return self

    def __floordiv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(other)

        if isinstance(other, Point):
            return Point(self.x // other.x, self.y // other.y)

        if isinstance(other, int):
            return Point(self.x // other, self.y // other)

        return Point()

    def __rfloordiv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(self)

        if isinstance(other, Point):
            return Point(other.x // self.x, other.y // self.y)

        if isinstance(other, int):
            return Point(other // self.x, other // self.y)

        return Point()

    def __ifloordiv__(self, other: Union[int, "Point"]) -> "Point":
        self.__validate(other)

        if isinstance(other, Point):
            self.x //= other.x
            self.y //= other.y

        if isinstance(other, int):
            self.x //= other
            self.y //= other

        return self

    def __divmod__(self, other: Union[int, "Point"]) -> "Point":
        # used by `divmod` function
        return self


if __name__ == "__main__":
    p1 = Point(1, 1)
    p2 = Point(5, 2)
    p3 = Point(-3, -4)

    print(p1 / p2)
    print(p2 / p3)
    print(p3 / p2)

    print(p1 / 2)
    print(5 / p1)
    print(p1 / 2.5)  # returns default Point(0, 0)
    print(p1 / "abc")  # returns default Point(0, 0)

    print(p1 // p2)
    print(p2 // p3)
    print(p3 // p2)

    print(p1 // 2)
    print(5 // p1)
    print(p1 // 2.5)  # returns default Point(0, 0)
    print(p1 // "abc")  # returns default Point(0, 0)

    p1 /= p2
    print("P1: ", p1)

    p2 /= 5
    print("P2: ", p2)

    p1 //= p2
    print("P1: ", p1)

    p2 //= 5
    print("P2: ", p2)
