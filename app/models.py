from flask import url_for
from flask_admin.contrib.sqla import ModelView
from . import db, admin
from .exceptions import ValidationError


class Component(db.Model):

    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True)
    annual_risk = db.Column(db.Integer)
    inspect_int = db.Column(db.Float)
    subcomponents = db.relationship('SubComponent', backref='component',
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')
    consequences = db.relationship(
        'Consequence', backref='component', lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return '<Component {}>'.format(self.ident)

    def get_url(self):
        return url_for('api.get_component', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'ident': self.ident,
        }

    def import_data(self, data):
        try:
            self.ident = data['ident']
        except KeyError as e:
            raise ValidationError('Invalid valve: missing ' + e.args[0])
        return self


class SubComponent(db.Model):

    __tablename__ = 'subcomponents'

    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)

    def __repr__(self):
        return '<SubComponent {}>'.format(self.ident)

    def get_url(self):
        return url_for('api.get_subcomponent', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'ident': self.ident,
            'category': self.category,
        }

    def import_data(self, data):
        try:
            self.ident = data['ident']
            self.category = data['category']
        except KeyError as e:
            raise ValidationError('Invalid valve: missing ' + e.args[0])
        return self


class Consequence(db.Model):

    __tablename__ = 'consequences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    hydro_release = db.Column(db.Float)
    vessel_trips = db.relationship('VesselTrip', backref='consequence',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)


class Vessel(db.Model):

    __tablename__ = 'vessels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    abbr = db.Column(db.String(64), unique=True)
    rate = db.Column(db.Integer)
    mob_time = db.Column(db.Float)
    vessel_trips = db.relationship('VesselTrip', backref='vessel',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')


class VesselTrip(db.Model):

    __tablename__ = 'vessel_trip'

    id = db.Column(db.Integer, primary_key=True)
    active_time = db.Column(db.Float)
    vessel_id = db.Column(
        db.Integer, db.ForeignKey('vessels.id'), index=True)
    consequence_id = db.Column(
        db.Integer, db.ForeignKey('consequences.id'), index=True)

    @property
    def total_time(self):
        vessel = Vessel.query.get_or_404(self.vessel_id)
        return self.active_time + vessel.mob_time


class FailureMode(db.Model):

    __tablename__ = 'failure_modes'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    failure_prob = db.Column(db.Float)
    cost = db.Column(db.Integer)
    subcomponent_id = db.Column(
        db.Integer, db.ForeignKey('subcomponents.id'), index=True)


admin.add_view(ModelView(Component, db.session))
admin.add_view(ModelView(SubComponent, db.session))
admin.add_view(ModelView(Consequence, db.session))
admin.add_view(ModelView(Vessel, db.session))
admin.add_view(ModelView(VesselTrip, db.session))
