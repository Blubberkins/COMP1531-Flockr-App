import data
import error
def channel_invite(token, channel_id, u_id):
    channel_id_true = 0
    for channel_invited in data['channels']:
        if channel_invited['channel_id'] == channel_id:
            channel_id_true = 1
            break   
    if channel_id_true == 0:
        raise InputError("Invalid channel id")

    for inviter in data['users']:
        if inviter['token'] == token:
            break

    token_true = 0
    for members in channel_invited['all_members']:
        if inviter['u_id'] == members['u_id']:
            token_true = 1
            break
    if token_true == 0:
        raise AccessError("Inviter is not part of this channel")

    for members in channel_invited['all_members']:
        if members['u_id'] == u_id:
            raise InputError("Invitee is already invited to this channel")

    u_id_true = 0
    for invitee in data['users']:
        if invitee['u_id'] == u_id:
            u_id_true = 1
            break
    if u_id_true == 0:
        raise InputError("Invitee does not exist")

    if channel_id_true == 1 and token_true == 1 and u_id_true == 1:
        invitee_member_info = {'u_id' : invitee['u_id'], 'name_first' : invitee['name_first'], 'name_last' : invitee['name_last']}
        channel_invited['all_members'].append(invitee_member_info)

    return {}

def channel_details(token, channel_id):
    channel_id_true = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_id_true = 1
            break   
    if channel_id_true == 0:
        raise InputError("Invalid channel id")

    for user in data['users']:
        if user['token'] == token:
            break

    token_true = 0
    for members in channel['all_members']:
        if user['u_id'] == members['u_id']:
            token_true = 1
            break
    if token_true == 0:
        raise AccessError("User is not part of this channel")

    channel_details_dict = {'name' : channel['name'], 'owner_members' : channel['owner_members'], 'all_members' : channel['all_members']}

    return channel_details_dict

def channel_messages(token, channel_id, start):
    # Check channel_id
    num_users = len(data.data["users"])
    num_channels = len(data.data["channels"])
    u_id = 0
    for x in range(num_users):
        if data.data["users"][x]["token"] == token:
            u_id = data.data["users"][x]["u_id"]
    correct_channel_id = False
    isValid_token = False
    channel_index = 0

    for x in range(num_channels):
        if data.data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check token
            num_members = len(data.data["channels"][x]["all_members"])
            for i in range(num_members):
                if u_id in data.data["channels"][x]["all_members"][i]["u_id"]:
                    isValid_token = True
                    break
            break
    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isValid_token == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    # Check whether start > no. messages in channel
    if  start > len(data.data["channels"][channel_index]["messages"]):
        raise   InputError("Start is greater than the total number of messages in the channel")
    
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
    # Check channel_id
    num_users = len(data.data["users"])
    num_channels = len(data.data["channels"])
    u_id = 0
    for x in range(num_users):
        if data.data["users"][x]["token"] == token:
            u_id = data.data["users"][x]["u_id"]
    correct_channel_id = False
    isValid_token = False
    channel_index = 0
    member_index = 0

    for x in range(num_channels):
        if data.data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check token
            num_members = len(data.data["channels"][x]["all_members"])
            for i in range(num_members):
                if u_id in data.data["channels"][x]["all_members"][i]["u_id"]:
                    member_index = i
                    isValid_token = True
                    break
            break
    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isValid_token == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    # Check if user is an owner_member
    isOwner_Member = False
    num_owners = len(data.data["channels"][channel_index]["owner_members"])
    for owner_index in range(num_owners):
        if u_id in data.data["channels"][channel_index]["owner_members"][owner_index]["u_id"]
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