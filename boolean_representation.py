

class Pair:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<Pair(x={self.x}, y={self.y})> @ {id(self)}"

    def __bool__(self) -> bool:
        if not self.x and not self.y:
            return False
        return True


if __name__ == "__main__":
    p1 = Pair(0, 0)
    p2 = Pair(1, 3)

    print(p1)
    print(p2)

    print(bool(p1))
    print(bool(p2))

