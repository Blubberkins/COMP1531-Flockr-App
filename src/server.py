import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import channel

import message
import auth
import other
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

@APP.route('/channel/invite', methods=['POST'])
def http_channel_invite():
    data = request.get_json()
    response = channel.channel_invite(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

@APP.route('/channel/details', methods=['GET'])
def http_channel_details():
    response = channel.channel_details(request.args.get('token'), request.args.get('channel_id'))
    return dumps(response)

@APP.route('/channel/addowner', methods=['POST'])
def http_channel_addowner():
    data = request.get_json()
    response = channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

@APP.route('/channel/removeowner', methods=['POST'])
def http_channel_removeowner():
    data = request.get_json()
    response = channel.channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(response)

@APP.route('/channel/messages', methods=['GET'])
def http_channel_messages():
    response = channel.channel_messages(request.args.get("token"), request.args.get("channel_id"), request.args.get("start"))
    return dumps(response)

@APP.route('/channel/leave', methods=['POST'])
def http_channel_leave():
    data = request.get_json()
    response = channel.channel_leave(data["token"], data["channel_id"])
    return dumps(response)

@APP.route('/channel/join', methods=["POST"])
def http_channel_join():
    data = request.get_json()
    response = channel.channel_join(data["token"], data["channel_id"])

@APP.route("/message/send", methods=["POST"])
def http_message_send():
    data = request.get_json()
    response = message.message_send(data["token"], data["channel_id"], data["message"])
    return dumps(response)

@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    data = request.get_json()
    response = message.message_remove(data["token"], data["message_id"])
    return dumps(response)

@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    data = request.get_json()
    response = message.message_edit(data['token'], data['message_id'], data['message'])
    return dumps(response)

@APP.route('/auth/login', methods=['POST'])
def http_auth_login():
    data = request.get_json()
    response = auth.auth_login(data['email'], data['password'])
    return dumps(response)

@APP.route('/auth/logout', methods=['POST'])
def http_auth_logout():
    data = request.get_json()
    response = auth.auth_logout(data['token'])
    return dumps(response)

@APP.route('/auth/register', methods=['POST'])
def http_auth_register():
    data = request.get_json()
    response = auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last'])

@APP.route("/users/all", methods=['GET'])
def http_users_all():
    response = other.users_all(request.args.get('token'))
    return dumps(response)

@APP.route("/admin/userpermission/change", methods=['POST'])
def http_admin_userpermission_change():
    data = request.get_json()
    response = other.admin_userpermission_change(data['token'], data['u_id'], data['permission_id'])
    return dumps(response)

@APP.route("/search", methods=['GET'])
def http_search():
    response = other.search(request.args.get('token'), request.args.get('query_str'))

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

