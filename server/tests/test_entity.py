import pytest
from model import Entity, EntityData, Property


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
    {'field': 'x', 'value': 0, 'expected': False, 'message': 'Set x=0'},
    {'field': 'x', 'value': 1, 'expected': True, 'message': 'Set x=1'},
    {'field': 'y', 'value': 0, 'expected': False, 'message': 'Set y=0'},
    {'field': 'y', 'value': 1, 'expected': True, 'message': 'Set y=1'},
])
def entity_validate(request):
    class EntityValidate(EntityData):
        _properties = Property.build([
            ['x', int, {'default': 1}],
            ['y', int, {'default': 1}]])

        def __init__(self, data=None, keep_valid=False):
            super().__init__(data=data)
            self._keep_valid = keep_valid

        def is_valid(self):
            return self.x + self.y >= 2

    ret = request.param
    ret['class'] = EntityValidate
    return ret


def test_entity_validate(entity_validate):
    message = entity_validate['message']
    field = entity_validate['field']
    value = entity_validate['value']
    expected = entity_validate['expected']
    obj = entity_validate['class']()

    obj[field] = value
    assert obj.validate() == expected, "%s and allow invalid" % message


def test_entity_keep_valid(entity_validate):
    message = entity_validate['message']
    field = entity_validate['field']
    value = entity_validate['value']
    expected = entity_validate['expected']
    obj = entity_validate['class'](keep_valid=True)
    try:
        obj[field] = value
        assert expected, "%s and keep valid" % message
    except:
        assert not expected, "%s and keep valid" % message


@pytest.fixture(params=[
    {'collection': None, 'expected': 'entitycollection',
        'message': 'default collection'},
    {'collection': 'override', 'expected': 'override',
        'message': 'override collection'},
])
def entity_collection(request, db):
    ret = request.param

    class EntityCollection(Entity):
        _collection = ret['collection']
    ret['class'] = EntityCollection
    return ret


def test_entity_collection(entity_collection):
    message = entity_collection['message']
    expected = entity_collection['expected']
    cls_type = entity_collection['class']
    assert cls_type.collection_name() == expected, message
    assert cls_type.collection() is not None, message


@pytest.fixture(params=[
    {'name': None, 'age': None, 'message': 'no values'},
    {'name': 'test', 'age': None, 'message': 'name'},
    {'name': None, 'age': 42, 'message': 'age'},
    {'name': 'this', 'age': 21, 'message': 'both'}
])
def entity_populate(request, db):
    class Populated(Entity):
        _properties = Property.build([
            ['name', str, {'default': 'no name'}],
            ['age', int, {'default': 0}]
        ])
    ret = request.param
    ret['cls'] = Populated
    return ret


def test_entity_populated(entity_populate):
    name = entity_populate['name']
    age = entity_populate['age']
    message = entity_populate['message']
    cls = entity_populate['cls']
    obj = cls()
    obj.name = name
    obj.age = age
    assert obj.validate() and not obj.saved, 'Validate %s' % message
    obj.save()
    assert obj.validate() and obj.saved, 'Saved %s' % message
    newObj = cls(obj.name)
    assert newObj.valid and newObj.saved, 'Loaded %s' % message
    assert newObj.name == obj.name, "Loaded name for %s" % message
    assert newObj.age == obj.age, "Loaded age for %s" % message
