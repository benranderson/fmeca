import math
import logging
from flask import url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from . import db, admin
from .exceptions import ValidationError


class Facility(db.Model):

    __tablename__ = 'facilities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    remaining_life = db.Column(db.Float)
    deferred_prod_cost = db.Column(db.Integer)
    risk_cut_off = db.Column(db.Integer)
    vessels = db.relationship('Vessel', backref='facility',
                              lazy='dynamic',
                              cascade='all, delete-orphan')
    areas = db.relationship('Area', backref='facility',
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    consequences = db.relationship('Consequence', backref='facility',
                                   lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def get_url(self):
        return url_for('api.get_facility', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'areas_url': url_for('api.get_facility_areas', id=self.id,
                                 _external=True),
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid facility: missing ' + e.args[0])
        return self


class Area(db.Model):

    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    equity_share = db.Column(db.Float, nullable=False)
    facility_id = db.Column(
        db.Integer, db.ForeignKey('facilities.id'), index=True)
    components = db.relationship('Component', backref='area',
                                 lazy='dynamic',
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def get_url(self):
        return url_for('api.get_area', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'facility_url': self.facility.get_url(),
            'name': self.name,
            'equity_share': self.equity_share,
            'components_url': url_for('api.get_area_components', id=self.id,
                                      _external=True),
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.equity_share = data['equity_share']
        except KeyError as e:
            raise ValidationError('Invalid area: missing ' + e.args[0])
        return self


class Component(db.Model):

    __tablename__ = 'components'

    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True, nullable=False)
    category = db.Column(db.String(64))
    service_type = db.Column(db.String(64))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), index=True)
    consequences = db.relationship(
        'Consequence', backref='component', lazy='dynamic',
        cascade='all, delete-orphan')
    subcomponents = db.relationship(
        'SubComponent', backref='component', lazy='dynamic',
        cascade='all, delete-orphan')
    fmeca = db.relationship("FMECA", backref='component', uselist=False)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def get_url(self):
        return url_for('api.get_component', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'area_url': self.area.get_url(),
            'ident': self.ident,
        }
        #     'subcomponents_url': url_for('api.get_component_subcomponents',
        #                                  id=self.id, _external=True),
        #     'consequences_url': url_for('api.get_component_consequences',
        #                                 id=self.id, _external=True),
        # }

    def import_data(self, data):
        try:
            self.ident = data['ident']
        except KeyError as e:
            raise ValidationError('Invalid component: missing ' + e.args[0])
        return self


class SubComponent(db.Model):

    __tablename__ = 'subcomponents'

    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64))
    category = db.Column(db.String(64))
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)
    failures = db.relationship('Failure', backref='subcomponent',
                               lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def get_url(self):
        return url_for('api.get_subcomponent', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'component_url': self.component.get_url(),
            'ident': self.ident,
            'category': self.category,
        }
        #     'failure_modes_url': url_for('api.get_subcomponent_failure_modes',
        #                                  id=self.id, _external=True),
        # }

    def import_data(self, data):
        try:
            self.ident = data['ident']
            self.category = data['category']
        except KeyError as e:
            raise ValidationError(
                'Invalid sub-component: missing ' + e.args[0])
        return self


class Consequence(db.Model):

    __tablename__ = 'consequences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    mean_time_to_repair = db.Column(db.Float)
    replacement_cost = db.Column(db.Integer)
    deferred_prod_rate = db.Column(db.Float)
    vessel_trips = db.relationship('VesselTrip', backref='consequence',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    failures = db.relationship('Failure', backref='consequence',
                               lazy='dynamic')
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)
    facility_id = db.Column(
        db.Integer, db.ForeignKey('facilities.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def get_url(self):
        return url_for('api.get_consequence', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'component_url': self.component.get_url(),
            'name': self.name,
            'mean_time_to_repair': self.mean_time_to_repair,
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.mean_time_to_repair = data['mean_time_to_repair']
        except KeyError as e:
            raise ValidationError(
                'Invalid consequence: missing ' + e.args[0])
        return self

    @property
    def gross_deferred_volume(self):
        return self.mean_time_to_repair * self.deferred_prod_rate

    @property
    def production_impact(self):
        facility = Facility.query.get_or_404(self.facility_id)
        return self.gross_deferred_volume * facility.deferred_prod_cost

    @property
    def equipment_cost(self):
        equipment_cost = self.replacement_cost
        for vessel_trip in self.vessel_trips:
            equipment_cost += vessel_trip.total_cost
        return self.component.area.equity_share * equipment_cost

    @property
    def total_cost(self):
        return self.production_impact + self.equipment_cost


class VesselTrip(db.Model):

    __tablename__ = 'vessel_trip'

    id = db.Column(db.Integer, primary_key=True)
    active_repair_time = db.Column(db.Float)
    vessel_id = db.Column(
        db.Integer, db.ForeignKey('vessels.id'), index=True)
    consequence_id = db.Column(
        db.Integer, db.ForeignKey('consequences.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.active_repair_time}>'

    @property
    def total_cost(self):
        vessel = Vessel.query.get_or_404(self.vessel_id)
        total_time = self.active_repair_time + vessel.mob_time
        return total_time * vessel.day_rate


class Vessel(db.Model):

    __tablename__ = 'vessels'

    id = db.Column(db.Integer, primary_key=True)
    abbr = db.Column(db.String(64))
    name = db.Column(db.String(128))
    day_rate = db.Column(db.Integer)
    mob_time = db.Column(db.Float)
    facility_id = db.Column(
        db.Integer, db.ForeignKey('facilities.id'), index=True)
    vessel_trips = db.relationship('VesselTrip', backref='vessel',
                                   lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.abbr}>'


class FMECA(db.Model):

    __tablename__ = 'fmecas'

    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'),
                             index=True)
    failures = db.relationship('Failure', backref='fmeca', lazy='dynamic')
    rbi = db.relationship("RBI", backref='fmeca', uselist=False)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    # TODO: Add caching
    def create(self):
        for subcomponent in self.component.subcomponents:

            for failure_mode in FailureMode.query.\
                    filter_by(subcomponent_category=subcomponent.category).all():

                try:
                    consequence = Consequence.query.\
                        filter_by(component=self.component,
                                  name=failure_mode.consequence_description).\
                        first()
                    if consequence is None:
                        raise ValidationError('No consequences found')
                except ValidationError as e:
                    logging.info('No consequences found')

                failure = Failure(fmeca=self,
                                  subcomponent=subcomponent,
                                  failure_mode=failure_mode,
                                  consequence=consequence)

                db.session.add(failure)
        db.session.commit()


class RBI(db.Model):

    __tablename__ = 'rbis'

    id = db.Column(db.Integer, primary_key=True)
    inspection_type = db.Column(db.String(64))
    fmeca_id = db.Column(db.Integer, db.ForeignKey('fmecas.id'), index=True)
    failures = db.relationship('Failure', backref='rbi', lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def run(self):
        for failure in self.fmeca.failures:
            if failure.failure_mode.inspection_type == self.inspection_type and not failure.failure_mode.time_dependant:
                failure.rbi = self
        db.session.commit()

    @property
    def risk(self):
        risk = 0
        for failure in self.fmeca.failures:
            if failure.rbi == self:
                risk += failure.risk
        return risk

    @property
    def inspection_interval(self):
        return self.fmeca.component.area.facility.risk_cut_off / self.risk


class FailureMode(db.Model):

    __tablename__ = 'failure_modes'

    id = db.Column(db.Integer, primary_key=True)
    subcomponent_category = db.Column(db.String(64))
    description = db.Column(db.String(128))
    time_dependant = db.Column(db.Boolean)
    mean_time_to_failure = db.Column(db.Float)
    detectable = db.Column(db.String(64))
    inspection_type = db.Column(db.String(64))
    consequence_description = db.Column(db.String(64))
    failures = db.relationship('Failure', backref='failure_mode',
                               lazy='dynamic')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.description}>'


class Failure(db.Model):

    __tablename__ = 'failures'

    id = db.Column(db.Integer, primary_key=True)
    subcomponent_id = db.Column(
        db.Integer, db.ForeignKey('subcomponents.id'), index=True)
    fmeca_id = db.Column(
        db.Integer, db.ForeignKey('fmecas.id'), index=True)
    failure_mode_id = db.Column(
        db.Integer, db.ForeignKey('failure_modes.id'), index=True)
    consequence_id = db.Column(
        db.Integer, db.ForeignKey('consequences.id'), index=True)
    rbi_id = db.Column(
        db.Integer, db.ForeignKey('rbis.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    @property
    def probability(self):
        """
        Return the annual probability of failure of the failure mode
        """

        # apply rbi filters
        if not self.failure_mode.time_dependant:
            if self.failure_mode.detectable == 'Lagging':
                multiplier = 0.5
            else:
                multiplier = 1
        else:
            multiplier = 0

        try:
            failure_rate = 1 / self.failure_mode.mean_time_to_failure
            t = 1
            return multiplier * (1 - math.exp(-failure_rate * t))
        except ZeroDivisionError as e:
            raise e

    @property
    def total_cost(self):
        """
        Return the total cost of the failure.
        """
        if self.consequence:
            return self.consequence.total_cost
        else:
            return 0

    @property
    def risk(self):
        """
        Return the annual commercial risk of the failure.
        """
        return self.probability * self.total_cost


class MyView(BaseView):
    @expose('/')
    def index(self):
        return 'Hello World!'


admin.add_view(ModelView(Facility, db.session))
admin.add_view(ModelView(Area, db.session))
admin.add_view(ModelView(Component, db.session))
admin.add_view(ModelView(SubComponent, db.session))
admin.add_view(ModelView(FailureMode, db.session))
admin.add_view(ModelView(Consequence, db.session))
admin.add_view(ModelView(Vessel, db.session))
admin.add_view(ModelView(VesselTrip, db.session))
admin.add_view(ModelView(Failure, db.session))
