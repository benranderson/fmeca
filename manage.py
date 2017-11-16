#!/usr/bin/env python
import os
import subprocess
import sys

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import Facility, Area, Component, SubComponent, Vessel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def make_shell_context():
    return dict(app=app, db=db, Facility=Facility)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=8080))


@manager.command
def seeddb():
    """Seeds the database."""
    for i in range(5):
        f = Facility(name='facility-{}'.format(i))
        db.session.add(f)
        for j in range(5):
            a = Area(name='area-{}-{}'.format(j, i), remaining_life=7,
                     equity_share=0.72, facility=f)
            db.session.add(a)
            for k in range(10):
                c = Component(ident='component-{}-{}-{}'.format(k, j, i),
                              annual_risk=100000, inspect_int=4, area=a)
                db.session.add(c)
                for m in range(5):
                    sc = SubComponent(ident='sc-{}-{}-{}-{}'.format(m, k, j, i),
                                      category=100000, component=c)
    db.session.commit()

    db.session.add(Vessel(name='Heavy Lift Vessel',
                          abbr='HLV', rate=300000, mob_time=7))
    db.session.add(Vessel(name='Dive Support Vessel',
                          abbr='DSV', rate=100000, mob_time=7))
    db.session.commit()


@manager.command
def testcore(html=False):
    """ Run unit tests on core module"""
    import pytest
    pytest.main(['-x', 'core/tests'])


@manager.command
def test(html=False):
    """Run the unit tests."""

    # start coverage engine
    import coverage
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

    # run tests
    import unittest
    from tests import suite
    unittest.TextTestRunner(verbosity=2).run(suite)

    # print coverage report
    cov.stop()
    cov.report()
    print('')

    if html:
        # create html coverage report
        covdir = os.path.join(HERE, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


@manager.command
def createdb(drop_first=False):
    """Creates a database."""
    if drop_first:
        db.drop_all()
    db.create_all()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    # migrate database to latest revision
    upgrade()


@manager.command
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                print('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


if __name__ == '__main__':
    manager.run()
