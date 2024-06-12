

class Binary:
    def __init__(self, number: int):
        self.number: int = number
        self._bin_number: str = bin(number)

    def __repr__(self):
        return f"<{self.__class__.__name__} number={self.number} bin_number={self._bin_number}> @ {id(self)}"

    def __and__(self, other: "Binary") -> "Binary":
        return Binary(self.number & other.number)

    def __rand__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            return Binary(other & self.number)
        return Binary(other.number & self.number)

    def __iand__(self, other: "Binary") -> "Binary":
        self.number &= other.number
        self._bin_number = bin(self.number)
        return self

    def __or__(self, other: "Binary") -> "Binary":
        return Binary(self.number | other.number)

    def __ror__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            return Binary(other | self.number)
        return Binary(other.number | self.number)

    def __ior__(self, other: "Binary") -> "Binary":
        self.number |= other.number
        self._bin_number = bin(self.number)
        return self

    def __xor__(self, other: "Binary") -> "Binary":
        return Binary(self.number ^ other.number)

    def __rxor__(self, other: "Binary") -> "Binary":
        if isinstance(other, int):
            return Binary(other ^ self.number)
        return Binary(other.number ^ self.number)

    def __ixor__(self, other: "Binary") -> "Binary":
        self.number ^= other.number
        self._bin_number = bin(self.number)
        return self


if __name__ == "__main__":
    b1 = Binary(5)  # 0b101
    b2 = Binary(7)  # 0b111

    print(b1 & b2)
    print(b1 | b2)
    print(b1 ^ b2)

    print(11 & b2)
    print(5 | b2)

    b1 &= b2
    print(b1)

    b2 |= b1
    print(b2)

    b1 ^= b2
    print(b1)
