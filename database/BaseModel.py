from peewee import *
import database as logdb

class BaseModel(Model):


    class Meta:
        database = logdb.database
