import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import channel

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

@app.route('/channel/invite', methods=['POST'])
def http_channel_invite():
    data = request.get_json()
    response = channel.channel_invite(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

@app.route('/channel/details', methods=['GET'])
def http_channel_details():
    data = request.get_json()
    response = channel.channel_details(data['token'], data['channel_id'])
    return dumps(response)

@app.route('/channel/addowner', methods=['POST'])
def http_channel_addowner():
    data = request.get_json()
    response = channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

@app.route('/channel/removeowner', methods=['POST'])
def http_channel_removeowner():
    data = request.get_json()
    response = channel.channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
