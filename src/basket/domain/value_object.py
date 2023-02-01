from typing import NamedTuple
from collections import namedtuple


class Amount(float):
    def __new__(cls, value):
        value = float.__new__(cls, value)
        if value is not None and value < 0:
            raise ValueError("Amount value must be positive")
        return value


class Currency(str):
    ALLOWED = ["BTC", "EUR", "USD"]

    def __new__(cls, value):
        if value not in cls.ALLOWED:
            raise ValueError("Invalid Currency")
        return str.__new__(cls, value)


class PriceType(NamedTuple):
    amount: Amount
    currency: Currency

    def __str__(self):
        return f"({self.amount}, '{self.currency}')"

    def __add__(self, other):
        if isinstance(other, PriceType) and self.currency == other.currency:
            return Price(self.amount + other.amount, self.currency)
        if not other:
            return Price(self.amount, self.currency)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, PriceType) and self.currency == other.currency:
            return Price(self.amount - other.amount, self.currency)

        raise TypeError("Invalid operation")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Price(self.amount * other, self.currency)
        if isinstance(other, PriceType):
            return Price(self.amount * other.amount, self.currency)

    def __bool__(self):
        return bool(self.amount)

    __repr__ = __str__
    __radd__ = __add__
    __rmul__ = __mul__


class Price(PriceType):
    CHANGE = {
        "BTC": 0.1,
        "EUR": 1,
        "USD": 2,
    }
    assert list(CHANGE.keys()) == Currency.ALLOWED

    def __new__(cls, amount: int, currency: str):
        return super().__new__(cls, Amount(amount), Currency(currency))

    def change(self, currency):
        try:
            rate = self.CHANGE[currency] / self.CHANGE[self.currency]
            return Price(self.amount * rate, currency)
        except KeyError:
            raise ValueError("Invalid currency")


class Qty(int):
    def __new__(cls, value: int):
        if value <= 0:
            raise ValueError("Qty must exist")
        return int.__new__(cls, value)


class Rate(float):
    def __new__(cls, value: float):
        if not 0 <= value <= 1:
            raise ValueError("Rate must be between 0 and 1")
        return float.__new__(cls, value)


class Promotion(namedtuple("Promotion", ["rate", "quantifyer"])):
    def __new__(cls, rate, quantifyer):
        return super().__new__(cls, Rate(rate), Qty(quantifyer))

    def __str__(self):
        return f"({self.rate}, {self.quantifyer})"

    __repr__ = __str__


class Product:
    def __init__(self, name: str, price: Price):
        self.name = name
        self.price = price

    @classmethod
    def build(cls, name: str, price: tuple):
        amount, currency = price
        return Product(name, Price(amount, currency))

    def __str__(self):
        return f"{self.name} {self.price}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        return self.name == other.name and self.price == other.price

    __repr__ = __str__
