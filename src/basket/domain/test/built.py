import unittest
from . import sources
from ..entity import Batch
from ..value_object import Product, Promotion

class _TestPromotions:
    @property
    def THIRD_FREE(self):
        return Promotion(*sources.Promotions.THIRD_FREE)
    @property
    def SECOND_HALF_PRICE(self):
        return Promotion(*sources.Promotions.SECOND_HALF_PRICE)
    @property
    def TWENTY_PERCENT(self):
        return Promotion(*sources.Promotions.TWEENTY_PERCENT)

    _SET_INVALID = None
    try:
        _SET_INVALID = Promotion(*sources.Promotions.INVALID_RATE)
    except ValueError:
        pass
    assert _SET_INVALID is None

    try:
        _SET_INVALID = Promotion(*sources.Promotions.INVALID_QTF)
    except ValueError:
        pass
    assert _SET_INVALID is None

class _TestProducts:
    @property
    def IPHONE(self):
        return Product.build(*sources.Products.IPHONE)

    @property
    def VELO(_):
        return Product.build(*sources.Products.VELO)

    @property
    def WEED(cls):
        return Product.build(*sources.Products.WEED)

    _SET_INVALID = None
    try:
        _SET_INVALID = Product.build(*sources.Products.INVALID_AMOUNT)
    except ValueError:
        pass
    assert _SET_INVALID is None
    try:
        _SET_INVALID = Product.build(*sources.Products.INVALID_CURRENCY)
    except ValueError:
        pass
    assert _SET_INVALID is None

class _TestBatches:
    @property
    def IPHONE_PROMO_UNUSED(self):
        return Batch.build(*sources.Batches.IPHONE_PROMO_UNUSED)
    @property
    def VELO_PROMO(self):
        return Batch.build(*sources.Batches.VELO_PROMO)
    @property
    def ONE_VELO(self):
        return Batch.build(*sources.Batches.ONE_VELO)
    @property
    def WEED_LARGE_PROMO(self):
        return Batch.build(*sources.Batches.WEED_LARGE_PROMO)

    _SET_INVALID = None
    try:
        _SET_INVALID = Batch.build(*sources.Batches.INVALID)
    except ValueError:
        pass
    assert _SET_INVALID is None


TestPromotions = _TestPromotions()
TestProducts = _TestProducts()
TestBatches = _TestBatches()
