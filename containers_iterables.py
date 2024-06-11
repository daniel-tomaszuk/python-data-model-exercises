

class Taco:

    def __init__(self, shell: str, toppings: list[str] | None):
        self.shell = shell
        self.toppings = toppings or []
        self.index = -1

    def __iter__(self):
        # should return an iterable that has __next__ method implemented
        return (t for t in self.toppings)

    def __len__(self) -> int:
        return len(self.toppings)

    def __reversed__(self):
        # should return reversed iterable
        # for i in range(len(self) - 1, -1, -1):
        #     yield self.toppings[i]
        return self.toppings[::-1]

    # def __next__(self):
    #     self.index += 1
    #     if self.index >= len(self.toppings):
    #         self.index = -1
    #         raise StopIteration()
    #     return self.toppings[self.index]


if __name__ == "__main__":
    taco = Taco("soft", toppings=["cheese", "olives", "tomatoes"])

    for t in taco:
        print(t)

    print(len(taco))

    for t in reversed(taco):
        print(t)

    iterator = iter(taco)
    print(next(iterator))
    print(next(iterator))
