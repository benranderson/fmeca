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
                                    lazy='dynamic')

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


admin.add_view(ModelView(Component, db.session))
admin.add_view(ModelView(SubComponent, db.session))
