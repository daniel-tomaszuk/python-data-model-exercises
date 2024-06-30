import typing as t


class ValidField:
    _VALID_TYPE = None

    def __init__(self, min_value: int = None, max_value: int = None) -> None:
        self.type_ = self._VALID_TYPE
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: object) -> t.Any:
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: t.Any) -> None:
        raise NotImplementedError


class IntegerField(ValidField):
    _VALID_TYPE = int

    def __set__(self, instance: object, value: int) -> None:
        if not isinstance(value, self.type_):
            raise TypeError(f"{self.name} must have {self.type_.__name__} type")

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be greater or equal to {self.min_value}")

        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be less or equal to {self.max_value}")

        instance.__dict__[self.name] = value


class CharField(ValidField):
    _VALID_TYPE = str

    def __init__(self, min_value: int = None, max_value: int = None) -> None:
        if min_value is not None and min_value < 0:
            raise ValueError("Minimal value can not be less than 0")

        super().__init__(min_value=min_value, max_value=max_value)

    def __set__(self, instance: object, value: str) -> None:
        if not isinstance(value, self.type_):
            raise TypeError(f"{self.name} must have {self.type_.__name__} type")

        if self.min_value is not None and len(value) < self.min_value:
            raise ValueError(f"{self.name} must have at least {self.min_value} characters")

        if self.max_value is not None and len(value) > self.max_value:
            raise ValueError(f"{self.name} must not have more than {self.max_value} characters")

        instance.__dict__[self.name] = value
