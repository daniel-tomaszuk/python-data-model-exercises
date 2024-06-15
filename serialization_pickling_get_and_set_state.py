import datetime
import pickle
from copy import deepcopy


class Employee:

    def __init__(self, name: str, title: str, supervisors: tuple["Employee", ...] | None = None):
        self.name = name
        self.title = title
        self.supervisors = supervisors

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"name={self.name} "
            f"title={self.title} "
            f"supervisors={self.supervisors}"
            f"> @ {id(self)}"
        )

    def __getstate__(self) -> dict:
        # gets object state to be pickled
        state = deepcopy(self.__dict__)
        print(f"__getstate__: {state}")

        if "supervisors":
            del state["supervisors"]

        state["save_date"] = datetime.datetime.now()

        return state

    def __setstate__(self, state):
        # sets object state when unpickling
        print(f"__setstate__: {state}")
        self.supervisors = None
        for key in state:
            setattr(self, key, state[key])


if __name__ == "__main__":
    s1 = Employee(name="Mick", title="PO")
    s2 = Employee(name="Emily", title="PM")
    e1 = Employee(name="John", title="Python Developer", supervisors=(s1, s2))

    print(s1)
    print(s2)
    print(e1)

    s1_dump = pickle.dumps(s1)
    print(s1_dump)
    print(pickle.loads(s1_dump))

    e1_dump = pickle.dumps(e1)
    print(e1_dump)

    e1_loads = pickle.loads(e1_dump)
    print(e1_loads)

    print(e1_loads.name)
    print(e1_loads.title)
    print(e1_loads.save_date)
    print(e1_loads.supervisors)
