

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
        return f"{self.shell} shell {self.protein} taco {toppings}"

    def __format__(self, format_spec: str) -> str:
        print("Format spec:", format_spec)

        if format_spec.endswith("d"):
            return str(id(self))

        # custom formatting string
        if format_spec.endswith("taco"):
            return self.__repr__().upper() + "!!!!"

        return super().__format__(format_spec)

    def __bytes__(self) -> bytes:
        message = "".join(hex(ord(c)) for c in self.__str__())
        return message.encode()


if __name__ == "__main__":
    t1 = Taco("hard", protein="chicken")
    t2 = Taco("soft", protein="tofu", toppings=["cheese", "lettuce", "sour cream"])

    print(t1)
    print(t2)

    print(repr(t1))
    print(repr(t2))

    # format doesn't call t1.__format__  if it knows how to format the class on its own
    print("Format as string:", "{!s}".format(t1))
    print("Format as repr:", "{!r}".format(t1))

    # t1.__format__  is called here, default formatting isn't  known so instance method is called
    print("{}".format(t1))

    # some additional formatting with format strings
    print("{:02d}".format(t1))
    print("{:taco}".format(t1))  # not really a good idea, but will work as long as Taco class supports it

    # check out __bytes__
    print("bytes:", bytes(t1))
