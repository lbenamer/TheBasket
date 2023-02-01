import pytest
from sqlalchemy.orm import sessionmaker, clear_mappers

from ..infra.orm import ORM


def populate_engine(engine):
    with sessionmaker(bind=engine)() as tx:
        from basket.domain.test.built import TestProducts

        seeds = [TestProducts]
        for seed in seeds:
            for name in dir(seed):
                if not name.startswith("_"):
                    obj = getattr(seed, name)
                    tx.add(obj)
            tx.commit()


@pytest.fixture
def engine():
    orm = ORM()
    populate_engine(orm.engine)
    yield orm.engine
    clear_mappers()
    orm.engine.dispose()


@pytest.fixture
def tx(engine):
    with sessionmaker(bind=engine)() as tx:
        yield tx
