import re


class Vin:
    """
    Descriptor example. Descriptor has to have __get__, __set__, __delete__
    """
    _validation_regex = re.compile("\\d{9}")

    def __init__(self, vin: str = "000000000"):
        self._vin = vin

    def __repr__(self):
        return f"<{self.__class__.__name__} vin={self._vin}> @ {id(self)}"

    def __get__(self, instance, owner) -> str:
        print(f"Vin: __get__ {instance} {owner}")
        return self._vin

    def __set__(self, instance, value):
        print(f"Vin: __set__ {instance} {value}")
        if not self._validation_regex.match(value):
            raise ValueError("Wrong VIN number!")

        self._vin = value

    def __delete__(self, instance):
        print(f"Vin: __delete__ {instance}")
        raise AttributeError("Vin can not be deleted!")


class Car:
    ALLOWED_COLORS = ("red", "blue", "green")
    vin = Vin()

    def __init__(self, color: str):
        self._color = color

    def __repr__(self):
        return f"<{self.__class__.__name__} color={self._color}> @ {id(self)}"


if __name__ == "__main__":
    c1 = Car(color="red")
    print(c1.vin)

    c1.vin = "123123123"
    print(c1.vin)

    try:
        del c1.vin
    except Exception as e:
        print(e)

    try:
        c1.vin = "fake vin number"
    except Exception as e:
        print(e)

    print(c1.vin)
