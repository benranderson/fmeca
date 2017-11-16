import pytest
import json

from .context import rbi
from .context import Failure, SubComponent, Component, Consequence

# tolerance
tol_pc = 0.001

FACILITY = json.load(
    open('core/tests/test_inputs/facility.json')
)


FAILURE_MODES = json.load(
    open('core/tests/test_inputs/failure_modes.json')
)


@pytest.fixture()
def consequences():
    return {
        'Major Intervention': 1000000,
        'Minor Intervention': 300000,
        'Loss of Redundancy': 50000,
    }

# Failures
# -------------


def test_failure(consequences):
    f = Failure('Loss of Function due to Failure to Open on demand',
                'Actuated Process Valve', consequences)
    assert 'Loss of Function due to Failure to Open on demand' in repr(f)
    assert f.consequence == 'Minor Intervention'
    assert f.cost == 300000
    assert f.mttf == 3077.4
    assert f.time_dependant == False
    assert f.detectable == "Lagging"
    assert f.inspection_type == "ROV Inspection"


def test_failure_probability(consequences):
    f = Failure('Loss of Function due to Failure to Open on demand',
                'Actuated Process Valve', consequences)
    expected = 0.000324897
    assert abs(f.probability - expected) <= tol_pc * expected


def test_failure_risk(consequences):
    f = Failure('Loss of Function due to Failure to Open on demand',
                'Actuated Process Valve', consequences)
    expected = 97.469
    assert abs(f.risk - expected) <= tol_pc * expected


# Subcomponents
# -------------


def test_subcomponent(consequences):
    sc = SubComponent('Actuated Process Valve', 'V1', consequences)
    assert 'V1' in repr(sc)
    assert any(failure.description ==
               'Loss of Function due to Failure to Open on demand' for failure in sc.failures)


# Components
# -------------


def test_component():
    c = Component('M1')
    assert 'M1'in repr(c)


@pytest.fixture()
def component():
    return Component('M1')


def test_component_add_subcomponent(component):
    component.add_subcomponent('Actuated Process Valve', 'V1')
    assert any(subcomponent.description ==
               'Actuated Process Valve' for subcomponent in component.subcomponents)


def test_component_add_consequence(component, consequences):
    for name, cost in consequences.items():
        component.add_consequence(name, cost)
    assert component.consequences['Major Intervention'] == 1000000


@pytest.fixture()
def loaded_component(component, consequences):
    lc = component
    lc.add_subcomponent('Actuated Process Valve', 'V1')
    for name, cost in consequences.items():
        lc.add_consequence(name, cost)
    return lc


def test_component_risk_before_run_rbi(loaded_component):
    assert loaded_component.total_risk == 'Run component RBI.'


def test_component_run_rbi(loaded_component):
    loaded_component.run_rbi()
    expected = 251.7950529
    assert abs(loaded_component.total_risk - expected) <= tol_pc * expected

# Consequences
# ------------


def test_consequence():
    c = Consequence('Major Intervention')
    assert 'Major Intervention' in repr(c)
