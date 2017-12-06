import csv
from app import db
from app.models import Facility, Vessel, Area, Component, Consequence, \
    VesselTrip, SubComponent

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

c = Component(ident='P11', category='Tree', service_type='Production', area=a)
db.session.add(a)

consequences_file = open('inputs/consequences.csv')
consequences = csv.reader(consequences_file)

for consequence in consequences:
    cons = Consequence(name=consequence[0], mean_time_to_repair=consequence[10],
                       replacement_cost=consequence[11],
                       deferred_prod_rate=consequence[14],
                       component=c, facility=f)
    v1 = Vessel.query.filter_by(name=consequence[2]).first()
    vt1 = VesselTrip(vessel=v1, active_repair_time=consequence[5],
                     consequence=cons)
    v2 = Vessel.query.filter_by(name=consequence[6]).first()
    vt2 = VesselTrip(vessel=v2, active_repair_time=consequence[9],
                     consequence=cons)
    db.session.add(cons)


subcomponents_file = open('inputs/p11.csv')
subcomponents = csv.reader(subcomponents_file)

for subcomponent in subcomponents:
    s = SubComponent(ident=subcomponent[1], category=subcomponent[0],
                     component=c)
    db.session.add(s)

db.session.commit()
