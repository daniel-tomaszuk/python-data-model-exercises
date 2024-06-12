

class Binary:
    def __init__(self, number: int):
        self.number = number
        self._binary = bin(number)

    def __repr__(self):
        return f"<{self.__class__.__name__} number={self.number} bin_number={self._binary}> @ {id(self)}"

    def __lshift__(self, other: "Binary") -> "Binary":
        return Binary(self.number << other.number)

    def __rshift__(self, other: "Binary") -> "Binary":
        return Binary(self.number >> other.number)

    def __rlshift__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            return Binary(other << self.number)
        return Binary(other.number << other.number)

    def __rrshift__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            return Binary(other >> self.number)
        return Binary(other.number >> self.number)

    def __irshift__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            self.number >>= other
        else:
            self.number >>= other.number
        self._binary = bin(self.number)
        return self

    def __ilshift__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            self.number <<= other
        else:
            self.number <<= other.number
        self._binary = bin(self.number)
        return self


if __name__ == "__main__":
    b1 = Binary(4)
    b2 = Binary(64)

    print(b1 << b2)
    print(b2 << b1)

    print(b1 >> b2)
    print(b2 >> b1)

    print(4 << b1)
    print(8 >> b1)

    b1 <<= 2
    print(b1)

    b2 >>= 4
    print(b2)
