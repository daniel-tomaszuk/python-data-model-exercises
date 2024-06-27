
import operator


class ResourceException(ValueError):
    """Custom exception dedicated to Resource class"""


class Validation:
    POSITIVE_INTEGER_REQUIRED_ERROR = "Please provide positive integer value."
    RESOURCE_NOT_AVAILABLE_ERROR = "Requested resource count is not available at the moment."
    FREEUP_ERROR = "Can't free up more resources than it's allocated."
    DIED_MORE_THAN_AVAILABLE_ERROR = "It's not possible for more that total resource count to be broken."

    @classmethod
    def validate_positive_integer(cls, x: int) -> int:
        if not isinstance(x, int) or x <= 0:
            raise ValueError(cls.POSITIVE_INTEGER_REQUIRED_ERROR)
        return x

    @classmethod
    def validate_condition(cls, x: int, y: int, op: operator, error_message: str = "") -> None:
        if not op(x, y):
            error_message: str = error_message or f"Required condition is not met: {x} {op} {y}"
            raise ResourceException(error_message)


class Resource:
    """General purpose resource class."""

    def __init__(
        self,
        name: str,
        manufacturer: str,
        total: int,
        allocated: int,

    ):
        self._name = name
        self._manufacturer = manufacturer
        self._total = total
        self._allocated = allocated


    @property
    def name(self) -> str:
        return self._name

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def total(self) -> int:
        return self._total

    @property
    def allocated(self) -> int:
        return self._allocated

    @property
    def available(self) -> int:
        return self.total - self.allocated

    @property
    def category(self) -> str:
        """Computed property that returns a lower case version of the class name"""
        return f"{type(self).__name__.lower()}"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} "
            f"name={self.name} "
            f"manufacturer={self.manufacturer} "
            f"total={self.total} "
            f"allocated={self.allocated}> "
            f"@ {hex(id(self))}"
        )

    def claim(self, count: int) -> None:
        """
            Method to take n resources from the pool (as long as inventory is available)
        """
        Validation.validate_positive_integer(count)
        Validation.validate_condition(
            self.available,
            count,
            op=operator.gt,
            error_message=Validation.RESOURCE_NOT_AVAILABLE_ERROR,
        )

        self._allocated += count

    def freeup(self, count: int) -> None:
        """
            Method to return n resources to the pool (e.g. disassembled some builds)
        """
        Validation.validate_positive_integer(count)
        Validation.validate_condition(
            self._allocated,
            count,
            op=operator.ge,
            error_message=Validation.FREEUP_ERROR,
        )

        self._allocated -= count

    def died(self, count: int) -> None:
        """
            Method to return and permanently remove inventory from the pool
            (e.g. they broke something) - as long as total available allows it
        """
        Validation.validate_positive_integer(count)
        Validation.validate_condition(
            self.total,
            count,
            op=operator.ge,
            error_message=Validation.DIED_MORE_THAN_AVAILABLE_ERROR,
        )
        self._allocated -= count
        self._allocated = self._allocated if self._allocated > 0 else 0
        self._total -= count
        self._total = self.total if self._total > 0 else 0

    def purchased(self, count: int) -> None:
        """
            Method to add inventory to the pool (e.g. they purchased a new CPU)
        """
        Validation.validate_positive_integer(count)
        self._total += count


class CPU(Resource):

    def __init__(
        self,
        name: str,
        manufacturer: str,
        total: int,
        allocated: int,
        cores: int,
        socket: str,
        power_watts: int,

    ):
        super().__init__(name, manufacturer, total, allocated)

        self._cores = Validation.validate_positive_integer(cores)
        self._socket = socket
        self._power_watts = Validation.validate_positive_integer(power_watts)

    @property
    def cores(self) -> int:
        return self._cores

    @property
    def socket(self) -> str:
        return self._socket

    @property
    def power_watts(self) -> int:
        return self._power_watts


class Storage(Resource):
    def __init__(
        self,
        name: str,
        manufacturer: str,
        total: int,
        allocated: int,
        capacity_gb: int,
    ):
        super().__init__(name, manufacturer, total, allocated)
        self._capacity_gb = Validation.validate_positive_integer(capacity_gb)

    @property
    def capacity_gb(self) -> int:
        return self._capacity_gb


class HDD(Storage):
    def __init__(
        self,
        name: str,
        manufacturer: str,
        total: int,
        allocated: int,
        capacity_gb: int,
        size: str,
        rpm: int,
    ):
        super().__init__(name, manufacturer, total, allocated, capacity_gb)
        self._size = size
        self._rpm = rpm

    @property
    def size(self) -> str:
        return self._size

    @property
    def rpm(self) -> int:
        return self._rpm
