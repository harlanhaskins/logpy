from peewee import *
from datetime import datetime
from .Response import *
from .BaseModel import BaseModel
from .ListJSONCollector import ListJSONCollector

class Log(BaseModel):
    from .Source import Source
    content = TextField(null=False)
    source = ForeignKeyField(Source, null=False, related_name="logs")
    date = DateTimeField()

    @classmethod
    def add(cls, content, source):
        if not content:
            return Response(successful=False,
                            status_code=HTTP_BAD_REQUEST,
                            description="You must provide text.")
        log = cls.create(content=content,
                         source=source,
                         date=datetime.utcnow())
        if not log:
            return Response(successful=False,
                            statusCode=HTTP_INTERNAL_ERROR,
                            description="The database encountered an " + 
                                        "internal error.")
        return Response(data=log)


    @classmethod
    def clear(cls, id, source):
        log_with_id_response = cls.find(id, source)
        if not log_with_id_response.successful:
            return log_with_id_response
        log_with_id_response.data.delete_instance()
        if not source.logs.exists():
            source.clear_logs()
        return Response(data=log_with_id_response.data)


    @classmethod
    def find(cls, id, source):
        if not id:
            return Response(successful=False,
                            status_code=HHTP_BAD_REQUEST,
                            description="You must provide an id.")
        log_with_id = (cls.select()
                          .where(cls.id == id)
                          .where(cls.source == source))
        if not log_with_id.exists():
            return Response(successful=False,
                            status_code=HTTP_BAD_REQUEST,
                            description="Could not find log with id " + 
                                        "'{id}'.".format(id=id))
        return Response(data=log_with_id.first())


    @classmethod
    def all_json(cls, source):
        logs = [l for l in cls.select().where(cls.source.name == source)]
        if not logs:
            return Response(successful=False,
                            status_code=HTTP_BAD_REQUEST,
                            description="No logs found for '" + 
                                        source + "'")
        return Response(data=ListJSONCollector(logs))


    def modify(self, text):
        if not text:
            return Response(successful=False,
                            description="You must supply text.")
        try:
            self.content = text
            self.save()
            return Response(data=self)
        except Log.DoesNotExist:
            return Response(successful=False,
                            description="Could not update log.")


    def json_object(self):
        return {
            "content" : self.content,
            "date" : self.date.isoformat(),
            "id" : self.id,
        }

