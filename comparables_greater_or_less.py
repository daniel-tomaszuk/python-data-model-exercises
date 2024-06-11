from math import sqrt


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __normalize(self) -> float:
        # check distance from point (0, 0)
        return sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other: "Point") -> bool:
        for key, value in self.__dict__.items():
            if value != getattr(other, key):
                return False
        return True

    def __ne__(self, other: "Point") -> bool:
        # this is done like this by default in Python
        return not self.__eq__(other)

    def __gt__(self, other: "Point") -> bool:
        # greater than
        return self.__normalize() > other.__normalize()

    def __ge__(self, other: "Point") -> bool:
        # greater or equal
        return self.__normalize() >= other.__normalize()

    def __lt__(self, other: "Point") -> bool:
        # less than
        return self.__normalize() < other.__normalize()

    def __le__(self, other: "Point") -> bool:
        # less or equal
        return self.__normalize() <= other.__normalize()


if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(1, 2)
    p3 = Point(1, -4)

    print(p1 > p2)
    print(p1 >= p2)
    print(p1 < p2)
    print(p1 <= p2)

    print(p1 > p3)
    print(p1 >= p3)
    print(p3 > p1)
    print(p3 > p2)
