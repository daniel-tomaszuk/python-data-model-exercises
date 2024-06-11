from uuid import uuid4


class Car:
    __slots__ = ("color", "year", "uuid")  # only these attributes are allowed, removes class __dict__ attribute!

    def __init__(self, color: str, year: int):
        self.color = color
        self.year = year
        self.uuid = str(uuid4())

    def __repr__(self) -> str:
        return f"<Car color={self.color}, year={self.color}> @ {id(self)}"

    def __eq__(self, other: "Car") -> bool:
        # When it's implemented, then Car object is no longer hashable by default and can not be used as a dict key,
        # __hash__ method is required
        return (
            self.color == other.color
            and self.year == self.year
            and self.__class__ == other.__class__
            and self.uuid == other.uuid
        )

    def __hash__(self) -> int:
        # Pro Tip: make sure that if two objects are equal, their hashes are equal!
        return hash((self.color, self.year, self.uuid))


if __name__ == "__main__":
    c1 = Car("red", 1997)
    c2 = Car("blue", 2001)
    c3 = Car("red", 1997)
    print(c1, c2, c3)
    print(c1 == c3)

    car_reviews = {
        c1: "awsome",
        c2: "meh",
        c3: "ok",
    }
    print("Reviews: ", car_reviews)
    print(car_reviews[c1])

    c1.color = "yellow"  # state mutated, changes the hash and dict key!
    print(car_reviews[c1])  # throws an KeyError
