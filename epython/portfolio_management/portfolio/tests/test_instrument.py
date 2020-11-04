from test_db import db
from portfolio_management.portfolio.instrument import Instrument, InstrumentFx
from portfolio_management.common.base_item import Factory


def test_instrument_new(db):
    _instrument1 = Factory.create('Instrument', db=db, name='Apple', id='AAP', instrument_type='equity',
                                  category='Nasdaq', description='Apple stock', venue='NYSE')
    assert isinstance(_instrument1, Instrument)
    assert _instrument1.name() == 'Apple'


def test_instrument(db):
    _instrument1 = Factory.create('Instrument', db=db, name='Apple', id='AAP', instrument_type='equity',
                                  category='Nasdaq', symbol='AAP', description='Apple stock', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))
    _instrument2 = Factory.create('InstrumentFx', db=db, ccy_pair='EURUSD', id='EURUSD', instrument_type='fx',
                                  category='spot', venue='NYSE')
    print('Instrument: {0}'.format(_instrument1))
    print('Instrument: {0}'.format(_instrument2))
    assert (isinstance(_instrument1, Instrument))
    assert (isinstance(_instrument2, InstrumentFx))
