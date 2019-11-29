from model.entity import Property, Entity


name = 'name'
email = 'email'
display_name = 'display_name'
is_connected = 'is_connected'


class User(Entity):
    _collection = 'access'
    _dynamic = False
    _properties = {
        name: Property(str, lambda x: x is not None and x != ''),
        email: Property(str, lambda x: x is not None and x != ''),
        display_name: Property(str, lambda x: x is not None and x != ''),
        is_connected: Property(bool)
    }


def t(x): return x+1
