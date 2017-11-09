from flask import Flask, render_template, send_file, url_for, redirect, flash
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import main
from app import db
from ..models import Component, Vessel, Consequence, VesselTrip
from .forms import VesselForm, ComponentForm, ConsequenceForm, VesselTripForm


@main.route('/', methods=['GET'])
def index():
    components = Component.query.all()
    vessels = Vessel.query.all()
    return render_template('index.html', components=components, vessels=vessels)


@main.route('/vessel/add', methods=['GET', 'POST'])
def vessel_add():
    form = VesselForm()
    if form.validate_on_submit():
        vessel = Vessel(name=form.name.data,
                        abbr=form.abbr.data,
                        rate=form.rate.data,
                        mob_time=form.mob_time.data)
        db.session.add(vessel)
        flash('Vessel added.')
        return redirect(url_for('.index'))
    heading = "Add a new Vessel"
    return render_template('form.html', form=form, heading=heading)


@main.route('/component/<int:id>', methods=['GET', 'POST'])
def component(id):
    component = Component.query.get_or_404(id)
    return render_template("component.html", component=component)


@main.route('/component/add', methods=['GET', 'POST'])
def component_add():
    form = ComponentForm()
    if form.validate_on_submit():
        component = Component(ident=form.ident.data,
                              annual_risk=form.annual_risk.data,
                              inspect_int=form.inspect_int.data)
        db.session.add(component)
        flash('Component added.')
        return redirect(url_for('.index'))
    heading = "Add a new Component"
    return render_template('form.html', form=form, heading=heading)


@main.route('/component/<int:component_id>/consequence/<int:consequence_id>', methods=['GET', 'POST'])
def consequence(component_id, consequence_id):
    consequence = Consequence.query.get_or_404(consequence_id)
    return render_template("consequence.html", consequence=consequence,
                           component_id=component_id)


@main.route('/component/<int:id>/consequence/add', methods=['GET', 'POST'])
def consequence_add(id):
    component = Component.query.get_or_404(id)
    form = ConsequenceForm()
    if form.validate_on_submit():
        consequence = Consequence(name=form.name.data,
                                  hydro_release=form.hydro_release.data)
        consequence.component_id = component.id
        db.session.add(consequence)
        flash('Global Consequence added.')
        return redirect(url_for('.component', id=component.id))
    heading = "Add a new Global Consequence"
    return render_template('form.html', form=form, heading=heading)


@main.route('/component/<int:component_id>/consequence/<int:consequence_id>/vessel_trip/add', methods=['GET', 'POST'])
def vessel_trip_add(component_id, consequence_id):
    consequence = Consequence.query.get_or_404(consequence_id)
    form = VesselTripForm()
    form.vessel_id.choices = [(vessel.id, vessel.name)
                              for vessel in Vessel.query.order_by('name')]
    component = Component.query.get_or_404(component_id)
    if form.validate_on_submit():
        vessel_trip = VesselTrip(active_time=form.active_time.data,
                                 vessel_id=form.vessel_id.data)
        vessel_trip.consequence_id = consequence.id
        db.session.add(vessel_trip)
        flash('Vessel Trip added.')
        return redirect(url_for('.component', id=component_id))
    heading = "Add a new Vessel Trip"
    return render_template('form.html', form=form, heading=heading)


# @main.route('/component/<int:id>/subcomponent/add', methods=['GET', 'POST'])
# def consequence_add(id):
#     component = Component.query.get_or_404(id)
#     form = ConsequenceForm()
#     form.vessel.choices = [(vessel.id, vessel.name)
#                            for vessel in Vessel.query.order_by('name')]
#     if form.validate_on_submit():
#         consequence = Consequence(name=form.name.data,
#                                   hydro_release=form.hydro_release.data)
#         vessel = Vessel.query.get_or_404(form.vessel.data)
#         consequence.vessel.append(vessel)
#         consequence.component_id = component.id
#         db.session.add(consequence)
#         flash('Global Consequence added.')
#         return redirect(url_for('.component', id=component.id))
#     heading = "Add a new Global Consequence"
#     return render_template('form.html', form=form, heading=heading)


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
