from flask import Flask, render_template, send_file, url_for, redirect, flash
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from . import main
from app import db
from ..models import Component, Vessel, Consequence
from .forms import ComponentForm, ConsequenceForm


@main.route('/')
def index():
    components = Component.query.all()
    return render_template('index.html', components=components)


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


@main.route('/component/<int:id>/consequence/add', methods=['GET', 'POST'])
def consequence_add(id):
    component = Component.query.get_or_404(id)
    form = ConsequenceForm()
    form.vessels.choices = [(vessel.id, vessel.name)
                            for vessel in Vessel.query.order_by('name')]
    if form.validate_on_submit():
        consequence = Consequence(tag=form.name.data, size=form.hydro_release.data,
                                  vessel=form.vessel.data)
        consequence.component_id = component.id
        db.session.add(consequence)
        flash('Global Consequence added.')
        return redirect(url_for('.component', id=component.id))
    heading = "Add a new Global Consequence"
    return render_template('form.html', form=form, heading=heading)


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
    axes.plot([0, interval], [risk, risk], color='r', label='Risk')
    axes.plot(x, y, color='g', ls='--', label='RBI')
    axes.set_xlim([0, interval + 0.1 * interval])
    axes.set_ylim([0, risk + 0.1 * risk])
    axes.legend()
    axes.grid(True)
    axes.set_xlabel('Inspection Interval [yrs]')
    axes.set_ylabel('Commercial Risk [£]')
    axes.set_title(ident)
    return fig
