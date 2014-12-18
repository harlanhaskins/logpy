__author__ = 'harlanhaskins'

from peewee import *

"""
database
The peewee interface to the database
The server interfaces with this API
"""

################
# Constants
################

DATABASE_IDENTIFIER = 'logpy'

database = PostgresqlDatabase(DATABASE_IDENTIFIER,
                              user=DATABASE_IDENTIFIER,
                              password=DATABASE_IDENTIFIER,
                              threadlocals=True)


def create_tables():
    """
    create_tables is an internal function to ensure that all tables in the
    system are created.
    """

    import Log
    import Source
    Source.Source.create_table(fail_silently=True)
    Log.Log.create_table(fail_silently=True)


def connect():
    database.connect()
    create_tables()
