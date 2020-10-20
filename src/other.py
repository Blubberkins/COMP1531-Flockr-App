from data import data

def clear():
    global data
    data["users"].clear()
    data["channels"].clear()
    data["members"].clear()

def users_all(token):
    """
    Returns a list of all users in the Flockr
        Args:
            token: String which is used as an authorisation hash
        Return:
            user_list: A list of all users
        Raises:
            AccessError: An error that occurs when token is invalid or the user is not authorised
    """
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
    """
    Changes the global permissions a user has access to
        Args:
            token: String which is used as an authorisation hash
            u_id: An integer which is used to identify a user
            permission_id: An integer which defines what global permissions a user has access to
        Raises:
            InputError: An error that occurs when either u_id or permission_id is invalid
            AccessError: An error that occurs when token is invalid or the user is not authorised
    """
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

def admin_userpermission_change(token, u_id, permission_id):
    pass

def search(token, query_str):
    token_exist = False
    for user in data['users']:
        if user['token'] == token:
            token_exist = True
            break
    if token_exist == False:
        raise AccessError("Token does not exist")

    u_id = 0
    # retrieve and store the u_id of the user
    for x in data['users']:

        if x['token'] == token:
            u_id = x['u_id']
            break

    

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
