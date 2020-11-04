from data import data
from error import InputError
from error import AccessError

def clear():
    """ Clears all data stored in the data file """

    global data
    data["users"].clear()
    data["channels"].clear()
    data["members"].clear()
    data["messages"].clear()
    data["num_messages"] = 0

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

    global data
    
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
        
        all_users = {
            'users': users_list
        }

    return all_users

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

    if permission_id != 1 or permission_id != 2:
        raise InputError("Permission id is not valid")

    token_exist = False
    for user in data['users']:
        if user['token'] == token:
            token_exist = True
            break
    if token_exist == False:
        raise AccessError("Token does not exist")
    
    if user['permission_id'] == 2:
        raise AccessError("User is not authorised")
    
    u_id_true = False
    for member in data['users']:
        if member['u_id'] == u_id:
            u_id_true = True
            break
    if u_id_true == False:
        raise InputError("Target does not exist")

    member['permission_id'] = permission_id
    
    return {}

def search(token, query_str):
    """
    Given a query string, return a collection of messages in all of the channels that the user has joined that match the query
        Args:
            token: String which is used as an authorisation hash
            query_str: String that is being searched for
        Return:
            search_results: A list of dictionaries containing info on all the messages that match the search query
    """

    # checking for valid token
    token_exist = False
    for user in data['users']:

        if user['token'] == token:
            token_exist = True
            break

    if token_exist == False:
        raise AccessError("Token does not exist")

    # retrieve and store the u_id of the user
    u_id = 0
    for x in data['users']:

        if x['token'] == token:
            u_id = x['u_id']
            break

    # define a list of channel_ids from the channels the user has joined
    joined_channel_ids = []

    # x loops through each channel
    for x in data['channels']:

        # y loops through each member in all_members
        for y in x['all_members']:

            # if the user is a member of the channel, add the channel id to joined_channel_ids and loop to the next channel
            if y['u_id'] == u_id:
                joined_channel_ids.append(x['channel_id'])
                break

    # define a list of dictionaries containing the search results that will be returned by the function
    search_results = {'messages' : []}

    # x loops through each message
    for x in data['messages']:

        # if the search string appears in the message
        if query_str in x['message']:

            # y loops through the user's joined channel ids
            for y in joined_channel_ids:

                # if the message was sent in a channel the user has joined, add the message info to search_results and loop to the next message
                if x['channel_id'] == y:
                    search_results['messages'].append({
                        'message_id': x['message_id'],
                        'u_id': x['u_id'],
                        'message': x['message'],
                        'time_created': x['time_created']
                    })
                    break

    return search_results