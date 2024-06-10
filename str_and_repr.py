

class Taco:

    def __init__(self, shell: str, protein: str, toppings: list | None = None):
        self.shell = shell
        self.protein = protein
        self.toppings = toppings

    def __repr__(self) -> str:
        # Formal representation of an instance, fallbacks to default object memory location if not defined
        return (
            f"<{self.__class__.__name__} "
            f"toppings={self.toppings} "
            f"protein={self.protein} "
            f"shell={self.shell} @ {id(self)}>"
        )

    def __str__(self) -> str:
        # Informal representation of an instance, fallbacks to __repr__ if not defined
        toppings: str = (f"with {", ".join(self.toppings)}" if self.toppings else "")
        return f"{self.shell} shell {self.protein} taco {toppings} @ {id(self)}"


if __name__ == "__main__":
    t1 = Taco("hard", protein="chicken")
    t2 = Taco("soft", protein="tofu", toppings=["cheese", "lettuce", "sour cream"])

    print(t1)
    print(t2)

    print(repr(t1))
    print(repr(t2))
