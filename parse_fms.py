import json


fmcco = json.load(open('core/inputs/failure_modes.json'))
fmcc_cur = json.load(open('failure_modes.json'))

fmcc_new = {}

for sc in fmcco:
    fmcc_new[sc] = {}
    for fm in fmcco[sc]["Failure Modes"]:
        c = fmcco[sc]["Failure Modes"][fm]["Global Consequences"]
        try:
            if fmcc_cur[sc][fm]["Random/Time Dependant"] == "R.":
                td = False
            else:
                td = True
        except KeyError:
            td = None
        try:
            mttf = fmcc_cur[sc][fm]["BP Ored MTTF"]
        except KeyError:
            mttf = None
        try:
            det = fmcc_cur[sc][fm]["Detectable by Inspection"]
        except KeyError:
            det = None
        try:
            ins = fmcc_cur[sc][fm]["Type of Inspection"]
        except KeyError:
            ins = None
        try:
            mttf = fmcc_cur[sc][fm]["BP Ored MTTF"]
        except KeyError:
            mttf = None

        fmcc_new[sc][fm] = {}

        fmcc_new[sc][fm]['time_dependent'] = td
        fmcc_new[sc][fm]['mean_time_to_failure'] = mttf
        fmcc_new[sc][fm]['detectable'] = det
        fmcc_new[sc][fm]['inspection_type'] = ins
        fmcc_new[sc][fm]['consequence_description'] = c

with open('fms.json', 'w') as o:
    json.dump(fmcc_new, o, indent=4)
