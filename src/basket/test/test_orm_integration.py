from sqlalchemy import select
from basket.domain.value_object import Product
from basket.domain.test import sources


def test_orm_integration(tx):
    stmt = select(Product).where(Product.name == sources.Products.WEED[0])
    result = tx.scalars(stmt).first()
    assert result.price


# def test_batch_integration(tx):
#     from basket.domain.test.built import TestBatches
#     with  tx:
#         # batch = Batch.build(*sources.Batches.IPHONE_PROMO_UNUSED)
#         tx.add(TestBatches.IPHONE_PROMO_UNUSED)
#         tx.commit()
