from . import db


class Component(db.Model):
    
    __tablename__ = 'components'
    
    id = db.Column(db.Integer, primary_key=True)
    ident = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Component {}>'.format(self.ident)