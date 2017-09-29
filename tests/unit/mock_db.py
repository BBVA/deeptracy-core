

class MockQuery:
    _ret_val = None

    def __init__(self, model):
        self._model = model

    def get(self, id):
        return self._ret_val

    def update(self, condition):
        return self.condition


class MockSession:
    query = MockQuery

    def close(self):
        pass

    def add(self, object):
        pass


class MockDeeptracyDBEngine:

    engine = None
    Base = None
    Session = MockSession
    created_session = None
