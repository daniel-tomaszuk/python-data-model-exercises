from math import pi, cos, sin


class ComplexNumber:
    def __init__(self, x: int | float = 1, j: int | float = 1):
        self.x = x
        self.j = j

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} x={self.x}, y={self.j}> @ {id(self)}"

    def __complex__(self) -> complex:
        # implements complex part of a number
        return complex(self.x, self.j)


class Voltage:
    def __init__(self, base_voltage: float, freq_hz: int = 50):
        self.base_voltage = base_voltage
        self.a_freq = 2 * pi * freq_hz  # angular frequency

    def __complex__(self) -> complex:
        # assume time = 1s
        real = cos(self.a_freq) * self.base_voltage
        imag = sin(self.a_freq) * self.base_voltage
        return complex(real, imag)

    def value_at_time(self, t: int | float = 0) -> complex:
        real = cos(self.a_freq * t) * self.base_voltage
        imag = sin(self.a_freq * t) * self.base_voltage
        return complex(real, imag)


if __name__ == "__main__":
    p1 = ComplexNumber(-4, 3.25)
    p2 = ComplexNumber(5.25, 2.33)
    p3 = ComplexNumber(-11.70, -20.25)

    print(complex(p1))
    print(complex(p2))
    print(complex(p3))

    v1 = Voltage(230, 50)
    v2 = Voltage(120, 60)

    print(complex(v1))
    print(complex(v2))
    print("----")
    for i in range(0, 6000):
        t = i / 100
        print(v1.value_at_time(t=t))
