import copy
import json
from collections import namedtuple
import math
from exceptions import ValidationError

# load input data
failure_modes = json.load(open('app/core/inputs/subcomponents.json'))
fm_settings = json.load(open('app/core/inputs/fm_settings.json'))


class Component:
    def __init__(self, ident):
        self.ident = ident
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

    def run_rbi(self, inspection_type='ROV Inspection'):
        # run calculation if first time
        if self._total_risk is None:
            print('Calculating total component risk.')
            # self.subcomponents_calculated = copy.deepcopy(self.subcomponents)
            self._total_risk = 0
            for subcomponent in self.subcomponents:
                for risk in subcomponent.risks:
                    if risk.inspection_type == inspection_type:
                        self._total_risk += subcomponent.total_risk
        return self._total_risk


def annual_probability_of_failure(mttf):
    """ Returns the annual probability of failure of a subcomponent based on
    the Mean Time to Failure (MTTF). """
    failure_rate = 1 / mttf
    t = 1
    return 1 - math.exp(-failure_rate * t)


class SubComponent:
    def __init__(self, description, ident, consequences=None):
        self.description = description
        self.ident = ident
        try:
            self.failures = failure_modes[self.description]['Failure Modes']
        except KeyError:
            print('Choose subcomponent from list.')
        for failure in self.failures:
            print(self.failures[failure],
                  self.failures[failure]["Global Consequences"])
        self._risks = []
        self.consequences = consequences

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    @property
    def risks(self):
        # run calculation if first time
        if len(self._risks) == 0:
            print('Compiling subcomponent risks.')
            for failure in self.failures:
                probability = annual_probability_of_failure(
                    self.failures[failure]['mttf'])
                consequence = self.failures[failure]["Global Consequences"]
                try:
                    cost = self.consequences[consequence]
                except KeyError as e:
                    raise ValidationError(
                        'Invalid consequence: missing ' + e.args[0])

                self._risks.append(Risk(failure, probability, cost))

        return self._risks


class Failure:
    def __init__(self, subcomponent, consequence):
        self.rate = failure_modes[subcomponent]
        self.consequence = consequence
        self.time_dependant


class Risk:

    def __init__(self, name, probability, cost):
        self.name = name
        self.probability = probability
        self.cost = cost

    @property
    def risk(self):
        return self.probability * self.cost


if __name__ == "__main__":

    sc = SubComponent('Actuated Process Valve', 'V1')
    sc.consequences = {
        'Major Intervention': 400,
        'Minor Intervention': 100
    }

    print(sc.risks)

    # print(failure_modes)

    # sc = SubComponent('Actuated Process Valve', 'V1')
    # sc.consequences = {'major': 400, 'minor': 100}

    # print(sc.risks)
    # print(sc.risks)
    # print(sc.total_risk)
    # print(sc.total_risk)

    # manifold = Component('M1')
    # manifold.add_consequence('major', 2000)
    # manifold.add_consequence('minor', 100)
    # manifold.add_subcomponent('Actuated Process Valve', 'V1')

    # print(manifold.total_risk)

    # coupling = SubComponent('C1')
    # failure_mode = FailureMode(0.1, 'major')
    # coupling.add_failure_mode(failure_mode)
    # manifold.add_consequence('change', 200)
    # failure_mode = FailureMode(0.5, 'change')
    # coupling.add_failure_mode(failure_mode)
    # manifold.add_subcomponent(coupling)

    # print(manifold.risk)

    # print('Run 2')
    # manifold.add_subcomponent(valve)
    # print(manifold.risk)

    # import json
    # from pprint import pprint

    # subcomponent_dict = json.load(open('app/subcomponents.json'))

    # # pprint(subcomponent_dict)

    # subcomponent = "Actuated Process Valve"

    # # for fm in subcomponent_dict[subcomponent]["Failure Modes"]:
    # #     pprint(fm['Failure Rate (fpmh)'])

    # # #

    # fms = subcomponent_dict['Acoustic Sand Detector']["Failure Modes"]["Loss of Function due to Failure to Open on demand"]

    # print(fms)

    # # # for item in

    # # print(fms)

    # # # for fc in fms['Failure Causes']:
    # # #     print(fc)

    # # # pprint(data)
