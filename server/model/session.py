"""
    session information
"""
from model.entity import Entity
from model.property import Property
import hashlib
import secrets


def _generate_secret(length, inHex=False):
    if inHex:
        return secrets.token_hex(length)
    return secrets.token_urlsafe(length)


def _generate_digest(secret):
    h = hashlib.md5(secret.encode())
    return h.hexdigest()


def _request_token_async(session, req):
    return None


def request_token(session, req):
    return None


def authorise_token(session, req):
    return None


def get_session(req):
    name = req.get('name')
    token = req.get('token')
    if name is None or token is None:
        return None

    digest = _generate_digest(token + name)
    return Session().load({'digest': req['digest']})


class Session(Entity):
    _properties = Property.build([
        ['name', str],
        ['authorised', bool, {'default': False}]
    ])

    def authorised(self, value):
        return self._prop('authorised', default=False)
