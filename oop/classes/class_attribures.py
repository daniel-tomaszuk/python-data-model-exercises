

class Person:
    pass


class Program:
    language = "Python"
    version = "3.12"

    def __repr__(self):
        return f"<{self.__class__.__name__} lang={self.language} ver={self.version}> @ {id(self)}"


if __name__ == "__main__":
    print(type(Program))
    print(Program.language)
    print(Program.version)
    print("__dict__:", Program.__dict__)

    instance_1 = Program()
    print(instance_1)

    Program.version = "3.13"
    print(Program.version)

    instance_2 = Program()
    print(instance_2)
    print(instance_1)  # !! version is updated for every instance

    print(getattr(Program, "version"))
    setattr(Program, "version", "3.11")
    print(Program.version)
    print(instance_2)
    print(instance_1)  # !! version is updated for every instance

    print(getattr(Program, "test", "No such attr"))

    Program.y = "test"
    print(Program.__dict__)
