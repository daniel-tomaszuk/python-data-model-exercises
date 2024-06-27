import operator

import pytest

from single_ingeritance.project.implementation import Resource, Validation, ResourceException, CPU


class BaseTestCase:
    @pytest.fixture
    def default_resource_data(self) -> dict:
        return dict(
            name="Resource 1",
            manufacturer="Manufacturer 1",
            total=10,
            allocated=5,
        )

    @pytest.fixture
    def default_cpu_data(self, default_resource_data) -> dict:
        return {
            **default_resource_data,
            "cores": 8,
            "socket": "AMD4",
            "power_watts": 300,
        }


class TestValidators:

    @pytest.mark.parametrize(
        "invalid_value", [
            -1, 0, 2.25, -2.25, "2", "-2", None, [], {}, (), "abcd",
        ]
    )
    def test_validate_positive_integer__raises_error(self, invalid_value):
        with pytest.raises(ValueError) as e:
            Validation.validate_positive_integer(invalid_value)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR

    @pytest.mark.parametrize(
        "allowed_value", [
            1, 2, 10, 50, 100,
        ]
    )
    def test_validate_positive_integer__success(self, allowed_value):
        Validation.validate_positive_integer(allowed_value)

    @pytest.mark.parametrize(
        "x,y,condition_operator", [
            (10, 5, operator.gt),
            (10, 5, operator.ge),
            (5, 10, operator.lt),
            (5, 10, operator.le),
            (10, 10, operator.eq),
        ]
    )
    def test_validate_condition__success(self, x, y, condition_operator):
        Validation.validate_condition(x, y, condition_operator)

    @pytest.mark.parametrize(
        "x,y,condition_operator", [
            (5, 10, operator.gt),
            (5, 6, operator.ge),
            (10, 5, operator.lt),
            (5, 4, operator.le),
            (10, 11, operator.eq),
        ]
    )
    def test_validate_condition__failure(self, x, y, condition_operator):
        with pytest.raises(ResourceException) as e:
            Validation.validate_condition(x, y, condition_operator)
        assert e.value.args[0].startswith("Required condition is not met")


class TestResource(BaseTestCase):
    def test_resource_creation(self, default_resource_data: dict):
        resource = Resource(**default_resource_data)
        assert all(
            getattr(resource, key) == default_resource_data[key]
            for key in default_resource_data.keys()
        )

    def test_resource_str(self, default_resource_data):
        resource = Resource(**default_resource_data)
        assert str(resource) == resource.name

    def test_resource_repr(self, default_resource_data):
        resource = Resource(**default_resource_data)
        assert repr(resource).startswith(
            "<Resource name=Resource 1 manufacturer=Manufacturer 1 total=10 allocated=5>"
        )

    def test_resource_category(self, default_resource_data):
        resource = Resource(**default_resource_data)
        assert resource.category == "resource"

    def test_resource_claim__success(self, default_resource_data):
        claim_count = 3

        resource = Resource(**default_resource_data)
        resource.claim(claim_count)

        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"] + claim_count
        assert resource.available == (
            (default_resource_data["total"] - default_resource_data["allocated"]) - claim_count
        )

    @pytest.mark.parametrize(
        "invalid_value", [-1, 0, 0.25]
    )
    def test_resource_claim__negative_value(self, default_resource_data, invalid_value):
        resource = Resource(**default_resource_data)
        with pytest.raises(ValueError) as e:
            resource.claim(invalid_value)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_claim__resource_not_available(self, default_resource_data):
        resource = Resource(**default_resource_data)
        with pytest.raises(ResourceException) as e:
            resource.claim(resource.available + 1)
        assert e.value.args[0] == Validation.RESOURCE_NOT_AVAILABLE_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_freeup_success(self, default_resource_data):
        freeup_count = 3

        resource = Resource(**default_resource_data)
        resource.freeup(freeup_count)

        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"] - freeup_count
        assert resource.available == (
            (default_resource_data["total"] - default_resource_data["allocated"]) + freeup_count
        )

    @pytest.mark.parametrize(
        "invalid_value", [-1, 0, 0.25]
    )
    def test_resource_freeup_negative_value(self, default_resource_data, invalid_value):
        resource = Resource(**default_resource_data)
        with pytest.raises(ValueError) as e:
            resource.freeup(invalid_value)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_freeup__resource_not_available(self, default_resource_data):
        resource = Resource(**default_resource_data)
        with pytest.raises(ResourceException) as e:
            resource.freeup(resource.allocated + 1)
        assert e.value.args[0] == Validation.FREEUP_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_died_success(self, default_resource_data):
        died_count = 3

        resource = Resource(**default_resource_data)
        resource.died(died_count)

        assert resource.total == default_resource_data["total"] - died_count
        assert resource.allocated == default_resource_data["allocated"] - died_count
        assert resource.available == (
            (default_resource_data["total"] - died_count) - (default_resource_data["allocated"] - died_count)
        )

    @pytest.mark.parametrize(
        "invalid_value", [-1, 0, 0.25]
    )
    def test_resource_died_negative_value(self, default_resource_data, invalid_value):
        resource = Resource(**default_resource_data)
        with pytest.raises(ValueError) as e:
            resource.died(invalid_value)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_died__all_died(self, default_resource_data):
        resource = Resource(**default_resource_data)
        resource.died(resource.total)
        assert resource.total == 0
        assert resource.available == 0
        assert resource.allocated == 0

    def test_resource_died__more_than_available_error(self, default_resource_data):
        resource = Resource(**default_resource_data)
        with pytest.raises(ResourceException) as e:
            resource.died(resource.total + 1)
        assert e.value.args[0] == Validation.DIED_MORE_THAN_AVAILABLE_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_resource_purchase_success(self, default_resource_data):
        purchase_count = 3

        resource = Resource(**default_resource_data)
        resource.purchased(purchase_count)

        assert resource.total == default_resource_data["total"] + purchase_count
        assert resource.allocated == default_resource_data["allocated"]
        assert resource.available == (
            (default_resource_data["total"] + purchase_count) - default_resource_data["allocated"]
        )

    @pytest.mark.parametrize(
        "invalid_value", [-1, 0, 0.25]
    )
    def test_resource_purchase_negative_value(self, default_resource_data, invalid_value):
        resource = Resource(**default_resource_data)
        with pytest.raises(ValueError) as e:
            resource.purchased(invalid_value)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR
        assert resource.total == default_resource_data["total"]
        assert resource.allocated == default_resource_data["allocated"]

    def test_category(self, default_resource_data):
        resource = Resource(**default_resource_data)
        assert resource.category == "resource"


class TestCPU(BaseTestCase):
    def test_cpu_created(self, default_cpu_data):
        cpu = CPU(**default_cpu_data)

        assert cpu.cores == default_cpu_data["cores"]
        assert cpu.socket == default_cpu_data["socket"]
        assert cpu.power_watts == default_cpu_data["power_watts"]
        assert cpu.category == "cpu"

    @pytest.mark.parametrize(
        "invalid_cores_count", [-1, 0, 0.25]
    )
    def test_cpu_invalid_cores_not_allowed(self, default_cpu_data, invalid_cores_count):
        default_cpu_data = {
            **default_cpu_data,
            "cores": invalid_cores_count,
        }
        with pytest.raises(ValueError) as e:
            CPU(**default_cpu_data)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR

    @pytest.mark.parametrize(
        "invalid_power_watts", [-1, 0, 0.25]
    )
    def test_cpu_invalid_cores_not_allowed(self, default_cpu_data, invalid_power_watts):
        default_cpu_data = {
            **default_cpu_data,
            "power_watts": invalid_power_watts,
        }
        with pytest.raises(ValueError) as e:
            CPU(**default_cpu_data)
        assert e.value.args[0] == Validation.POSITIVE_INTEGER_REQUIRED_ERROR


# TODO: CONTINUE WITH THE TESTS
