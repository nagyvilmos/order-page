import pytest
from model import EntityData, Property


@pytest.fixture(params=[
    {'value': None, 'valid': False, 'create': True,
        'message': 'Create empty entity data'},
    {'value': {'name': 'Test'}, 'valid': True,
        'create': True, 'message': 'Create with name'},
    {'value': {'names': 'Test'}, 'valid': False,
        'create': False, 'message': 'Create with bad field'},
    {'value': {'name': 'Test', 'age': 42, 'tags': ['a', 'b', 'c']}, 'valid': True,
        'create': True, 'message': 'Create with bad field'}
])
def create_entity_data(request):
    class CreateEntityClass(EntityData):
        _properties = Property.build(['name', 'age', 'tags'])
    ret = request.param
    ret['class'] = CreateEntityClass
    return ret


def test_create_entity_data(create_entity_data):
    value = create_entity_data['value']
    try:
        obj = create_entity_data['class'](value)
        assert create_entity_data['create'], '%s instantiate' % create_entity_data['message']
        assert len(obj) == 0 if value is None else len(
            value), '%s size' % create_entity_data['message']
        assert obj.validate(
        ) == create_entity_data['valid'], '%s valid' % create_entity_data['message']
    except:
        assert not create_entity_data['create'], '%s exception' % create_entity_data['message']


@pytest.fixture(params=[
    {'value': {}, 'message': 'Defaults'},
    {'value': {'age': 42, 'tags': ['a', 'b', 'c']},
        'message': 'Default String'},
    {'value': {'name': 'Test', 'tags': [
        'a', 'b', 'c']}, 'message': 'Default number'},
    {'value': {'name': 'Test', 'age': 42, 'tags': [
        'a', 'b' 'c']}, 'message': 'No default'}
])
def entity_defaults(request):
    class EntityDefaultClass(EntityData):
        _properties = Property.build([
            ['name', str, {'default': 'Name'}],
            ['age', int, {'default': 21}],
            ['tags', None, {'default': ['x']}]])
    ret = request.param
    ret['class'] = EntityDefaultClass
    return ret


def test_entity_defaults(entity_defaults):
    message = entity_defaults['message']
    value = entity_defaults['value']
    obj = entity_defaults['class'](value)
    assert obj.name == value.get('name', 'Name'), "Check %s name" % message
    assert obj.age == value.get('age', 21), "Check %s age" % message
    assert obj.tags == value.get('tags', ['x']), "Check %s tags" % message


@pytest.fixture(params=[
    {'x': None, 'y': None, 'z': 2, 'message': 'Defaults'},
    {'x': 1, 'y': 1, 'z': 2, 'message': 'Defaults'},
    {'x': 4, 'y': None, 'z': 5, 'message': 'x=4'},
    {'x': -2, 'y': -6, 'z': -8, 'message': '[-2,-6]'},
    {'x': 1, 'y': -12, 'z': -11, 'message': '[1,-12]'},
])
def entity_derived(request):
    class EntityDerived(EntityData):
        _properties = Property.build([
            ['x', int, {'default': 1}],
            ['y', int, {'default': 1}],
            ['z', int, {'default': lambda obj: obj.x + obj.y}]])
    ret = request.param
    ret['class'] = EntityDerived
    return ret


def test_entity_derived(entity_derived):
    message = entity_derived['message']
    x = entity_derived['x']
    y = entity_derived['y']
    z = entity_derived['z']
    obj = entity_derived['class']()

    obj.x = x
    if x is None:
        assert obj.x == 1, message
    else:
        assert obj.x == x, message
    obj.y = y
    if y is None:
        assert obj.y == 1, message
    else:
        assert obj.y == y, message
    assert obj.z == z, message


def test_entity_setter():
    def setter(obj, value):
        obj.z = obj.z+1
        return value

    class EntitySetter(EntityData):
        _properties = Property.build([
            ['x', int, {'set': setter}],
            ['y', int, {'set': setter}],
            ['z', int, {'default': 0}]])

    obj = EntitySetter()

    obj.x = 1
    assert obj.z == 1, 'set x'
    obj.y = 1
    assert obj.z == 2, 'set y'
    obj.x = 1
    obj.y = 1
    assert obj.z == 4, 'set x+y'


@pytest.fixture(params=[
    {'x': 0, 'y': 0, 'expected': [], 'message': 'Set 0 0'},
    {'x': 1, 'y': 0, 'expected': ['x'], 'message': 'Set 1 0'},
    {'x': 0, 'y': 1, 'expected': ['y'], 'message': 'Set 0 1'},
    {'x': 1, 'y': 1, 'expected': ['x', 'y'], 'message': 'Set 1 1'},
])
def entity_validate(request):
    def validate(obj, value):
        return obj.x + obj.y >= 2

    class EntityValidate(EntityData):
        _properties = Property.build([
            ['x', int, {'default': 1, 'validate': validate}],
            ['y', int, {'default': 1, 'validate': validate}]])
    ret = request.param
    ret['class'] = EntityValidate
    return ret


def test_entity_derived(entity_validate):
    message = entity_validate['message']
    x = entity_validate['x']
    y = entity_validate['y']
    expected = entity_validate['expected']
    obj = entity_validate['class']()

    try:
        obj.x = x
        assert 'x' in expected, message
    except Exception as ex:
        assert 'x' not in expected, message

    try:
        obj.y = y
        assert 'y' in expected, message
    except:
        assert 'y' not in expected, message