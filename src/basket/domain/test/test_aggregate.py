import unittest
from ..aggregate import Basket
from ..entity import Batch
from ..value_object import Price, Product
from . import sources
from .built import TestProducts, TestPromotions


class TestBasket(unittest.TestCase):

    def test_basket_life_cycle(self):
        basket = Basket()
        basket.add(TestProducts.IPHONE, 3)

        assert basket.price('USD') == 3 * TestProducts.IPHONE.price
        assert basket.price() == 3 * TestProducts.IPHONE.price.change('EUR')

        basket.add(TestProducts.IPHONE, 2, [TestPromotions.THIRD_FREE])
        assert basket.batches[TestProducts.IPHONE].quantity == 5
        assert basket.price('USD') == 4 * TestProducts.IPHONE.price

        basket.add(TestProducts.WEED, 3)
        assert basket.price('EUR') == Price(3700, 'EUR')

        assert basket.total_price('EUR') == Price(4662, 'EUR')
