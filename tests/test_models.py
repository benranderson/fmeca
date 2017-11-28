import os
import pytest

from app import create_app
from app import db as _db
from app.models import Vessel, VesselTrip, Consequence


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test Flask application."""
    app = create_app('testing')

    # establish an application context before running the tests
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


def test_vessel_model(session):
    v = Vessel(abbr='DSV')

    session.add(v)
    session.commit()

    assert v.id > 0
    assert 'DSV' in repr(v)


def test_vesseltrip_model(session):
    v = Vessel(day_rate=1000, mob_time=5)
    session.add(v)

    vt = VesselTrip(active_repair_time=10, vessel=v)

    session.add(vt)
    session.commit()

    assert vt.id > 0
    assert '10' in repr(vt)
    assert vt.total_cost == 15000


def test_consequence(session):
    c = Consequence(name='Minor Intervention')

    session.add(c)
    session.commit()

    assert c.id > 0
    assert 'Minor Intervention' in repr(c)
