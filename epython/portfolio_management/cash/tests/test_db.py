import kydb
import kydb_config
import pytest


@pytest.fixture
def db():
    db = kydb.connect('memory://local')
    db.mkdir('/portfolio_management/test')
    db.upload_objdb_config(kydb_config.OBJDB_CONFIG)
    return db
