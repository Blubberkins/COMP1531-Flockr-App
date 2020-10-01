import data
import error
def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    # Check channel_id
    num_channels = len(data.data["channels"])
    correct_channel_id = False
    isValid_token = False
    channel_index = 0
    for x in range(num_channels):
        if data.data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check token
            if token in data.data["channels"][x]["channel_id"]:
                isValid_token = True
                break
            break
    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isValid_token == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    # Check whether start > no. messages in channel
    if  start > len(data.data["channels"][channel_index]["messages"]):
        raise InputError("Start is greater than the total number of messages in the channel")
    
    # Initialise return dictionary
    returnDict = {}
    returnDict["messages"] = []
    returnDict["start"] = start
    returnDict["end"] = 50
    num_messages = 50
    if len(data.data["channels"][channel_index]["messages"]) <= 50:
        returnDict["end"] = -1
        num_messages = len(data.data["channels"][channel_index]["messages"])
    for x in range(num_messages):
        returnDict["messages"].append(data.data["channels"][channel_index]["messages"][x])
    return returnDict

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }