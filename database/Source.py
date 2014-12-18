from peewee import *
from .BaseModel import BaseModel
from .ListJSONCollector import ListJSONCollector
from .Response import *

class Source(BaseModel):

    name = TextField(null=False, unique=True)

    @classmethod
    def add(cls, name):
        source = cls.create(name=name)
        if not source:
            return Response(successful=False,
                            status_code=HTTP_INTERNAL_ERROR,
                            description="Could not add source.")
        return Response(data=source)


    def add_log(self, content):
        from .Log import Log
        log = Log.add(content, self)
        return log

    def clear_logs(self):
        try:
            self.delete_instance(recursive=True)
            return Response(description="Successfully cleared logs for '" +
                                        self.name + "'")
        except:
            return Response(successful=False,
                            description="Could not clear '" +
                                         self.name + "'")

    @classmethod
    def find(cls, name):
        source = cls.select().where(cls.name == name)
        if not source.exists():
            return Response(successful=False,
                            status_code=HTTP_BAD_REQUEST,
                            description="Could not find source '" +
                                        name + "'")
        return Response(data=source.first())


    @classmethod
    def exists(cls, name):
        source = cls.select().where(name=name)
        return source.exists()


    def all_logs(self):
        return ListJSONCollector(self.logs)


    def json_object(self):
        return {
            "source" : self.name,
            "logs" : self.all_logs().json_object()
        }

