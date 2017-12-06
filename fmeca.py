import os
import click
import json
# import subprocess
# import sys

from flask_migrate import Migrate, upgrade

from app import create_app, db
from app.models import FailureMode, Facility, Area, Component, Consequence, \
    SubComponent, Vessel, VesselTrip

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
def load_fms():
    """Seeds the database."""

    fms_json = json.load(open('fms.json'))
    for sc in fms_json:
        for fm_json in fms_json[sc]:
            fm = FailureMode(subcomponent_category=sc,
                             description=fm_json,
                             time_dependant=fms_json[sc][fm_json]["time_dependent"],
                             mean_time_to_failure=fms_json[sc][fm_json]["mean_time_to_failure"],
                             detectable=fms_json[sc][fm_json]["detectable"],
                             inspection_type=fms_json[sc][fm_json]["inspection_type"],
                             consequence_description=fms_json[sc][fm_json]["consequence_description"])
            db.session.add(fm)
    db.session.commit()


@app.cli.command()
def example():
    import csv

    f = Facility(name='Foinaven', risk_cut_off=302500,
                 deferred_prod_cost=18)
    db.session.add(f)

    vessels_file = open('inputs/vessels.csv')
    vessels = csv.reader(vessels_file)

    for vessel in vessels:
        v = Vessel(name=vessel[0], abbr=vessel[1], day_rate=vessel[2],
                   mob_time=vessel[3], facility=f)
        db.session.add(v)

    a = Area(name='DC1', equity_share=0.72, facility=f)
    db.session.add(a)

    c = Component(ident='P11', category='Tree',
                  service_type='Production', area=a)
    db.session.add(a)

    consequences_file = open('inputs/consequences.csv')
    consequences = csv.reader(consequences_file)

    for consequence in consequences:
        cons = Consequence(name=consequence[0], mean_time_to_repair=consequence[10],
                           replacement_cost=consequence[11],
                           deferred_prod_rate=consequence[13],
                           component=c, facility=f)
        v1 = Vessel.query.filter_by(name=consequence[2]).first()
        vt1 = VesselTrip(vessel=v1, active_repair_time=consequence[5],
                         consequence=cons)
        v2 = Vessel.query.filter_by(name=consequence[6]).first()
        vt2 = VesselTrip(vessel=v2, active_repair_time=consequence[9],
                         consequence=cons)
        db.session.add(cons)

    subcomponents_file = open('inputs/subcomponents.csv')
    subcomponents = csv.reader(subcomponents_file)

    for subcomponent in subcomponents:
        s = SubComponent(category=subcomponent[0], ident=subcomponent[1],
                         component=c)
        db.session.add(s)

    db.session.commit()


@app.cli.command()
def seeddb():
    """Seeds the database."""

    fms_json = json.load(open('fms.json'))
    for sc in fms_json:
        for fm_json in fms_json[sc]:
            fm = FailureMode(subcomponent_category=sc,
                             description=fm_json,
                             time_dependant=fms_json[sc][fm_json]["time_dependent"],
                             mean_time_to_failure=fms_json[sc][fm_json]["mean_time_to_failure"],
                             detectable=fms_json[sc][fm_json]["detectable"],
                             inspection_type=fms_json[sc][fm_json]["inspection_type"],
                             consequence_description=fms_json[sc][fm_json]["consequence_description"])
            db.session.add(fm)

    for i in range(5):
        f = Facility(name='facility-{}'.format(i), risk_cut_off=302500,
                     deferred_prod_cost=18)
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

                # consequences
                cons1 = Consequence(name='Change in Operation',
                                    mean_time_to_repair=60,
                                    replacement_cost=100000,
                                    deferred_prod_rate=1000,
                                    component=c,
                                    facility=f)
                cons2 = Consequence(name='Loss of Redundancy',
                                    mean_time_to_repair=60,
                                    replacement_cost=100000,
                                    deferred_prod_rate=1000,
                                    component=c,
                                    facility=f)
                cons3 = Consequence(name='Major Intervention',
                                    mean_time_to_repair=60,
                                    replacement_cost=100000,
                                    deferred_prod_rate=1000,
                                    component=c,
                                    facility=f)
                cons4 = Consequence(name='Minor Intervention',
                                    mean_time_to_repair=60,
                                    replacement_cost=100000,
                                    deferred_prod_rate=1000,
                                    component=c,
                                    facility=f)
                cons5 = Consequence(name='Planned Intervention',
                                    mean_time_to_repair=60,
                                    replacement_cost=100000,
                                    deferred_prod_rate=1000,
                                    component=c,
                                    facility=f)
                db.session.add_all([cons1, cons2, cons3, cons4, cons5])

                for m in range(5):
                    sc = SubComponent(ident='sc-{}-{}-{}-{}'.format(m, k, j, i),
                                      category='Acoustic Sand Detector',
                                      component=c)
                    db.session.add(sc)

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


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
