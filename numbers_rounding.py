

class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __round__(self, n: int = 2):
        return round((self.x ** 2 + self.y ** 2) ** 0.5, ndigits=n)


if __name__ == "__main__":
    p1 = Point(-4, 3.25)
    p2 = Point(5.25, 2.33)
    p3 = Point(-11, -20)

    print(round(p1))
    print(round(p2))
    print(round(p1, 5))
    print(round(p2, 3))
    print(round(p3, 10))
    print(round(p3, 0))

    print(round(p3, -1))
    print(round(p3, -2))
