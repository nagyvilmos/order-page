import logging
import model.migration as migration
from model.session import get_session, request_token


log = logging.getLogger('order_page')
orderPage = None


class OrderPage:
    def __init__(self, mongo):
        global orderPage
        orderPage = self
        self.db = mongo.db
        self._init_model()

    def _init_model(self):
        """set up the inital data"""
        migration.set_model(self.db)

    def action_auth(self, session, req):
        return session

    def request(self, req):
        """
            Entry point for the API
            req contains a json structure, if the 
        """
        session = get_session(req)

        action = {
            'request_token': [request_token, False]
        }.get(req.get('action'), [None, True])
        action_func = action[0]
        action_auth = action[1]

        if action_auth and session is None:
            return self.reply()
        if action_func is not None:
            # possibly we can get a different session back
            session = action_func(session, req)
        return self.reply(session)

    def reply(self, session=None):
        """
            Exit point for the API
        """
        if session is None:
            # any defaults can be returned here:
            return {'success': False,
                    'response': 'No active session',
                    'data': None}
        return session.get_session_data()
