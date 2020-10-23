import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import other

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

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    data = request.get_json()
    response = other.users_all(data['token'])
    return dumps(response)

@APP.route("/admin/userpermission/change", methods=['POST'])
def http_admin_userpermission_change():
    data = request.get_json()
    response = other.admin_userpermission_change(data['token'], data['u_id'], data['permission_id'])
    return dumps(response)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
