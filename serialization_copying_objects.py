from copy import copy, deepcopy


class Taco:

    def __init__(self, protein: str, toppings: list[str] | None = None):
        self.protein = protein
        self.cheese = None
        self.toppings = toppings

    def __repr__(self) -> str:
        return (f"<{self.__class__.__name__} "
                f"protein={self.protein} "
                f"cheese={self.cheese} "
                f"toppings={self.toppings}"
                f"> @ {id(self)}")

    def __copy__(self) -> "Taco":
        new_taco = Taco(self.protein)
        new_taco.cheese = "cheddar"

        new_taco.toppings = self.toppings  # BEWARE!! Makes a list reference, not a new list!
        return new_taco

    def __deepcopy__(self, memodict={}):
        new_taco = Taco(self.protein, toppings=deepcopy(self.toppings))
        new_taco.cheese = "deep fried cheese"
        return new_taco


if __name__ == "__main__":
    t1 = Taco("steak", toppings=["a", "b", "c"])
    t2 = copy(t1)  # calls __copy__
    t1.protein = "tofu"
    t1.toppings.append("d")  # also appended to t2
    print(t1)
    print(t2)

    t3 = deepcopy(t1)
    t1.toppings.append("x")  # not appended to t3, but still appended to t2
    print("----")
    print(t1)
    print(t2)
    print(t3)
