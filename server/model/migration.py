"""
    Database migration
    Set up the initial db content and amend as required
    Any method with the migrate decorator is run if not called before according to the 'migrated' collection
"""

from datetime import datetime
import logging
import sys
import inspect
import types


log = logging.getLogger('migration')
mongo = None
migrated = None
migrate_funcs = []


def migrate(func):
    migration = func.__name__

    def wrapper(*args, **kwargs):
        doc = {'migration': migration}
        if migrated.find_one(doc):
            return

        log.info('Migration: ' + migration)
        func(*args, **kwargs)
        doc['date_time'] = datetime.now()
        migrated.insert(doc)

    # add the wrapper to the list of migrations
    # if it hasn't already been called, then it will
    # be called once and recorded in the database
    migrate_funcs.append(wrapper)
    return func


def set_model(db):
    global mongo, migrated
    mongo = db
    migrated = mongo['migrated']
    for func in migrate_funcs:
        func()
    log.info('db up to date')


@migrate
def initialise_user():
    mongo.user.insert_one({'name': 'admin'})
