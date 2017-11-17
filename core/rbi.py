class RBI:

    def __init__(self, fmeca):
        self.fmeca = fmeca
        self._generate_rbi()

    def _generate_rbi(self):
        # TODO: Add rbi logic (from risk_calculator but modified to take a
        #       fmeca argument and loop through each inspection type)

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
