

class Person:
    pass


if __name__ == "__main__":
    print(type(Person))
    print(type(type))
    print(Person.__name__)

    p = Person()
    print(type(p))
    print(p.__class__)
    print(type(p) is p.__class__)
    print(isinstance(p, Person))

    print("\n")
    print(object.__dir__)

    print("\n")
    print(help(type))
    print(help(object))
