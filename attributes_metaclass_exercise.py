import functools


class AnnouncerMeta(type):
    """
    Print method name and arg when it's called.
    Somthing is wrong here, please fix it.

    Note:
        The issue in the provided code is with the usage of functools.wraps and the creation of the call_wrapper
        function inside the loop. The problem arises because the func and name variables are
        captured by the call_wrapper function, which results in all wrapped functions
        referencing the last func and name values from the loop.

    """
    #
    # def __new__(cls, class_name, bases, namespace):
    #     for name, func in list(namespace.items()):
    #         if callable(func):
    #             @functools.wraps(func, name)
    #             def call_wrapper(*args, **kwargs):
    #                 try:
    #                     return func(*args, **kwargs)
    #                 finally:
    #                     print(f"Called {name}")
    #
    #             namespace[name] = call_wrapper
    #     return type.__new__(cls, class_name, bases, namespace)

    # Solution - create one more additional function with its own namespace so wrapper uses the right name and func
    def __new__(cls, class_name, bases, namespace):
        for name, func in list(namespace.items()):
            if callable(func):
                namespace[name] = cls.wrap_function(func, name)
        return type.__new__(cls, class_name, bases, namespace)

    @classmethod
    def wrap_function(cls, func, name):
        @functools.wraps(func)
        def call_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            finally:
                print(f"Called {name} with args: {args} and kwargs: {kwargs}")

        return call_wrapper


class ExampleClass(metaclass=AnnouncerMeta):
    """
    Example metaclass usage. Nothing wrong here.
    """

    def foo(self, n: int) -> str:
        return f"foo{n}"

    def bar(self, n: int) -> str:
        return f"bar{n}"


if __name__ == "__main__":
    instance = ExampleClass()

    # check out wrong and right versions of meta __new__
    print(instance.foo(1))
    print(instance.bar(2))
