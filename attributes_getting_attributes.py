

class Pair:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} x={self.x} y={self.y}"

    def __getattr__(self, item: str):
        # fallback for __getattribute__
        print(f"__getattr__: {item}")
        if item == "z":
            return self.x + self.y
        return AttributeError(f"__getattr__ - No such attribute: {item}")

    def __getattribute__(self, item: str):
        # Is called for every attribute!
        print(f"__getattribute__: {item}")
        if item == "z":
            return self.x + self.y
        return super().__getattribute__(item)

    def __dir__(self) -> list[str]:
        dir: list[str] = [key for key in self.__dict__]
        return dir + ["z"]


if __name__ == "__main__":
    pair = Pair(3, 7)
    print(pair.x, pair.y,  pair.z)
    print(pair.a)

    print(pair)
    print(pair.__dict__)

    pair.b = 100
    print(pair.b)

    print("\n---")
    getattr(pair, "x")
    getattr(pair, "a")

    print(dir(pair))
    print(pair.z)
