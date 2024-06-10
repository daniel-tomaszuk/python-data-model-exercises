import sys
from time import sleep


class Buffer:
    def __init__(self, max_length: int = 32) -> None:
        self._data = b""
        self.max_length = max_length

    def write(self, msg: bytes) -> None:
        if len(self._data) < self.max_length:
            self._data += msg[:self.max_length - len(self._data)]

    def flush(self) -> None:
        if self._data:
            sys.stdout.write(self._data.decode("UTF-8"))
            self._data = b""

    def __del__(self):
        # Decreases reference count by 1.
        # __del__  is only called when the instance is actually being deleted, so when reference count is 0
        # it's not guaranteed to run every time when it's expected. Ex. sudden power outage
        print("Deleting!")
        self.flush()


if __name__ == "__main__":
    b1 = Buffer()
    b2 = b1
    b1.write(b"Daniel is writing!")
    del b1

    sleep(1)
    print("End of scrip!")
    sleep(1)
