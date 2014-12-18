from flask import *
from datetime import datetime
import database
from database.Response import Response
from database.Log import Log
from database.Source import Source
import json

app = Flask(__name__)

def body_from_request(request):
    if request.method == "GET" or request.method == "DELETE":
        body = request.args
    else:
        body = request.get_json(force=True, silent=True)
        if body is None:
            body = request.form
    return body

@app.before_request
def parse_body():
    request.body = body_from_request(request)

@app.route("/<source>", methods=["GET", "POST", "DELETE"])
def log(source):
    source_response = Source.find(source)
    if request.method == "GET":
        return source_response.to_flask()
    elif request.method == "POST":
        text = request.body.get("text")
        if not source_response.successful:
            source_response = Source.add(source)
        log = source_response.data.add_log(text)
        return log.to_flask()
    elif request.method == "DELETE":
        if not source_response.successful:
            return source_response.to_flask()
        delete_response = source_response.data.clear_logs()
        return delete_response.to_flask()

@app.route('/<source>/<id>', methods=["GET", "POST", "DELETE"])
def log_id(source, id):
    source_response = Source.find(source)
    if not source_response.successful:
        return source_response.to_flask()
    log_response = Log.find(id, source_response.data)
    if not log_response.successful:
        return log_response.to_flask()
    if request.method == "GET":
        return log_response.to_flask()
    log = log_response.data
    if request.method == "POST":
        text = request.body.get("text", "")
        return log.modify(text).to_flask()
    elif request.method == "DELETE":
        return Log.clear(id, source_response.data).to_flask()

if __name__ == "__main__":
    database.connect()
    app.run(host="localhost", port=4455, debug=True, threaded=True)

