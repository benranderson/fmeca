from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DecimalField, IntegerField, \
    SelectField, FormField, FieldList, BooleanField
from wtforms.validators import Required


class FacilityForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    remaining_life = DecimalField('Remaining Life [yrs]')
    deferred_prod_cost = IntegerField('Deferred Production Cost [£/barrel]')
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
    name = SelectField('Name')
    mean_time_to_repair = DecimalField('Mean Time to Repair [days]')
    replacement_cost = IntegerField('Replacement Cost [£]')
    deferred_prod_rate = DecimalField('Deferred Production Rate [barrels/day]')
    submit = SubmitField('Submit')


class SubComponentForm(FlaskForm):
    ident = StringField('Identifier')
    # TODO: make selectfield
    category = SelectField('Category')
    submit = SubmitField('Submit')


class MultiSubComponentForm(FlaskForm):
    subcomponents = FieldList(
        FormField(SubComponentForm), min_entries=7, max_entries=7)
    submit = SubmitField('Submit')


class FailureModeForm(FlaskForm):
    subcomponent_category = StringField(
        'Subcomponent Category', validators=[Required()])
    description = StringField('Description')
    time_dependant = BooleanField('Time Dependant')
    mean_time_to_failure = DecimalField('Mean Time to Failure (MTTF) [yrs]')
    detectable = SelectField('Detectable by Inspection', choices=[
        ('Lagging', 'Lagging'),
        ('Leading', 'Leading'),
        ('Not Detectable', 'Not Detectable'),
    ])
    inspection_type = SelectField('Inspection Type', choices=[
        ('ROV Inspection', 'ROV Inspection'),
        ('Diver Inspection', 'Diver Inspection'),
    ])
    consequence_description = SelectField('Global Consequence', choices=[
        ('Loss of Redundancy', 'Loss of Redundancy'),
        ('Change in Operation', 'Change in Operation'),
        ('Minor Intervention', 'Minor Intervention'),
        ('Major Intervention', 'Major Intervention'),
        ('Planned Intervention', 'Planned Intervention'),
    ])
    submit = SubmitField('Submit')


class VesselForm(FlaskForm):
    abbr = StringField('Abbreviation', validators=[Required()])
    name = StringField('Name')
    day_rate = IntegerField('Day Rate [$/day]', validators=[Required()])
    mob_time = DecimalField('Mobilisation Time [days]')
    submit1 = SubmitField('Submit')


class VesselTripForm(FlaskForm):
    vessel_id = SelectField('Vessel', coerce=int)
    active_repair_time = DecimalField('Active Repair Time [days]',
                                      validators=[Required()])
    submit = SubmitField('Submit')
