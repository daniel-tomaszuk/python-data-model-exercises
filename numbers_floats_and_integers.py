

class Point:
    def __init__(self, x: int | float = 1, y: int | float = 1):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}> @ {id(self)}"

    def __int__(self) -> int:
        return int(self.x + self.y)

    def __float__(self) -> float:
        return float(self.x + self.y)


if __name__ == "__main__":
    p1 = Point(-4, 3)
    p2 = Point(5.25, 2.33)
    p3 = Point(-3, -4)

    print(int(p1))
    print(float(p2))
