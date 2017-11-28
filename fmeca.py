import os
import click
import json
# import subprocess
# import sys

from flask_migrate import Migrate

from app import create_app, db
from app.models import FailureMode, Facility, Area, Component, SubComponent, Vessel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


migrate = Migrate(app, db)

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Facility=Facility, Area=Area)


# @app.cli.command()
# def test():
#     """Run the unit tests."""
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
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


@app.cli.command()
@click.option('--drop_first', default=False)
def createdb(drop_first):
    """Creates a database."""
    if drop_first:
        db.drop_all()
    db.create_all()


@app.cli.command()
def seeddb():
    """Seeds the database."""

    fms_json = json.load(open('failure_modes.json'))
    for sc in fms_json:
        for fm_json in fms_json[sc]:
            if fms_json[sc][fm_json]["Random/Time Dependant"] == "T.D.":
                time_dependant = True
            else:
                time_dependant = False
            fm = FailureMode(subcomponent_category=sc,
                             description=fm_json,
                             time_dependant=time_dependant,
                             mean_time_to_failure=fms_json[sc][fm_json]["BP Ored MTTF"],
                             detectable=fms_json[sc][fm_json]["Detectable by Inspection"],
                             inspection_type=fms_json[sc][fm_json]["Type of Inspection"],
                             consequence=fms_json[sc][fm_json]["Consequence"])
            db.session.add(fm)

    for i in range(5):
        f = Facility(name='facility-{}'.format(i), risk_cut_off=302500)
        db.session.add(f)
        v = Vessel(name='Heavy Lift Vessel',
                   abbr='HLV', day_rate=300000, mob_time=7, facility=f)
        db.session.add(v)
        for j in range(5):
            a = Area(name='area-{}-{}'.format(j, i),
                     equity_share=0.72, facility=f)
            db.session.add(a)
            for k in range(10):
                c = Component(ident='component-{}-{}-{}'.format(k, j, i),
                              category='Manifold', service_type='Production',
                              area=a)
                db.session.add(c)
                for m in range(5):
                    sc = SubComponent(ident='sc-{}-{}-{}-{}'.format(m, k, j, i),
                                      category='Chemical Injection Piping',
                                      component=c)

    db.session.commit()


@app.cli.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                print('Removing {}'.format(full_pathname))
                os.remove(full_pathname)

# @manager.command
# def deploy():
#     """Run deployment tasks."""
#     from flask_migrate import upgrade
#     # migrate database to latest revision
#     upgrade()
