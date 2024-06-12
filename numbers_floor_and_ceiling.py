from math import ceil, floor


class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __floor__(self) -> int:
        # not required if __float__ is implemented
        return floor((self.x ** 2 + self.y ** 2) ** 0.5)

    def __ceil__(self) -> int:
        # not required if __float__ is implemented
        return ceil((self.x ** 2 + self.y ** 2) ** 0.5)


if __name__ == "__main__":
    p1 = Point(-4, 3.25)
    p2 = Point(5.25, 2.33)
    p3 = Point(-11, -20)

    print(floor(p1))
    print(ceil(p2))
    print(floor(p3))
    print(ceil(p3))
