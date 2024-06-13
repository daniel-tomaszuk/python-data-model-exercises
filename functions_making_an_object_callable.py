from concurrent.futures import ProcessPoolExecutor


class Adder:
    def __init__(self, add_number: int | float):
        self.number = add_number

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} number={self.number}> @ {id(self)}"

    def __call__(self, second_number, *args, **kwargs) -> int | float:
        # also helps if there is a `can not be pickled` error
        print(f"called: {second_number} {args} {kwargs}")
        return self.number + second_number


if __name__ == "__main__":
    add_one = Adder(1)
    add_three = Adder(3)
    numbers = list(range(1, 6))

    print(add_one(2))
    print(add_three(2))
    print(Adder(5)(10))

    with ProcessPoolExecutor() as pool:
        results = pool.map(add_one, numbers)
        print(list(results))

        results = pool.map(add_three, numbers)
        print(list(results))
