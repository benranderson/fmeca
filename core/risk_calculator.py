import copy
import json
from collections import namedtuple
import math
from exceptions import ValidationError
from fmeca import FMECA
from rbi import RBI

# load input data
FAILURE_MODES = json.load(open('core/inputs/failure_modes.json'))
AREA = json.load(open('core/inputs/area1.json'))

from flask import Flask, jsonify, request


class RiskCalculator:

    def __init__(self, filename=''):
        if filename == '':
            self.facilities = []
            self.filename = ''
        else:
            self.facilities = self._read_existing_rc(filename)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    def import_data(self, data):

        try:
            self.name = data['name']
            self.remaining_life = data['remaining_life']
            self.equity_share = data['equity_share']
        except KeyError as e:
            raise ValidationError('Invalid area: missing ' + e.args[0])
        return self

        for a in data:
            if a not in self.__dict__:
                raise KeyError(f'{type(self)} does not contain attriute {a}')
            if type(data[a]) == type({}):
                c = self._format_class_name(a)
                if type(getattr(self, a)) == type({}):
                    for l in data[a].keys():
                        try:
                            o = eval(c)(l)
                        except:
                            raise KeyError(f'{a} does not map to valid class \
                                           name.')
                        o.import_data(data[a][l])
                        getattr(self, a)[l] = o
                elif type(getattr(self, a)) == type([]):
                    for l in data[a]:
                        o = eval(c)(l)
                        o.import_data(data[a][l])
                        getattr(self, a).append(o)
                else:
                    raise TypeError(f'{type(getattr(self, a))} is not \
                                    iterable')
            else:
                setattr(self, a, data[a])

    def _read_existing_rc(self, filename):
        # TODO: write function to open existing json file from previous
        #       RiskCalculator and create model in memory
        pass

    def save(self, filename=''):
        if filename == self.filename == '':
            raise ValueError('Enter valid filename for save.')
        else:
            if not '.json' in self.filename:
                self.filename = self.filename + '.json'
            with open(self.filename, 'w') as o:
                json.dump(self.export_data(), o)

    def add_facility(self, name, operator):
        self.facilities.append(Facility(name, operator))

    def export_data(self):
        data = {}
        data['filename'] = self.filename
        data['facilities'] = {k: v for k, v in
                              [f.ident, f.export_data() for f in self.facilites]}
        return data


class Facility():

    def __init__(self, name, operator):
        self.ident = self.name = name
        self.operator = operator
        self.vessels = {}
        self.areas = []
        # read in default lists i.e. FAILUREMODES above

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def export_data(self):
        return {
            'name': self.name,
            'operator': self.operator,
            'vessels': [self.vessels[vessel].export_data() for vessel in self.vessels]
        }

    def import_data(self, data):
        pass

    def add_area(self, area):
        self.areas.append(area)

    def read_vessels(self, json_filename):
        with open(json_filename, 'r') as j:
            d = json.load(j)
            self.vessels = d["Vessels"]

    def export_data(self):
        data = {}
        data['ident'] = data['name'] = self.name
        data['operator'] = self.operator
        data['vessels'] = self.vessels
        data['areas'] = {k: v for k, v in
                         [a.ident, a.export_data() for a in self.areas]}
        return data


class Vessel:

    def __init__(self, name, abbr, day_rate, mob_time):
        self.name = name
        self.abbr = abbr
        self.day_rate = day_rate
        self.mob_time = mob_time

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.abbr}>'

    def export_data(self):
        return {
            'name': self.name,
            'abbr': self.abbr,
            'day_rate': self.day_rate,
            'mob_time': self.mob_time
        }


class Area:

    def __init__(self, name):
        self.ident = self.name = name
        self.components = []
        self.financial_data = {}

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def add_component(self, component):
        self.components.append(component)

    def read_components(self, json_filename):
        with open(json_filename, 'r') as j:
            # TODO: define components.json and map to component objects
            pass

    def read_financial_data(self, json_filename):
        with open(json_filename, 'r') as j:
            self.financial_data = json.load(j)

    def export_data(self):
        data = {}
        data['ident'] = data['name'] = self.name
        data['components'] = {k: v for k, v in
                              [c.ident, c.export_data() for c in self.components]}
        data['financial_data'] = self.financial_data
        return data


class Consequence:
    def __init__(self, name):
        self.ident = self.name = name
        # self.mttr = mttr
        self.vessel_trips = []

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def add_vessel_trip(self, vessel_trip):
        self.vessel_trips.append(vessel_trip)

    def export_data(self):
        data = {}
        data['ident'] = data['name'] = self.name
        data['vessel trips'] = {k: v for k, v in
                                [vt.ident, vt.export_data() for vt in self.vessel_trips]}
        return data


class Component:
    def __init__(self, ident):
        self.ident = ident
        self.fmeca = None
        self.rbi = None
        self.subcomponents = []
        self.consequences = {}
        self._total_risk = None

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def add_subcomponent(self, description, ident):
        # provide subcomponent with component consequence dict
        subcomponent = SubComponent(description, ident, self.consequences)
        self.subcomponents.append(subcomponent)

    def add_consequence(self, name, cost):
        self.consequences[name] = cost

    @property
    def total_risk(self):
        if self._total_risk is None:
            return 'Run component RBI.'
        else:
            return self._total_risk

    def run_rbi(self, inspection_type='ROV Inspection'):
        # run calculation if first time
        if self._total_risk is None:
            print('Calculating total component risk.')
            # self.subcomponents_calculated = copy.deepcopy(self.subcomponents)
            self._total_risk = 0
            for subcomponent in self.subcomponents:
                failures = subcomponent.failures
                for failure in failures:
                    if failure.inspection_type == inspection_type and not failure.time_dependant:
                        if failure.detectable == 'Lagging':
                            self._total_risk += 0.5 * failure.risk
                        else:
                            self._total_risk += failure.risk
        return self._total_risk

    def export_data(self):
        data = {}
        data['ident'] = self.ident
        data['fmeca'] = self.fmeca.export_data() if self.fmeca else None
        data['rbi'] = self.rbi.export_data() if self.rbi else None
        data['subcomponents'] = {k: v for k, v in
                                 [sc.ident, sc.export_data() for sc in self.subcomponents]}
        data['consequences'] = self.consequences
        data['total risk'] = self._total_risk
        return data

    def compile_rbi(self, fmeca):
        self.rbi = RBI(fmeca)

    def compile_base_fmeca(self):
        self.fmeca = FMECA(self.subcomponents)


class SubComponent:
    def __init__(self, description, ident, consequences=None):
        self.description = description
        self.ident = ident
        self.consequences = consequences
        self._failures = []
        self.failure_modes = FAILURE_MODES[self.description]['Failure Modes']

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    @property
    def failures(self):
        # run calculation if first time
        if len(self._failures) == 0:
            for failure_mode in self.failure_modes:
                f = Failure(failure_mode, self.description, self.consequences)
                self._failures.append(f)
        return self._failures

    def export_data(self):
        data = {}
        data['ident'] = self.ident
        data['description'] = self.description
        data['consequences'] = self.consequences if self.consequences else None
        data['failures'] = {k: v for k, v in
                            [f.ident, f.export_data() for f in self.failures]}
        data['failure modes'] = self.failure_modes
        return data


class Failure:
    def __init__(self, description, subcomponent, consequences=None):
        self.ident = self.description = description
        self.consequences = consequences
        self.consequence = FAILURE_MODES[subcomponent]['Failure Modes'][self.description]['Global Consequences']
        self.cost = self.consequences[self.consequence]
        self.mttf = FAILURE_MODES[subcomponent]['Failure Modes'][self.description]['BP Ored MTTF']

        if FAILURE_MODES[subcomponent]['Failure Modes'][self.description]['Random/Time Dependant'] == 'T.D.':
            self.time_dependant = True
        else:
            self.time_dependant = False

        self.detectable = FAILURE_MODES[subcomponent]['Failure Modes'][self.description]['Detectable by Inspection']
        self.inspection_type = FAILURE_MODES[subcomponent]['Failure Modes'][self.description]['Type of Inspection']

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.description}>'

    @property
    def probability(self):
        """
        Return the annual probability of failure of the failure mode
        """
        failure_rate = 1 / self.mttf
        t = 1
        return 1 - math.exp(-failure_rate * t)

    @property
    def risk(self):
        """
        Return the annual commercial risk of the failure mode
        """
        return self.probability * self.cost

    def export_data(self):
        data = {}
        data['ident'] = self.ident
        data['description'] = self.description
        data['consequences'] = self.consequences if self.consequences else None
        data['consequence'] = self.consequence
        data['cost'] = self.cost
        data['mttf'] = self.mttf
        return data


app = Flask(__name__)


# Instantiate the Facility Risk Class
risk_calculator = RiskCalculator('core/inputs/facilites.json')


@app.route('/', methods=['GET'])
def index():
    return "FMECA Homepage"


@app.route('/facilities/<ident>/area/new', methods=['POST'])
def new_area():
    facility = risk_calculator.facilities['ident']

    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['name', 'operator']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Facility
    index = risk_calculator.add_facility(values['name'], values['operator'])

    response = {'message': f'Facility will be added to Risk Calculator {index}'}
    return jsonify(response), 201


@app.route('/facilities/new', methods=['POST'])
def new_facility():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['name', 'operator']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Facility
    index = risk_calculator.add_facility(values['name'], values['operator'])

    response = {'message': f'Facility will be added to Risk Calculator {index}'}
    return jsonify(response), 201


@app.route('/facilities/', methods=['GET'])
def facilities():
    response = {'facilities': []}
    for facility in risk_calculator.facilities:
        response['facilities'].append(facility.name)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
