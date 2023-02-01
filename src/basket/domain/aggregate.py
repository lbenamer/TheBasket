from typing import List
from uuid import uuid4
from .value_object import Product, Qty, Price, Currency
from .entity import Batch

class Basket:
    def __init__(self, id: str = None,  batches: List[Batch] = None):
        self.id = id or str(uuid4())[:8]
        self.batches = { batch.product: batch for batch in batches or [] }

    @classmethod
    def build(cls, batches=None, id=None):
        return Basket(id, [ Batch.build(*src) for src in batches or [] ])

    def add(self, product: Product, quantity: Qty, promotions=None):
        if product in self.batches:
            self.batches[product].quantity += quantity
            self.batches[product].promotions += promotions or []
        else:
            self.batches[product] = Batch(product, quantity, promotions)
        return

    def remove(self, product: Product, quantity: Qty):
        if product in self.batches:
            batch = self.batches[product]
            try:
                batch.quantity -= quantity
            except ValueError:
                del self.batches[product]

    def price(self, currency: Currency = 'EUR') -> Price:
        prices = []
        for batch in self.batches.values():
            if batch.price.currency == currency:
                prices.append(batch.price)
            else:
                prices.append(batch.price.change(currency))
        return sum(prices) or Price(0, currency)

    def total_price(self, currency: Currency = 'EUR') -> Price:
        FEE_RATE = 1.05
        VAT_RATE = 1.20

        return self.price(currency) * FEE_RATE * VAT_RATE
