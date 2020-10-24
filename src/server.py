import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import message

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@app.route("/message/send", methods=["POST"])
def http_message_send():
    data = request.get_json()
    response = message.message_send(data["token"], data["channel_id"], data["message"])
    return dumps(response)

@app.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    data = request.get_json()
    response = message.message_remove(data["token"], data["message_id"])
    return dumps(response)

@app.route("/message/edit", methods=['PUT'])
def http_message_edit():
    data = request.get_json()
    response = message.message_edit(data['token'], data['message_id'], data['message'])
    return dumps(response)
if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
