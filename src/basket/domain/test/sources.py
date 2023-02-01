class Products:
    WEED = ('Weed', (100, 'EUR'))
    VELO = ('Velo', (1200, 'EUR'))
    IPHONE = ('iPhone', (1700, 'USD'))

    INVALID_AMOUNT = ('Invalid Amount', (-20, 'USD'))
    INVALID_CURRENCY = ('Invalid Currency', (20, 'XXX'))


class Promotions:
    THIRD_FREE = (0, 3)
    SECOND_HALF_PRICE = (0.5, 2)
    TWEENTY_PERCENT = (0.8, 1)

    INVALID_RATE = (1.2, 2)
    INVALID_QTF = (0.2, 0)


class Batches:
    IPHONE_PROMO_UNUSED = (Products.IPHONE, 2, [Promotions.THIRD_FREE])
    VELO_PROMO = (Products.VELO, 1, [Promotions.TWEENTY_PERCENT])
    ONE_VELO = (Products.VELO, 1)
    WEED_LARGE_PROMO = (Products.WEED, 12, [Promotions.THIRD_FREE, Promotions.TWEENTY_PERCENT])

    INVALID = (Products.WEED, 0)
