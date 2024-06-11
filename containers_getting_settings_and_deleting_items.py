

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

    def __setitem__(self, key: str, value: int | float):
        if key in self:  # uses __contains__
            self._prices[self._products.index(key)] = value
        else:
            self._products.append(key)
            self._prices.append(value)

    def __getitem__(self, item: str) -> str:
        # poor performance, but will do as an example
        for index, product in enumerate(self._products):
            if product == item:
                return self._prices[index]
        return self.__missing__(item)

    def __delitem__(self, key: str):
        if key in self:  # uses __contains__
            item_index: int = self._products.index(key)
            del self._products[item_index]
            del self._prices[item_index]
        else:
            self.__missing__(key)

    def __contains__(self, item: str) -> bool:
        return item in self._products

    def __missing__(self, key: str) -> str:
        message: str = f"Item `{key}` not found! Can raise error or return default value."
        print(message)
        return message


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

    # __setitem__
    print(i["leds"])
    i["leds"] += 5
    print(i["leds"])

    # add new item
    i["wire"] = 10.0
    print(i)

    # __delitem__
    del i["wire"]
    print(i)

    del i["other"]
