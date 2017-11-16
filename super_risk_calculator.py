import copy
import json
from collections import namedtuple
import math
from app.exceptions import ValidationError
from core.fmeca import FMECA
from core.rbi import RBI

class SuperFMECAType():
    
    def __init__(self, ident):
        self.ident = ident
    
    def export_data(self):
        data = {}
        for a in self.__dict__:
            if type(self.__dict__[a]) == type({}):
                data[a] = {k: v for k, v in
                    [(b, self.__dict__[a][b].export_data()) for b in 
                          self.__dict__[a].keys()]}
            elif type(self.__dict__[a]) == type([]):
                data[a] = { k: v for k, v in 
                    [(b.ident, b.export_data()) for b in self.__dict__[a]]}
            else:
                data[a] = self.__dict__[a]
        return data
    
    def import_data(self, data):
        for a in data:
            if type(data[a]) == type({}):
                c = _format_class_name(a)
                if type(getattr(self, a)) == type({}):
                    for l in data[a].keys():
                        o = eval(c)(l)
                        o.import_data(data[a][l])
                        getattr(self, a)[l] = o
                else:
                    for l in data[a]:
                        o = eval(c)(l)
                        o.import_data(data[a][l])
                        getattr(self, a).append(o)
            else:
                setattr(self, a, data[a])
    
    def _format_class_name(self, s):
        s = s.replace('_', ' ').title().replace(' ', '')
        if s[-3:] == 'ies':
            s = s[:-4] + 'y'
        else:
            s = s[:-1]
        return s

# load input data
FAILURE_MODES = json.load(open('core/inputs/failure_modes.json'))
AREA = json.load(open('core/inputs/area1.json'))

from flask import Flask, jsonify, request

class RiskCalculator(SuperFMECAType):
    
    def __init__(self, filename=''):
        if filename == '':
            self.facilities = []
            self.filename = ''
        else:
            self.facilities = self.import_data(open(filename, 'r').readlines())
            
    def save(self, filename=''):
        if filename == self.filename == '':
            raise ValueError('Enter valid filename for save.')
        else:
            if not '.json' in self.filename:
                self.filename = self.filename + '.json'
            with open(self.filename, 'w') as o:
                json.dump(self.export_data(), o)
        
    def add_facility(self, name, operator):
        self.import_data(Facility(name, operator).export_data())


class Facility(SuperFMECAType):

    def __init__(self, name, operator):
        super(type(self), self).__init__(name)
        self.name = name
        self.operator = operator
        self.vessels = {}
        self.areas = []
        # read in default lists i.e. FAILUREMODES above

    def add_area(self, area):
        self.import_data(area.export_data())

    def read_vessels(self, json_filename):
        with open(json_filename, 'r') as j:
            d = json.load(j)
            self.vessels = d["Vessels"]

class Area(SuperFMECAType):

    def __init__(self, name):
        super(type(self), self).__init__(name)
        self.name = name
        self.components = []
        self.financial_data = {}

    def add_component(self, component):
        self.import_data(component.export_data())

    def read_components(self, json_filename):
        self.import_data(open(json_filename, 'r').readlines())

    def read_financial_data(self, json_filename):
        with open(json_filename, 'r') as j:
            self.financial_data = json.load(j)


class Consequence(SuperFMECAType):
    def __init__(self, name):
        super(type(self), self).__init__(name)
        self.name = name
        # self.mttr = mttr
        self.vessel_trips = []

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def add_vessel_trip(self, vessel_trip):
        self.import_data(vessel_trip.export_data())

class Component(SuperFMECAType):
    def __init__(self, ident):
        super(type(self), self).__init__(ident)
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
        self.import_data(subcomponent.export_data())

    def add_consequence(self, name, cost):
        self.import_data({ "consequences": { name: cost } })

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
    
    def compile_rbi(self, fmeca):
        self.rbi = RBI(fmeca)

    def compile_base_fmeca(self):
        self.fmeca = FMECA(self.subcomponents)

class SubComponent(SuperFMECAType):
    def __init__(self, description, ident, consequences=None):
        super(type(self), self).__init__(ident)
        self.description = description
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


class Failure(SuperFMECAType):
    def __init__(self, description, subcomponent, consequences=None):
        super(type(self), self).__init__(description)
        self.description = description
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

app = Flask(__name__)


# Instantiate the Facility Risk Class
fmeca = RiskCalculator()


@app.route('/', methods=['GET'])
def index():
    return "FMECA Homepage"


@app.route('/facilities/new', methods=['POST'])
def new__facility():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['name']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Facility
    index = fmeca.add_facility(values['name'])

    response = {'message': f'Facility will be added to FMECA {index}'}
    return jsonify(response), 201


@app.route('/facilities/', methods=['GET'])
def facilities():
    response = {'facilities': []}
    for facility in fmeca.facilities:
        response['facilities'].append(facility.name)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
        