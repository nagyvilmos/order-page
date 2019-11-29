import model.field as field

# defined here, the mongo DB is callable through the entity class:
mongo = None


def init_model(db):
    global mongo
    mongo = db


class Property:
    """
        a property for an Entity
    """

    def __init__(self, type=None, validator=None, default=None):
        self.type = type
        self.validator = validator
        self.default = default

    def check_value(self, value):
        if not self.validate(value):
            return self.default
        return value

    def validate(self, value):
        if value is None:
            pass
        elif self.type is not None and self.type != type(value):
            return False
        if self.validator is None:
            return
        return self.validator(value)


class Entity:
    """Entity within the model"""
    _collection = ''
    _key = field.name
    _dynamic = True
    _properties = {}

    def __init__(self, data=None, key=None):
        self._update = []
        if data is None or len(data) == 0:
            self._data = {}
        else:
            self._data = data
        self.validate()
        self.saved = field._id in self._data.keys()

    def get(self, name, default=None):
        return self._data.get(name, None, default)

    def set(self, name, value):
        # _data is always the real value stored/restored but we allow override for self prop.
        if value != self.get(name):
            self._data[name] = value
            self.saved = False
            self.validate()
        return self

    def data(self):
        NotImplemented('data(self)')

    def load(self, key):
        col = mongo[type(self).lower()]
        data = col.find_one(key)
        return self.__init__(data)

    def save(self):
        # nothing happening
        if self.saved:
            return
        if not self.validate:
            Exception('Invalid entity')
        data = self.data()
        return self

    def validate(self):
        self.valid = len(self._data) > 0
        return self.valid

    @classmethod
    def list(cls, filter=None):
        return []
