import copy
from collections import namedtuple
import math
import json
# mttf
failure_modes = {
    'Actuated Process Valve': {
        'Loss of Function due to Failure to Open on demand': {'mttf': 500,
                                                              'consequence': 'minor'},
        'Loss of Function due to Failure to Close on demand': {'mttf': 1000,
                                                               'consequence': 'minor'},
        'Loss of Function due to Blockage': {'mttf': 100,
                                             'consequence': 'major'}
    },
    'Actuator': {
        'Loss of Function due to Failure to open after hydraulic pressure has been supplied via SCM': {'mttf': 100,
                                                                                                       'consequence': 'major'},
        'Loss of Function due to Failure to close after hydraulic pressure from SCM is dumped from open side': {'mttf': 100,
                                                                                                                'consequence': 'major'}
    }
}
        
class Facility():
    
    def __init__(self, operator, name):
        self.operator = operator
        self.name = name
        self.vessels = {}
        self.areas = []
        
    def add_area(self, area):
        self.areas.append(area)
        
    def read_vessels(self, json_filename):
        with open('facility_assumptions.json', 'r') as j:
            d = json.load(j)
            for v in d:
                vessels

class Area:
    
    def __init__(self, name):
        self.name = name
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)

class Component:
    def __init__(self, ident):
        self.ident = ident
        self.subcomponents = []
        self.consequences = {}
        self._total_risk = None
        # self.subcomponents_calculated = []

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.ident}>'

    def add_subcomponent(self, description, ident):
        # provide subcomponent with component consequence dict
        subcomponent = SubComponent(description, ident)
        subcomponent.consequences = self.consequences
        self.subcomponents.append(subcomponent)

    def add_consequence(self, name, cost):
        self.consequences[name] = cost

    # TODO: change this to run_fmeca(self, inspection_type)
    @property
    def total_risk(self):
        # run calculation if first time
        if self._total_risk is None:
            print('Calculating total component risk.')
            # self.subcomponents_calculated = copy.deepcopy(self.subcomponents)
            self._total_risk = 0
            for subcomponent in self.subcomponents:
                self._total_risk += subcomponent.total_risk
        return self._total_risk


def annual_probability_of_failure(mttf):
    """ Returns the annual probability of failure of a subcomponent based on
    the Mean Time to Failure (MTTF). """
    failure_rate = 1 / mttf
    t = 1
    return 1 - math.exp(-failure_rate * t)


class SubComponent:
    def __init__(self, description, ident):
        self.description = description
        self.ident = ident
        self.failures = failure_modes[self.description]
        self._risks = []
        self._total_risk = None
        self.consequences = None

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
                try:
                    cost = self.consequences[self.failures[failure]
                                             ['consequence']]
                except KeyError:
                    print('Select consequence from component consequence list.')

                self._risks.append({
                    'name': failure,
                    'probability': probability,
                    'cost': cost
                })

        return self._risks

    @property
    def total_risk(self):
        if self._total_risk is None:
            print('Calculating total risk of subcomponent.')
            self._total_risk = 0
            for risk in self.risks:
                self._total_risk += risk['probability'] * risk['cost']
        return self._total_risk


class Failure:
    def __init__(self, subcomponent, consequence):
        self.rate = failure_modes[subcomponent]
        self.consequence = consequence


if __name__ == "__main__":

    sc = SubComponent('Actuated Process Valve', 'V1')
    sc.consequences = {'major': 400, 'minor': 100}

    print(sc.risks)
    print(sc.risks)
    print(sc.total_risk)
    print(sc.total_risk)

    manifold = Component('M1')
    manifold.add_consequence('major', 2000)
    manifold.add_consequence('minor', 100)
    manifold.add_subcomponent('Actuated Process Valve', 'V1')

    print(manifold.total_risk)

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
