from data import data
import auth
from error import InputError

def channels_list(token):
    """
    Provide a list of all channels (and their associated details) that the authorised user is part of
        Args:
            token: String which is used as an authorisation hash
        Return:
            channels: List of dictionaries, where each dictionary contains types { channel_id, name }
    """

    global data

    # retrieve and store the u_id of the user
    u_id = 0
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
    """
    Provide a list of all channels (and their associated details)
        Args:
            token: String which is used as an authorisation hash
        Return:
            all_channels: List of dictionaries, where each dictionary contains types { channel_id, name }
    """

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
    """
    Creates a new channel with that name that is either a public or private channel
        Args:
            token: String which is used as an authorisation hash
            name: Name of the channel
            is_public: Boolean which states whether the channel is public or not
        Return:
            channels: List of dictionaries, where each dictionary contains types { channel_id, name }
        Raises:
            InputError: An error that occurs when the channel name is longer than 20 characters
    """

    global data

    # raises InputError if channel name is longer than 20 characters
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long.")
    
    # initialise variables
    u_id = -1
    name_first = ''
    name_last = ''
    profile_img_url = ''
    
    # find corresponding u_id, first name and last name of token
    for x in data['users']:

        if x["token"] == token:
            u_id = x['u_id']
            name_first = x['name_first']
            name_last = x['name_last']
            profile_img_url = x['profile_img_url']
            break

    # adding channel info
    new_channel = {
        'channel_id': len(data['channels']) + 1,
        'name': name,
        'is_public': is_public,
        'owner_members': [{"u_id": u_id, 'name_first': name_first, 'name_last': name_last, 'profile_img_url': profile_img_url}],
        'all_members': [{"u_id": u_id, 'name_first': name_first, 'name_last': name_last, 'profile_img_url': profile_img_url}],
        'stand_up' : {'is_active': False, 'time_finish': None}
    }

    # add the new channel to the data file
    data['channels'].append(new_channel)

    return {
        'channel_id' : new_channel["channel_id"]
    }

