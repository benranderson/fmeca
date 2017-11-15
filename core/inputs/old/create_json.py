import json

SUBCOMPONENTS = json.load(open('core/inputs/subcomponents.json'))
FAILURE_MODES = json.load(open('core/inputs/failure_modes.json'))

fms = {}

SUBCOMPONENTS_UPDATED = SUBCOMPONENTS

for sc in SUBCOMPONENTS:
    for fm in SUBCOMPONENTS[sc]['Failure Modes']:
        # print(FAILURE_MODES[sc][fm]['Random/Time Dependant'])
        try:
            time_dependant = FAILURE_MODES[sc]["Failure Modes"][fm]['Random/Time Dependant']
        except KeyError:
            time_dependant = None

        new = {
            "Random/Time Dependant": time_dependant,
            "BP Ored MTTF": 3077.4,
            "Detectable by Inspection": "Lagging",
            "Type of Inspection": "ROV Inspection"
        }
        SUBCOMPONENTS_UPDATED[sc]["Failure Modes"][fm].update(new)

with open('core/inputs/fms.json', 'w') as o:
    json.dump(SUBCOMPONENTS_UPDATED, o, indent=4)
