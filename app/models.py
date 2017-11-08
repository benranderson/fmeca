from flask import url_for
from . import db
from .exceptions import ValidationError


class Component(db.Model):
    
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Component {}>'.format(self.ident)
    
    def get_url(self):
        return url_for('api.get_component', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'ident': self.tag,
        }

    def import_data(self, data):
        try:
            self.ident = data['ident']
        except KeyError as e:
            raise ValidationError('Invalid valve: missing ' + e.args[0])
        return self