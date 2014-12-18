__author__ = 'harlanhaskins'


class ListJSONCollector():
    """
    An encapsulation of a list, allowing for json_object export
    """

    def __init__(self, collection):
        self.collection = collection

    def json_object(self):
        return [e.json_object() for e in self.collection]
