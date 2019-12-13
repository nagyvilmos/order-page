from model.entity_data import EntityData
import model.field as field


# defined here, the mongo DB is callable through the entity class:
mongo = None


def init_model(db):
    global mongo
    mongo = db


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
        if len(self._changed) == 0:
            return
        if not self.validate():
            Exception('Invalid entity')
        data = self.get_changed_values()
        col = type(self).collection
        key = self.get_

    @classmethod
    def collection(cls):
        return mongo[cls.collection_name()]

    @classmethod
    def collection_name(cls):
        return cls.__name__.lower() if cls._collection is None else cls._collection

    @classmethod
    def list(cls, filter=None):
        return []

    @classmethod
    def load(cls, key):
        if type(key) is not dict:
            key = {cls._key: key}
        data = cls.collection().find_one(key)
