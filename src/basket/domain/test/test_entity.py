import unittest
from ..entity import Batch
from ..value_object import Product, Promotion, Price
from . import sources
from .built import TestBatches, TestPromotions, TestProducts

class TestBatch(unittest.TestCase):
    def test_batch_update_quantity(self):
        batch = TestBatches.ONE_VELO
        batch.quantity = 2
        assert batch.price == Price(2400, 'EUR')
        assert batch.quantity == 2

    def test_batch_calculate_price(self):
        batch = TestBatches.WEED_LARGE_PROMO
        assert batch.price == Price(640, 'EUR')
        batch.quantity = 2
        assert batch.price == Price(160, 'EUR')
        batch.quantity = 3
        assert batch.price == Price(160, 'EUR'), "Third is free"
