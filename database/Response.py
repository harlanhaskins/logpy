__author__ = 'harlanhaskins'
from flask import Response as FlaskResponse
import json

# HTTP Status Codes
HTTP_OK = 200
HTTP_NO_DATA = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_INTERNAL_ERROR = 500


class Response:
    """
    A response is composed of three parts: a boolean success, an HTTP status
    code, a string description of the response, and relevant data. This object
    is returned from all dbapi methods.
    """
    __slots__ = ('successful', 'status_code', 'description', 'data')

    def __init__(self, successful=True, status_code=HTTP_OK, description=None,
                 data=None):
        self.successful = successful
        self.status_code = status_code
        self.description = description
        self.data = data

    def json_object(self):
        """
        json_object returns a dictionary representation of a json object.
        A fruitful response will simply return the data. All other responses
        will include a status. Messages will be included for failing responses.
        """
        if self.data is not None:
            return self.data.json_object()

        dict = {'success': self.successful}
        if self.description:
            dict['message'] = self.description
        return dict

    def to_flask(self):
        headers = {'Content-Type': 'application/json'}
        flask_response = FlaskResponse(json.dumps(self.json_object()),
                                       self.status_code, headers=headers)
        return flask_response
