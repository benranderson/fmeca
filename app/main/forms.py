from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DecimalField, IntegerField, \
    SelectField
from wtforms.validators import Required


class FacilityForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Submit')


class ComponentForm(FlaskForm):
    ident = StringField('Identifier', validators=[Required()])
    annual_risk = IntegerField('Commercial Risk [£]')
    inspect_int = DecimalField('Inspection Interval [yrs]')
    submit = SubmitField('Submit')


class SubComponentForm(FlaskForm):
    ident = StringField('Identifier', validators=[Required()])
    category = StringField('Category', validators=[Required()])
    submit = SubmitField('Submit')


class FailureModeForm(FlaskForm):
    description = StringField('Description', validators=[Required()])
    mttf = DecimalField('Mean Time to Failure (MTTF) [yrs]')
    consequence_id = SelectField('Global Consequence', coerce=int)
    submit = SubmitField('Submit')


class ConsequenceForm(FlaskForm):
    name = SelectField('Name', validators=[Required()], choices=[
                       ('change', 'Change in operation'),
                       ('loss', 'Loss of redundancy'),
                       ('major', 'Major Intervention'),
                       ('minor', 'Minor Intervention'),
                       ('planned', 'Planned Intervention'),
                       ])
    hydro_release = DecimalField('Hydrocarbon Release [Barrels]')
    submit = SubmitField('Submit')


class VesselForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    abbr = StringField('Abbreviation', validators=[Required()])
    rate = IntegerField('Day Rate [$/day]', validators=[Required()])
    mob_time = DecimalField('Mobilisation Time [days]')
    submit = SubmitField('Submit')


class VesselTripForm(FlaskForm):
    active_time = DecimalField('Active Time', validators=[Required()])
    vessel_id = SelectField('Vessel', coerce=int)
    submit = SubmitField('Submit')
