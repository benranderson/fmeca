from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DecimalField, IntegerField, \
    SelectField
from wtforms.validators import Required


class FacilityForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    remaining_life = DecimalField('Remaining Life [yrs]')
    deferred_prod_cost = IntegerField('Deferred Production Cost [£]')
    risk_cut_off = IntegerField('Risk Cut Off [£]')
    submit = SubmitField('Submit')


class AreaForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    equity_share = DecimalField('Equity Share')
    submit = SubmitField('Submit')


class ComponentForm(FlaskForm):
    ident = StringField('Identifier', validators=[Required()])
    category = StringField('Category')
    service_type = SelectField('Service Type', validators=[Required()], choices=[
        ('ge', 'Gas Export'),
        ('gi', 'Gas Injection'),
        ('gl', 'Gas Lift'),
        ('prod', 'Production'),
        ('service', 'Service'),
        ('wi', 'Water Injection'),
        ('others', 'Others (Combined)'),
    ])
    submit = SubmitField('Submit')


class ConsequenceForm(FlaskForm):
    name = SelectField('Name', validators=[Required()], choices=[
                       ('change', 'Change in operation'),
                       ('loss', 'Loss of redundancy'),
                       ('major', 'Major Intervention'),
                       ('minor', 'Minor Intervention'),
                       ('planned', 'Planned Intervention'),
                       ])
    mean_time_to_repair = DecimalField('Mean Time to Repair [days]')
    replacement_cost = IntegerField('Replacement Cost [£]')
    deferred_prod_rate = DecimalField('Deferred Production Rate [barrels/day]')
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


class VesselForm(FlaskForm):
    abbr = StringField('Abbreviation', validators=[Required()])
    name = StringField('Name')
    day_rate = IntegerField('Day Rate [$/day]', validators=[Required()])
    mob_time = DecimalField('Mobilisation Time [days]')
    submit = SubmitField('Submit')


class VesselTripForm(FlaskForm):
    vessel_id = SelectField('Vessel', coerce=int)
    active_repair_time = DecimalField('Active Repair Time [days]',
                                      validators=[Required()])
    submit = SubmitField('Submit')
