import pytest
import random
import pymongo

from model.entity import init_model

random.seed()
db_name = 'test_' + ("0000%i" % random.randint(0, 9999))[-4:]
client = pymongo.MongoClient('mongodb://localhost', 27017)


@pytest.fixture(scope='session')
def db(request):
    db = client.get_database(db_name)
    init_model(db)

    def fin():
        client.drop_database(db_name)
    request.addfinalizer(fin)
    return db
