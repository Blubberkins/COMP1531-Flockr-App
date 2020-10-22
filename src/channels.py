from data import data
import auth
from error import InputError

def channels_list(token):
    global data
    u_id = 0
    # retrieve and store the u_id of the user
    for x in data['users']:

        if x['token'] == token:
            u_id = x['u_id']
            break

    # create the dictionary to be returned by the function
    channels = {
        "channels" : []
    }

    # for each existing channel
    for x in data['channels']:
        # create a dictionary containing data about the channel
        channel_data = {"channel_id" : x['channel_id'], "name" : x['name']}

        is_member = False
        # check if the user is a member of the channel
        for y in x['all_members']:

            if y['u_id'] == u_id:
                is_member = True
                break
        
        # if the user is a member add the channel data to channels
        if is_member == True:
            channels['channels'].append(channel_data)
    
    return channels

def channels_listall(token):
    global data

    # create the dictionary to be returned by the function
    all_channels = {
        "channels" : []
    }

    for x in data['channels']:
        # create a dictionary containing data about the channel
        channel_data = {"channel_id" : x['channel_id'], "name" : x['name']}

        all_channels['channels'].append(channel_data)

    return all_channels

def channels_create(token, name, is_public):
    global data
    # raises InputError if channel name is longer than 20 characters
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long.")
    # find corresponding u_id, first name and last name of token
    num_users = len (data["users"])
    u_id = -1
    name_first = ''
    name_last = ''
    for x in range(num_users):
        if data["users"][x]["token"] == token:
            u_id = data['users'][x]['u_id']
            name_first = data['users'][x]['name_first']
            name_last = data['users'][x]['name_last']
            break

    new_channel = {}
    new_channel['channel_id'] = len(data['channels']) + 1
    new_channel['name'] = name 
    new_channel['is_public'] = is_public
    new_channel['owner_members'] = [{"u_id": u_id, 'name_first': name_first, 'name_last': name_last}]
    new_channel['all_members'] = [{"u_id": u_id, 'name_first': name_first, 'name_last': name_last}]
    new_channel['messages'] = [{}]

    # add the new channel to the data file
    data['channels'].append(new_channel)

    return {
        'channel_id' : new_channel["channel_id"]
    }
