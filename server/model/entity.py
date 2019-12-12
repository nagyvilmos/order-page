import model.field as field
from model.property import Property

# defined here, the mongo DB is callable through the entity class:
mongo = None


def init_model(db):
    global mongo
    mongo = db


class EntityData:
    # if marked TRUE, then error if a property change leaves the entity invalid

    _keep_valid = False
    _properties = []

    def __init__(self, data=None):
        self._keep_valid = False  # allow the instance to load
        self._data = {}
        self._changed = []
        if data is not None:
            for k in data:
                self[k] = data[k]
        self.valid = self.validate()
        self._changed = []  # clear again as not needed
        self._keep_valid = type(self)._keep_valid

    def __getattr__(self, item):
        prop = self.get_property(item)
        if prop is not None:
            return prop.get_value(self, self._data.get(item))
        return super().__getattr__(item)

    def __getitem__(self, index):
        return self.__getattr__(self.get_fields(index))

    def __setattr__(self, item, value):
        prop = self.get_property(item)
        if prop is not None:
            old = self._data.get(item)
            self._data[item] = prop.set_value(self, value)
            if self._keep_valid and not self.validate():
                self._data[item] = old
                self.validate()
                raise ValueError('Changing %s will leave %s invalid' %
                                 (item, self.__class__.__name__))
            if item not in self._changed:
                self._changed.append(item)
        else:
            super().__setattr__(item, value)

    def __setitem__(self, index, value):
        self.__setattr__(self.get_fields(index), value)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return '%s(%s)' % (type(self).__name__,
                           ', '.join(["%s: %s" % (s, str(self[s])) for s in self.get_fields() if self.get_property(s).derived or self._data.get(s) is not None]))

    def get_changed(self, index=None):
        for f in self.get_fields():
            if f not in self._changed and issubclass(f.type, EntityData):
                continue
            if len(self[f].get_changed()) > 0:
                self._changed.append(f)
        if index is None:
            return self._changed
        return self._changed[index]

    def get_changed_values(self, all_if_any=False):
        fields = self.get_changed()
        if all_if_any and len(fields) > 0:
            return self.get_data()
        if fields is None:
            return None
        return self.get_data(fields)

    def get_data(self, fields=None):
        if fields is None:
            return self._data
        return {f: self._data[f] for f in fields}

    def get_fields(self, index=None):
        fields = [p.name for p in type(self)._properties]
        if type(index) is str:
            if index in fields:
                return index
            return None
        if type(index) is int:
            return fields[int]
        return fields

    def get_property(self, prop_name):
        props = [p for p in type(self)._properties if p.name == prop_name]
        if len(props) == 0:
            return None
        return props[0]

    def validate(self):
        # !!! don't override - use is_valid!
        self.valid = self.is_valid()
        return self.valid

    def is_valid(self):
        return self._data is not None and len(self._data) > 0

    @staticmethod
    def build_properties(properties):
        return Property.build(properties)


class Entity(EntityData):
    """Entity within the model"""
    _collection = None
    _key = field.name

    def __init__(self, data=None, key=None):
        if key is not None:
            data = type(self).load(key)
        super().__init__(data)
        self.validate()
        self.saved = field._id in self._data.keys()

    def save(self):
        # nothing happening
        if self.saved:
            return
        if not self.validate():
            Exception('Invalid entity')
        data = self.data()
        return self

    @classmethod
    def collection(cls):
        return mongo[cls.collection()]

    @classmethod
    def collection_name(cls):
        return cls.__name__.lower() if cls._collection is None else cls._collection

    @classmethod
    def list(cls, filter=None):
        return []

    @classmethod
    def load(cls, key):
        data = cls.collection().find_one(key)
