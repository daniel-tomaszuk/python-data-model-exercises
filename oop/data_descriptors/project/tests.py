import pytest


from data_descriptors.project.project import IntegerField, CharField


class TestValidFields:

    @pytest.fixture
    def test_class(self, min_value: int = None, max_value: int = None):

        # other way to do it - use `type` class factory
        # return type("DummyTestClass", (), dict(min_value=min_value, max_value=max_value))

        class DummyTestClass:
            integer_field = IntegerField()
            integer_field_with_boundaries = IntegerField(min_value=-10, max_value=10)

            char_field = CharField()
            char_field_with_boundaries = CharField(min_value=1, max_value=5)
        return DummyTestClass

    def test_integer_field_data_descriptor__no_instance(self, test_class):

        assert isinstance(test_class.integer_field, IntegerField)
        assert isinstance(test_class.integer_field_with_boundaries, IntegerField)

        assert test_class.integer_field.min_value is None
        assert test_class.integer_field.max_value is None
        assert test_class.integer_field_with_boundaries.min_value == -10
        assert test_class.integer_field_with_boundaries.max_value == 10

    def test_integer_field_data_descriptor__with_instance__success(self, test_class):
        instance = test_class()

        instance.integer_field = 5
        assert instance.integer_field == 5
        assert instance.__dict__["integer_field"] == 5

        instance.integer_field_with_boundaries = 10
        assert instance.integer_field_with_boundaries == 10
        assert instance.__dict__["integer_field_with_boundaries"] == 10

        instance.integer_field_with_boundaries = -10
        assert instance.integer_field_with_boundaries == -10
        assert instance.__dict__["integer_field_with_boundaries"] == -10

    def test_integer_field_data_descriptor__with_instance__exceptions(self, test_class):
        instance = test_class()

        with pytest.raises(TypeError) as e:
            instance.integer_field = "abcd"
        assert e.value.args[0] == "integer_field must have int type"

        with pytest.raises(ValueError) as e:
            instance.integer_field_with_boundaries = -20
        assert e.value.args[0] == "integer_field_with_boundaries must be greater or equal to -10"

        with pytest.raises(ValueError) as e:
            instance.integer_field_with_boundaries = 20
        assert e.value.args[0] == "integer_field_with_boundaries must be less or equal to 10"

    def test_char_field_data_descriptor__no_instance(self, test_class):

        assert isinstance(test_class.char_field, CharField)
        assert isinstance(test_class.char_field_with_boundaries, CharField)

        assert test_class.char_field.min_value is None
        assert test_class.char_field.max_value is None
        assert test_class.char_field_with_boundaries.min_value == 1
        assert test_class.char_field_with_boundaries.max_value == 5

    def test_char_field_data_descriptor__with_instance__success(self, test_class):
        instance = test_class()

        instance.char_field = "abcd"
        assert instance.char_field == "abcd"
        assert instance.__dict__["char_field"] == "abcd"

        instance.char_field_with_boundaries = "xyz"
        assert instance.char_field_with_boundaries == "xyz"
        assert instance.__dict__["char_field_with_boundaries"] == "xyz"

    def test_char_field_data_descriptor__with_instance__exceptions(self, test_class):
        instance = test_class()

        with pytest.raises(TypeError) as e:
            instance.char_field = 10
        assert e.value.args[0] == "char_field must have str type"

        with pytest.raises(ValueError) as e:
            instance.char_field_with_boundaries = ""
        assert e.value.args[0] == "char_field_with_boundaries must have at least 1 characters"

        with pytest.raises(ValueError) as e:
            instance.char_field_with_boundaries = "a" * 20
        assert e.value.args[0] == "char_field_with_boundaries must not have more than 5 characters"

        with pytest.raises(ValueError) as e:
            CharField(min_value=-10)
        assert e.value.args[0] == "Minimal value can not be less than 0"
