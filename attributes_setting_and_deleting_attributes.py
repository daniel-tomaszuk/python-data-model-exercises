

class Restaurant:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.ratings: list[str] = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} location={self.location}> @ {id(self)}"

    def __setattr__(self, key: str, value):
        # Called every time dot `.` notation is used to set a value, also called by `setattr`
        print(f"__setattr__ -> {key}: {value}")

        if key == "ratings" and hasattr(self, "ratings"):
            print("Ratings can not be set directly!")
            return self.ratings

        self.__dict__[key] = value  # adds the key: value pair into instance attributes, __slots__ would change that

    def __delattr__(self, item: str):
        if item == "name":
            print("Name can not be removed!")
            return

        # del self.__dict__[item]  # completely removes the attribute
        self.__dict__[item] = None  # set value as None


if __name__ == "__main__":
    r = Restaurant(name="Gyro Bar", location="Somewhere")
    print(r)

    r.ratings = "test"
    print(r.ratings)

    r.ratings.append("Good!")
    print(r.ratings)

    delattr(r, "name")
    delattr(r, "location")
    print(r)
