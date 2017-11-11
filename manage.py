#!/usr/bin/env python
import os

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import Facility, Area, Component, Vessel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=8080))


@manager.command
def seed_db():
    """Seeds the database."""
    facility = Facility(name='Foinaven')
    db.session.add(facility)
    db.session.add(Area(name='DC1', remaining_life=7,
                        equity_share=0.72, facility=facility))
    db.session.add(Area(name='DC2A', remaining_life=7,
                        equity_share=0.42, facility=facility))
    db.session.add(Component(ident='M1', annual_risk=100000, inspect_int=4))
    db.session.add(Component(ident='SUT1', annual_risk=20000, inspect_int=8))
    db.session.add(Vessel(name='Heavy Lift Vessel',
                          abbr='HLV', rate=300000, mob_time=7))
    db.session.add(Vessel(name='Dive Support Vessel',
                          abbr='DSV', rate=100000, mob_time=7))
    db.session.commit()


@manager.command
def test():
    """Run the unit tests."""
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()
    import unittest
    from tests import suite
    unittest.TextTestRunner(verbosity=2).run(suite)
    COV.stop()
    COV.report()
    covdir = os.path.join(HERE, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


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
