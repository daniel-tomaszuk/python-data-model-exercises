

class Car:
    ALLOWED_COLORS = ("red", "blue", "green")

    def __init__(self, color: str):
        self._color = color

    def __repr__(self):
        return f"<{self.__class__.__name__} color={self.color}> @ {id(self)}"

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        if value not in self.ALLOWED_COLORS:
            raise AttributeError(f"Color {value} not allowed!")
        self._color = value

    @color.deleter
    def color(self):
        # self._color = "unpainted"
        raise AttributeError("Deletion not allowed!")


if __name__ == "__main__":
    c1 = Car(color="red")
    print(c1)

    c1.color = "blue"
    print(c1)

    c2 = Car(color="blue")
    c2.ALLOWED_COLORS = ("black", )

    print(c2.ALLOWED_COLORS)
    print(c1.ALLOWED_COLORS)

    # throws an error!
    try:
        c1.color = "white"
    except Exception as e:
        print(e)

    # throws an error
    try:
        del c1.color
        print(c1)
    except Exception as e:
        print(e)
