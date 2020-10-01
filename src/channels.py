import data
import auth
from error import InputError

def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):
    
    # raises InputError if channel name is longer than 20 characters
    if len(name) > 20:
        raise InputError("Name is more than 20 characters long.")

    new_channel = {
        "channel_id": len(data.data['channels']) + 1,
        "name" : name,
        "public" : is_public,
        "owners" : token,
        "members" : token
    }

    # add the new channel to the data file
    data.data['channels'].append(new_channel)

    return {
        'channel_id' : new_channel["channel_id"]
    }
