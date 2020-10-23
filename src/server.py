import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth

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

@app.route('/auth/login', methods=['POST'])
def http_auth_login():
    data = request.get_json()
    response = auth.auth_login(data['email'], data['password'])
    return dumps(response)

@app.route('/auth/logout', methods=['POST'])
def http_auth_logout():
    data = request.get_json()
    response = auth.auth_logout(data['token'])
    return dumps(response)

@app.route('/auth/register', methods=['POST'])
def http_auth_register():
    data = request.get_json()
    response = auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last'])
    return dumps(response)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
