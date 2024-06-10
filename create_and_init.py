from uuid import uuid4


class Person:

    def __new__(cls, *args, **kwargs) -> "Person":
        # Creates new object
        print("Class Type ", type(cls))
        print("Class ", cls)
        print("Args ",  args)
        print("Kwargs ", kwargs)
        obj = super().__new__(cls)
        obj.uuid = str(uuid4())

        return obj  # passed into __init__

    def __init__(self, name: str, age: int) -> None:
        # Called after __new__, new object gets init values
        self.name = name
        self.age = age


if __name__ == "__main__":
    person = Person("Daniel", 33)
    print(person.name)
    print(person.age)
    print(person.uuid)

