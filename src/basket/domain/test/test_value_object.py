import unittest
from ..value_object import Price, Promotion, Product, Qty, Rate

class TestPrice(unittest.TestCase):
    def test_build_price(self):
        price = Price(10, 'BTC')
        assert price.amount == 10
        assert price.currency == 'BTC'

    def test_build_invalid_price(self):
        with self.assertRaises(ValueError):
            Price(10, 'XXX')
        with self.assertRaises(ValueError):
            Price(-10, 'EUR')

    def test_price_is_immutable(self):
        price = Price(10, 'BTC')
        with self.assertRaises(AttributeError):
            price.amount = 12
        with self.assertRaises(AttributeError):
            price.currency = 'XXX'

    def test_price_equality(self):
        price_1 = Price(10, 'BTC')
        price_2 = Price(10, 'BTC')
        price_3 = Price(10, 'EUR')
        assert price_1 == price_2
        assert price_1 != price_3

    def test_price_operations(self):
        price_1 = Price(10, 'BTC')
        price_2 = Price(2, 'BTC')
        price_3 = Price(3, 'EUR')

        assert price_1 + price_2 == Price(12, 'BTC')
        assert price_1 - price_2 == Price(8, 'BTC')
        with self.assertRaises(TypeError):
            price_1 + price_3

        with self.assertRaises(TypeError):
            price_1 + 42

        assert price_1 * price_2 == Price(20, 'BTC')
        assert price_3 * 3 == Price(9, 'EUR')

    def test_change_currency(self):
        price = Price(10, 'BTC')
        change = price.change('EUR')
        assert change.amount == 100
        assert change.currency == 'EUR'

        with self.assertRaises(ValueError):
            price.change('XXX')


    def test_litteral_price(self):
        Price('10', 'BTC')

class TestPromotion(unittest.TestCase):
    def test_build_promotion(self):
        promo = Promotion(0.8, 3)
        assert type(promo.rate) is Rate
        assert type(promo.quantifyer) is Qty


class TestProduct(unittest.TestCase):
    def test_build_product(self):
        product = Product('velo', Price(1400, 'EUR'))
        assert product.name == 'velo'
        assert product.price.amount == 1400
        assert product.price.currency == 'EUR'

    def test_product_equality(self):
        product = Product('velo', Price(1400, 'EUR'))
        assert hash(product) == hash(Product(product.name, product.price))
        assert product == Product(product.name, product.price)
        assert product !=Product(product.name, Price(100, 'EUR'))
