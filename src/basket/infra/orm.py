from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    ARRAY,
    TypeDecorator,
    UUID,
    UniqueConstraint,
    BINARY,
    create_engine
)
from sqlalchemy.orm import registry, relationship, sessionmaker
from ..domain.value_object import Product, Price, Promotion
from ..domain.entity import Batch

class PriceORMType(TypeDecorator):
    impl = String
    def process_bind_param(self, value, dialect):
        return str(value)
    def process_result_value(self, value, dialect):
        args = eval(value)
        return Price(*args)

class PromotionsOrmType(TypeDecorator):
    impl = String
    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        values = eval(value)
        return Promotion(*values)

mapper_registry = registry()
metadata = mapper_registry.metadata

product_table = Table(
    "product",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('price', PriceORMType),
    UniqueConstraint('name', 'price', name="uq_product__name__price")
)

batch_table = Table(
    "batch",
    metadata,
    Column('id', String, primary_key=True),
    Column('quantity', Integer),
    Column('promotions', PromotionsOrmType),
    Column('product_id', Integer, ForeignKey('product.id'))
)

def start_orm():
    mapper_registry.map_imperatively(Product, product_table)
    mapper_registry.map_imperatively(Batch, batch_table, properties={
        "product": relationship("Product", uselist=False)
    })


class ORM:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.start_orm()
        return cls._instance

    def __init__(self):
        self._engine = None

    @classmethod
    def start_orm(cls):
        mapper_registry.map_imperatively(Product, product_table)
        mapper_registry.map_imperatively(Batch, batch_table, properties={
            "product": relationship("Product", uselist=False)
        })

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine("sqlite:///:memory:", echo=True)
            metadata.create_all(self.engine)
        return self._engine

    def txfactory(self):
        return sessionmaker(bind=self.engine)

    class Transaction:
        def start(self):
            self.tx = sessionmaker(bind=self.engine)()
            return self.tx

        def close(self):
            self.tx.close()
