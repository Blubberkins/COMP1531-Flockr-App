import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import user
import channels

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

@APP.route("/user/profile", methods = ["GET"])
def http_user_profile():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    return dumps(user.user_profile(token, u_id))

@APP.route("/user/profile/setname", methods = ["PUT"])
def http_user_profile_setname():
    data = request.get_json()
    response = user.user_profile_setname(data["token"], data["name_first"], data["name_last"])
    return dumps(response)

@APP.route("/user/profile/setemail", methods = ["PUT"])
def http_user_profile_setemail():
    data = request.get_json()
    response = user.user_profile_setemail(data["token"], data["email"])
    return dumps(response)

@APP.route("/user/profile/sethandle", methods = ["PUT"])
def http_user_profile_sethandle():
    data = request.get_json()
    response = user.user_profile_sethandle(data["token"], data["handle"])

@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    response = channels.channels_list(request.args.get('token'))
    return dumps(response)

@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    response = channels.channels_listall(request.args.get('token'))
    return dumps(response)

@APP.route("/channels/create", methods=['POST'])
def http_channels_create():
    data = request.get_json()
    response = channels.channels_create(data['token'], data['name'], data['is_public'])
    return dumps(response)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port

