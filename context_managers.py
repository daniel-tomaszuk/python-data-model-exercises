

class Car:
    def __init__(self):
        self.running = False
        self.odometer = 0
        self.direction_degrees = 90

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"running={self.running} "
            f"odometer={self.odometer} "
            f"direction={self.direction_degrees} degrees> @ {id(self)}"
        )

    def move(self, amount):
        if self.running:
            self.odometer += amount

    def _turn(self, amount):
        if self.running:
            self.direction_degrees += amount

    def __enter__(self):
        self.running = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False

    def turn_right(self):
        self._turn(90)

    def turn_left(self):
        self._turn(-90)

    def turn_around(self):
        self._turn(180)


if __name__ == "__main__":
    car = Car()
    print(car)

    car.running = True
    car.move(10)
    car.turn_right()
    car.move(5)
    car.turn_left()
    print(car)

    car.running = False
    print(car)

    print("\n--- With context manager ---")
    car2 = Car()
    print(car2)
    with car2:
        print(car2)
        car2.move(10)
        car2.turn_right()
        car2.move(5)
        car2.turn_left()
        print(car2)
    print(car2)
