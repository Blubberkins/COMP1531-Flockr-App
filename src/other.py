from data import data
from error import AccessError, InputError

def clear():
    global data
    data["users"].clear()
    data["channels"].clear()
    data["members"].clear()

def clear():
    global data
    data["users"].clear()
    data["channels"].clear()
    data["members"].clear()

def users_all(token):
    token_exist = False
    for user in data['users']:
        if user['token'] == token:
            token_exist = True
            break
    if token_exist == False:
        raise AccessError("Token does not exist")

    users_list = []
    for user in data['users']:
        user_dict = {
            "u_id": user['u_id'],
            "email": user['email'],
            "name_first": user['name_first'],
            "name_last": user['name_last'],
            "handle_str": user['handle_str']
        }
        users_list.append(user_dict)

    return users_list

def admin_userpermission_change(token, u_id, permission_id):
    global data

    token_exist = False
    for user in data['users']:
        if user['token'] == token:
            token_exist = True
            break
    if token_exist == False:
        raise AccessError("Token does not exist")
    
    token_true = False
    if user['permission_id'] == 1:
        token_true = True
    if token_true == False:
        raise AccessError("Authorised user does not have permission")

    for member in data['users']:
        if member['u_id'] == u_id:
            u_id_true = True
            break
    if u_id_true == False:
        raise InputError("User does not exist")

    if permission_id != 1 and permission_id != 2:
        raise InputError("Permission id does not exist")

    member['permission_id'] = permission_id

def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }