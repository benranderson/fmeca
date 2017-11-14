from copy import deepcopy


class Component:
    def __init__(self, ident):
        self.ident = ident
        self.subcomponents = []
        self.consequences = {}
        self._risk = None
        self.subcomponents_calculated = []

    def add_subcomponent(self, subcomponent):
        # provide subcomponent with component consequence dict
        subcomponent.consequences = self.consequences
        self.subcomponents.append(subcomponent)

    def add_consequence(self, name, cost):
        self.consequences[name] = cost
        # add new consequence to all subcomponents dicts
        for subcomponent in self.subcomponents:
            subcomponent.consequences = self.consequences

    @property
    def risk(self):
        # run calculation if first time or subcomponent list is updated
        if self._risk is None or self.subcomponents != self.subcomponents_calculated:
            print('Calculating component risk')
            self.subcomponents_calculated = deepcopy(self.subcomponents)
            self._risk = 0
            for subcomponent in self.subcomponents_calculated:
                self._risk += subcomponent.risk
        return self._risk


class SubComponent:
    def __init__(self, ident):
        self.ident = ident
        self._risk = None
        self.failure_modes = []
        self.consequences = None
        self.failure_modes_calculated = []

    def add_failure_mode(self, failure_mode):
        self.failure_modes.append(failure_mode)

    @property
    def risk(self):
        # run calculation if first time or failure mode list is updated
        if self._risk is None or self.failure_modes != self.failure_modes_calculated:
            print('Calculating subcomponent risk')
            self.failure_modes_calculated = deepcopy(self.failure_modes)
            self._risk = 0
            for failure_mode in self.failure_modes_calculated:
                try:
                    self._risk += failure_mode.probability * \
                        self.consequences[failure_mode.consequence]
                except KeyError:
                    print('Select consequence from component consequence list.')
        return self._risk


class FailureMode:
    def __init__(self, probability, consequence):
        self.probability = probability
        self.consequence = consequence


if __name__ == "__main__":
    manifold = Component('M1')
    manifold.add_consequence('major', 2000)
    manifold.add_consequence('minor', 100)
    manifold.add_consequence('change', 200)

    valve = SubComponent('V1')
    failure_mode = FailureMode(0.1, 'major')
    valve.add_failure_mode(failure_mode)
    failure_mode = FailureMode(0.3, 'gg')
    valve.add_failure_mode(failure_mode)
    manifold.add_subcomponent(valve)

    coupling = SubComponent('C1')
    failure_mode = FailureMode(0.1, 'major')
    coupling.add_failure_mode(failure_mode)
    failure_mode = FailureMode(0.5, 'change')
    coupling.add_failure_mode(failure_mode)
    manifold.add_subcomponent(coupling)

    print(manifold.risk)

    print('Run 2')
    manifold.add_subcomponent(valve)
    print(manifold.risk)
