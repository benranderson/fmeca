from flask import url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from . import db, admin
from .exceptions import ValidationError


class Facility(db.Model):
    __tablename__ = 'facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    areas = db.relationship('Area', backref='facility',
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    vessels = db.relationship('Vessel', backref='facility',
                              lazy='dynamic',
                              cascade='all, delete-orphan')

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
    remaining_life = db.Column(db.Float, nullable=False)
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
            'remaining_life': self.remaining_life,
            'equity_share': self.equity_share,
            'components_url': url_for('api.get_area_components', id=self.id,
                                      _external=True),
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.remaining_life = data['remaining_life']
            self.equity_share = data['equity_share']
        except KeyError as e:
            raise ValidationError('Invalid area: missing ' + e.args[0])
        return self


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True, nullable=False)
    annual_risk = db.Column(db.Integer)
    inspect_int = db.Column(db.Float)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), index=True)
    subcomponents = db.relationship('SubComponent', backref='component',
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')
    consequences = db.relationship(
        'Consequence', backref='component', lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def get_url(self):
        return url_for('api.get_component', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'area_url': self.area.get_url(),
            'ident': self.ident,
            'subcomponents_url': url_for('api.get_component_subcomponents',
                                         id=self.id, _external=True),
        }

    def import_data(self, data):
        try:
            self.ident = data['ident']
        except KeyError as e:
            raise ValidationError('Invalid component: missing ' + e.args[0])
        return self

    @property
    def commercial_risk(self):
        pass


<< << << < HEAD
# if self.subcomponents:
#     risk = 0
#     for subcomponent in self.subcomponents:
#         risk += subcomponent.risk
#     return risk
# else:
#     return None
== == == =
>>>>>> > master


class SubComponent(db.Model):
    __tablename__ = 'subcomponents'
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True)
    category = db.Column(db.String(64))
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)
    failure_modes = db.relationship('FailureMode', backref='subcomponent',
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
            'failure_modes_url': url_for('api.get_subcomponent_failure_modes',
                                         id=self.id, _external=True),
        }

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
    hydro_release = db.Column(db.Float)
    vessel_trips = db.relationship('VesselTrip', backref='consequence',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')
    failure_modes = db.relationship('FailureMode', backref='consequence',
                                    lazy='dynamic')
    component_id = db.Column(
        db.Integer, db.ForeignKey('components.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Vessel(db.Model):
    __tablename__ = 'vessels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    abbr = db.Column(db.String(64), unique=True)
    rate = db.Column(db.Integer)
    mob_time = db.Column(db.Float)
    facility_id = db.Column(
        db.Integer, db.ForeignKey('facilities.id'), index=True)
    vessel_trips = db.relationship('VesselTrip', backref='vessel',
                                   lazy='dynamic',
                                   cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.abbr}>'


class VesselTrip(db.Model):
    __tablename__ = 'vessel_trip'
    id = db.Column(db.Integer, primary_key=True)
    active_time = db.Column(db.Float)
    vessel_id = db.Column(
        db.Integer, db.ForeignKey('vessels.id'), index=True)
    consequence_id = db.Column(
        db.Integer, db.ForeignKey('consequences.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.active_time}>'

    @property
    def total_time(self):
        vessel = Vessel.query.get_or_404(self.vessel_id)
        return self.active_time + vessel.mob_time


class FailureMode(db.Model):
    __tablename__ = 'failure_modes'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))
    mttf = db.Column(db.Float)
    subcomponent_id = db.Column(
        db.Integer, db.ForeignKey('subcomponents.id'), index=True)
    consequence_id = db.Column(
        db.Integer, db.ForeignKey('consequences.id'), index=True)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.description}>'

    def get_url(self):
        return url_for('api.get_failure_mode', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'subcomponent_id': self.subcomponent.get_url(),
            'consequence_id': self.consequence.get_url(),
            'description': self.description,
            'mttf': self.mttf,
        }

    def import_data(self, data):
        try:
            self.description = data['description']
            self.mttf = data['mttf']
        except KeyError as e:
            raise ValidationError('Invalid failure mode: missing ' + e.args[0])
        return self

    def __init__(self, c):
        self.failure_causes = []
        self.local_consequences = []
        self.global_consequences = []
        self.failure_rate = c["Failure Rate (fpmh)"]
        self.prevention_barriers = c["Prevention barriers"]
        self.maintainance = c["Do maintenance repair/modify op procedure"]
        self.spare_part_replacement = c["Spare part replacement"]
        self.whole_system_replacement = c["Whole system replacement"]
        self.oreda_ref = c["OREDA tag/OREDA Volume/page"]
        self.prevention_barriers = c["Possible Prevention Barriers"]
        self.mitigation_barriers = c["Possible Mitigation Barriers"]
        self.failure_mode_bowtie = c["Bow Tie as per failure mode"]
        self.bow_tie_threat = c["Bow tie threat/branch"]


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

admin.add_view(MyView(name='Test View', menu_icon_type='glyph',
                      menu_icon_value='glyphicon-home'))
