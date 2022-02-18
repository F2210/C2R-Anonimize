from django.db import models, IntegrityError, connections
from django.db.utils import load_backend

# DATABASE CONNECTOR FOR ASYNCHRONOUS DB CALLS
def new_db_connection(alias='default'):
    """Returns a new database connection.
    Use with RawSQL to execute the query using new connection. If you run a
    query in a new process, see users.helpers.timeout(), it will throw
    "OperationalError: SSL error: decryption failed or bad record mac". You
    can either (1) close the current connection and Django will create new one
    or (2) use a new connection. Note that if you are inside a database
    transaction, you cannot close the current connection.
    """
    connections.ensure_defaults(alias)
    connections.prepare_test_settings(alias)
    db = connections.databases[alias]
    backend = load_backend(db['ENGINE'])
    return backend.DatabaseWrapper(db, alias)