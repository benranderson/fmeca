from flask import Flask, render_template, send_file, url_for, redirect, flash
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import main
from app import db
from ..models import Facility, Area, Component, SubComponent, Vessel, Consequence, \
    VesselTrip, FailureMode, FMECA, RBI
from .forms import FacilityForm, AreaForm, VesselForm, ComponentForm, \
    SubComponentForm, ConsequenceForm, VesselTripForm, FailureModeForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = FacilityForm()
    if form.validate_on_submit():
        facility = Facility(name=form.name.data,
                            remaining_life=form.remaining_life.data,
                            deferred_prod_cost=form.deferred_prod_cost.data,
                            risk_cut_off=form.risk_cut_off.data)
        db.session.add(facility)
        db.session.commit()
        flash('Facility added.')
        return redirect(url_for('.index'))
    facilities = Facility.query.all()
    return render_template('index.html', form=form, facilities=facilities)


@main.route('/failure_modes', methods=['GET'])
def failure_modes():
    failure_modes = FailureMode.query.all()
    return render_template('failure_mode.html', failure_modes=failure_modes)


@main.route('/facility/<int:id>', methods=['GET', 'POST'])
def facility(id):
    facility = Facility.query.get_or_404(id)
    a_form = AreaForm()
    if a_form.validate_on_submit():
        area = Area(facility=facility,
                    name=a_form.name.data,
                    equity_share=a_form.equity_share.data)
        db.session.add(area)
        db.session.commit()
        flash('Area added.')
        return redirect(url_for('.facility', id=id))
    v_form = VesselForm()
    if v_form.validate_on_submit():
        vessel = Vessel(facility=facility,
                        abbr=v_form.abbr.data,
                        name=v_form.name.data,
                        day_rate=v_form.day_rate.data,
                        mob_time=v_form.mob_time.data)
        db.session.add(vessel)
        db.session.commit()
        flash('Vessel added.')
        return redirect(url_for('.facility', id=id))
    return render_template('facility.html', a_form=a_form, v_form=v_form,
                           facility=facility)


@main.route('/area/<int:id>', methods=['GET', 'POST'])
def area(id):
    area = Area.query.get_or_404(id)
    form = ComponentForm()
    if form.validate_on_submit():
        component = Component(area=area,
                              ident=form.ident.data,
                              category=form.category.data,
                              service_type=form.service_type.data)
        db.session.add(component)
        db.session.commit()
        flash('Component added.')
        return redirect(url_for('.area', id=id))
    return render_template('area.html', form=form, area=area)


@main.route('/component/<int:id>', methods=['GET', 'POST'])
def component(id):
    component = Component.query.get_or_404(id)
    c_form = ConsequenceForm()
    if c_form.validate_on_submit():
        c = Consequence(component=component,
                        name=c_form.name.data,
                        mean_time_to_repair=c_form.mean_time_to_repair.data,
                        replacement_cost=c_form.replacement_cost.data,
                        deferred_prod_rate=c_form.deferred_prod_rate.data)
        db.session.add(c)
        db.session.commit()
        flash('Consequence added.')
        return redirect(url_for('.component', id=id))
    sc_form = SubComponentForm()
    if sc_form.validate_on_submit():
        sc = SubComponent(component=component,
                          ident=sc_form.ident.data,
                          category=sc_form.category.data)
        db.session.add(sc)
        db.session.commit()
        flash('Sub-Component added.')
        return redirect(url_for('.component', id=id))
    return render_template('component.html', c_form=c_form, sc_form=sc_form,
                           component=component)


@main.route('/consequence/<int:id>', methods=['GET', 'POST'])
def consequence(id):
    consequence = Consequence.query.get_or_404(id)
    form = VesselTripForm()
    form.vessel_id.choices = [(vessel.id, vessel.name)
                              for vessel in Vessel.query.filter_by(facility_id=consequence.component.area.facility.id).order_by('name')]
    if form.validate_on_submit():
        vt = VesselTrip(vessel_id=form.vessel_id.data,
                        active_repair_time=form.active_repair_time.data,
                        consequence=consequence)
        db.session.add(vt)
        db.session.commit()
        flash('Vessel Trip added.')
        return redirect(url_for('.consequence', id=id))
    return render_template('consequence.html', form=form,
                           consequence=consequence)


@main.route('/component/<int:id>/fmeca', methods=['GET', 'POST'])
def fmeca(id):
    component = Component.query.get_or_404(id)
    fmeca = FMECA(component=component)
    fmeca.create()
    flash('FMECA created.')
    return render_template('fmeca.html', fmeca=fmeca)


@main.route('/component/<int:id>/rbi', methods=['GET', 'POST'])
def rbi(id):
    fmeca = FMECA.query.filter_by(component_id=id).first()
    rbi = RBI(fmeca=fmeca, inspection_type='ROV Inspection')
    rbi.run()
    flash('RBI ran.')
    return render_template('rbi.html', rbi=rbi)


@main.route('/component/<int:id>/fig', methods=['GET'])
def fig(id):
    component = Component.query.get_or_404(id)
    risk = component.annual_risk
    interval = component.inspect_int
    ident = component.ident
    fig = draw_figure(ident, risk, interval)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


def draw_figure(ident, risk, interval):
    x = [0, interval, interval]
    y = [0, risk, 0]
    fig = plt.figure()
    # left, bottom, width, height (range 0 to 1)
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot([0, interval + 0.1 * interval], [risk, risk], color='r', ls='--',
              label='Risk Cut Off')
    axes.plot(x, y, color='blue', label='Calculated RBI')
    axes.set_xlim([0, interval + 0.1 * interval])
    axes.set_ylim([0, risk + 0.1 * risk])
    axes.legend()
    axes.grid(True)
    axes.set_xlabel('Inspection Interval [yrs]')
    axes.set_ylabel('Commercial Risk [£]')
    axes.set_title(ident)
    return fig
