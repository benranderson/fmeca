import json
from exceptions import ValidationError


class RiskCalculator:

    def __init__(self, filename):
        self.filename = filename
        self.facilities = []
        self._build_object_model()

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.filename}>'

    def _build_object_model(self):
        db = json.load(open(f'{self.filename}.json'))
        for facility_data in db['facilities']:
            f = Facility()
            self.facilities.append(f.import_data(facility_data))
            for vessel_data in facility_data['vessels']:
                v = Vessel(f)
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

    def __init__(self):
        self.ident = None
        self.name = None
        self.operator = None
        self.vessels = []
        self.areas = []

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def export_data(self):
        return {
            'ident': self.ident,
            'name': self.name,
            'operator': self.operator,
            'vessels': [vessel.export_data() for vessel in self.vessels]
        }

    def import_data(self, data):
        try:
            self.ident = data['ident']
            self.name = data['name']
            self.operator = data['operator']
        except KeyError as e:
            raise ValidationError('Invalid facility: missing ' + e.args[0])
        return self


class Vessel:

    def __init__(self, facility):
        self.facility = facility
        self.name = None
        self.abbr = None

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.abbr}>'

    def export_data(self):
        return {
            'name': self.name,
            'abbr': self.abbr
        }

    def import_data(self, data):
        try:
            self.name = data['name']
            self.abbr = data['abbr']
        except KeyError as e:
            raise ValidationError(
                f'Invalid vessel in {self.facility}: missing {e.args[0]}')
        return self


if __name__ == "__main__":
    rc = RiskCalculator('input')
    print(rc)
    for facility in rc.facilities:
        print(facility)
        for vessel in facility.vessels:
            print(vessel)

    f = Facility()
    f.ident = 'Andrew'
    rc.facilities.append(f)
    v = Vessel(f)
    f.vessels.append(v)

    rc.save('output')
