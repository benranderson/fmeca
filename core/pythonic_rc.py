import json
from exceptions import ValidationError

from flask import Flask, jsonify, request


class RiskCalculator:

    def __init__(self, filename):
        self.filename = filename
        self.facilities = []
        self.vessels = []
        self._build_object_model()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    def _build_object_model(self):

        db = json.load(open(f'{self.filename}.json'))

        # for vessel in db['vessels']:
        #     v = Vessel(f)

        for facility in db['facilities']:
            f = Facility()
            facility_data = db['facilities'][facility]
            self.facilities.append(f.import_data(facility_data))
        for vessel in db['vessels']:
            v = Vessel()
            vessel_data = db['vessels'][vessel]
            f.vessels.append(v.import_data(vessel_data))

    def export_data(self):
        return {
            'filename': self.filename,
            'facilities': [facility.export_data() for facility in self.facilities]
        }

    def save(self, filename=None):
        if not filename:
            filename = self.filename
        with open(f'{filename}.json', 'w') as o:
            json.dump(self.export_data(), o, indent=4)


class Facility:

    def __init__(self, ident=None, name=None, operator=None):
        self.ident = ident
        self.name = name
        self.operator = operator
        self.vessels = []
        self.areas = []

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def export_data(self):
        return {
            'ident': self.ident,
            'name': self.name,
            'operator': self.operator,
            'vessels': [vessel.ident for vessel in self.vessels]
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.operator = data['operator']
        except KeyError as e:
            raise ValidationError('Invalid facility: missing ' + e.args[0])
        return self


class Vessel:

    def __init__(self, facility=None, ident=None, name=None, day_rate=None,
                 mob_time=None):
        self.facility = facility
        self.ident = ident
        self.name = name
        self.day_rate = day_rate
        self.mob_time = mob_time

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def export_data(self):
        return {
            'ident': self.ident,
            'name': self.name,
            'day_rate': self.day_rate,
            'mob_time': self.mob_time
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.day_rate = data['day_rate']
            self.mob_time = data['mob_time']
        except KeyError as e:
            raise ValidationError(
                f'Invalid vessel in {self.facility}: missing {e.args[0]}')
        return self


app = Flask(__name__)

# Instantiate the Facility Risk Class
risk_calculator = RiskCalculator('database')


@app.route('/', methods=['GET'])
def index():
    response = risk_calculator.export_data()
    return jsonify(response), 201


@app.route('/facilities/', methods=['GET'])
def get_facilities():
    return jsonify({'facilities': [facility.export_data() for facility in
                                   risk_calculator.facilities]})


@app.route('/facilities/', methods=['POST'])
def new_facility():
    facility = Facility()
    facility.import_data(request.json)
    risk_calculator.facilities.append(facility)
    response = {'message': f'Facility will be added to {risk_calculator}'}
    return jsonify(response), 201


@app.route('/vessels/', methods=['GET'])
def get_vessels():
    vessels = {}
    for facility in risk_calculator.facilities:
        for vessel
    return jsonify(risk_calculator['vessels'])


@app.route('facilities/<ident>/vessels/', methods=['GET'])
def get_facility_vessels():
    vessels
    return jsonify({'vessels': [vessel.export_data() for vessel in
                                risk_calculator['vessels']]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
