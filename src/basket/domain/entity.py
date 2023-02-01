from uuid import uuid4
from .value_object import Product, Qty, Promotion, Price


class Batch:
    def __init__(
        self, product: Product, quantity: Qty, promotions=None, id=None
    ) -> None:
        self.id = id or str(uuid4())[:8]
        self.product = product
        self.quantity = quantity
        self.promotions = promotions or []

    @classmethod
    def build(cls, product, quantity, promotions=None, id=None):
        product = Product(product[0], Price(product[1][0], product[1][1]))
        promotions = [Promotion(rate, qtf) for rate, qtf in promotions or []]
        return Batch(product, quantity, promotions, id)

    def __str__(self):
        return f"{self.quantity} {self.product} for {self.price} with {self.promotions}"

    __repr__ = __str__

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value: Qty):
        self._quantity = Qty(value)

    def _calculate_product_price(self, promotion, base_price):
        nb_of_product_with_promo = int(self.quantity / promotion.quantifyer)
        promo_rate = (
            nb_of_product_with_promo * promotion.rate
            + (self.quantity - nb_of_product_with_promo)
        ) / self.quantity
        product_price = base_price * promo_rate
        return product_price

    @property
    def price(self):
        base_price = self.product.price * 1
        price = base_price * self.quantity
        for promotion in self.promotions:
            new_price = self._calculate_product_price(promotion, base_price)
            price = new_price * self.quantity
            base_price = new_price

        return Price(round(price.amount, 2), price.currency)
