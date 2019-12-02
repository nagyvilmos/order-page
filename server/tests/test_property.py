import pytest
from model import Property


def test_property():
    prop = Property('test')
    assert not prop.required, 'Default property is not required'


def test_property_string():
    prop = Property('test', str)
    assert prop.set_value(None, 'xxx') == 'xxx', 'Property set to str failed'


def test_build_properties():
    props = Property.build([
        ["string", str],
        ["integer", int],
        "any",
        ["not_null", str, {'default': 'default'}],
        ["from_range", str, {'validate': Property.is_in(
            ['a', 'b', 'c']), 'default': 'c'}],
        ["five_to_ten", int, {
            'validate': Property.in_range(5, 10), 'default': 7}],
        ["lower_case", str, {'set': lambda obj, x: x.lower()}],
        ["derived", int, {'default':
                          lambda obj: None if obj.integer is None else obj.integer * obj.five_to_ten}]
    ])
    assert len(props) == 8, ' failed to build properties'


@pytest.fixture(params=[
    {'min': 5, 'max': 10, 'inclusive': True, 'value': -7,
        'expected': False, 'message': 'negative value below minimum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 4,
        'expected': False, 'message': 'value below minimum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 5,
        'expected': True, 'message': 'value is minimum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 6,
        'expected': True, 'message': 'value over minimum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 7,
        'expected': True, 'message': 'value in range'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 9,
        'expected': True, 'message': 'value below maximum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 10,
        'expected': True, 'message': 'value is maximum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 11,
        'expected': False, 'message': 'value over maximum'},
    {'min': 5, 'max': 10, 'inclusive': True, 'value': 250,
        'expected': False, 'message': 'high value over maximum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': -7,
        'expected': False, 'message': 'negative value below minimum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 4,
        'expected': False, 'message': 'value below minimum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 5,
        'expected': False, 'message': 'value is minimum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 6,
        'expected': True, 'message': 'value over minimum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 7,
        'expected': True, 'message': 'value in range'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 9,
        'expected': True, 'message': 'value below maximum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 10,
        'expected': False, 'message': 'value is maximum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 11,
        'expected': False, 'message': 'value over maximum'},
    {'min': 5, 'max': 10, 'inclusive': False, 'value': 250,
        'expected': False, 'message': 'high value over maximum'},
])
def valid_in_range(request):
    return request.param


def test_valid_in_range(valid_in_range):
    in_range = Property.in_range(
        valid_in_range['min'], valid_in_range['max'], valid_in_range['inclusive'])
    assert in_range(
        None, valid_in_range['value']) == valid_in_range['expected'], valid_in_range['message']


@pytest.fixture(params=[
    {'list': ['a', 'c', 'b'], 'value': 'b',
        'expected': True, 'message': 'alpha in list'},
    {'list': ['a', 'c', 'b'], 'value': 'd',
        'expected': False, 'message': 'alpha not in list'},
    {'list': [5, 3, 2], 'value': 5, 'expected': True,
        'message': 'numeric in list'},
    {'list': [5, 3, 2], 'value': 1, 'expected': False,
        'message': 'numeric not in list'}
])
def valid_is_in(request):
    return request.param


def test_is_in(valid_is_in):
    is_in = Property.is_in(valid_is_in['list'])
    assert is_in(
        None, valid_is_in['value']) == valid_is_in['expected'], valid_in_range['message']


@pytest.fixture(params=[
    {'prop': ['a', 'c', 'b'], 'value': 'b',
        'expected': True, 'message': 'alpha in prop'},
    {'prop': ['a', 'c', 'b'], 'value': 'd',
        'expected': False, 'message': 'alpha not in prop'},
    {'prop': [5, 3, 2], 'value': 5, 'expected': True,
        'message': 'numeric in prop'},
    {'prop': [5, 3, 2], 'value': 1, 'expected': False,
        'message': 'numeric not in prop'}
])
def valid_in_prop(request):
    return request.param


def test_valid_in_prop(valid_in_prop):
    in_prop = Property.in_prop('prop')
    assert in_prop(
        valid_in_prop, valid_in_prop['value']) == valid_in_prop['expected'], valid_in_prop['message']


@pytest.fixture(params=[
    {'regex': '^x', 'value': 'xyz',
        'expected': True, 'message': 'matches start with'},
    {'regex': '^x', 'value': 'wxy',
        'expected': False, 'message': 'not matches start with'},
    {'regex': '.*z$', 'value': 'xyz',
        'expected': True, 'message': 'matches end with'},
    {'regex': '.*z$', 'value': 'wxy',
        'expected': False, 'message': 'not matches end with'},
])
def valid_matches(request):
    return request.param


def test_valid_matches(valid_matches):
    matches = Property.matches(valid_matches['regex'])
    assert matches(
        None, valid_matches['value']) == valid_matches['expected'], valid_matches['message']
