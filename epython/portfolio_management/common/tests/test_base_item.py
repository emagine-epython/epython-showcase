import kydb
from portfolio_management.kydb_config import OBJDB_CONFIG
from portfolio_management.common.base_item import BaseItem, Factory
import portfolio_management.utils.func_utils as fu
import datetime
from test_db import db
import pytest


def test_BaseItem(db):
    name = 'Test'
    updated = datetime.datetime.now()
    base_item = Factory.create('BaseItem', db=db, name=name, updated=updated)
    assert (base_item.name() == name)
    assert (base_item.updated() == updated)
