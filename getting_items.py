

class Inventory:
    def __init__(self):
        self._products: list[str] = ["leds", "batteries", "solder"]
        self._prices: list[float] = [1.00, 3.00, 5.00]

    def __repr__(self) -> str:
        product_price_pairs = (
            "{}: ${:.2f}".format(*pair)
            for pair in zip(self._products, self._prices)
        )
        listing = "\n".join(product_price_pairs)
        return "<Inventory>\n{listing}\n</Inventory>".format(listing=listing)

    def __getitem__(self, item: str):
        # poor performance, but will do as an example
        for index, product in enumerate(self._products):
            if product == item:
                return self._prices[index]
        return self.__missing__(item)

    def __contains__(self, item: str) -> bool:
        return item in self._products

    def __missing__(self, key: str) -> str:
        return "Item not found! Can raise error or return default value."


if __name__ == "__main__":
    i = Inventory()
    print(i)

    print(i["leds"])
    print(i["solder"])
    print(i["batteries"])

    # __missing__
    print("__missing__", i["something else"])

    # __contains__
    print("__contains__: ", "something else" in i)
