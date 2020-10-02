from data import data
import error
def channel_invite(token, channel_id, u_id):
    global data
    channel_id_true = 0
    for channel_invited in data['channels']:
        if channel_invited['channel_id'] == channel_id:
            channel_id_true = True
            break   
    if channel_id_true == False:
        raise InputError("Invalid channel id")

    for inviter in data['users']:
        if inviter['token'] == token:
            break

    token_true = False
    for members in channel_invited['all_members']:
        if inviter['u_id'] == members['u_id']:
            token_true = True
            break
    if token_true == False:
        raise AccessError("Inviter is not part of this channel")

    for members in channel_invited['all_members']:
        if members['u_id'] == u_id:
            raise InputError("Invitee is already invited to this channel")

    u_id_true = False
    for invitee in data['users']:
        if invitee['u_id'] == u_id:
            u_id_true = True
            break
    if u_id_true == False:
        raise InputError("Invitee does not exist")

    if channel_id_true == True and token_true == True and u_id_true == True:
        invitee_member_info = {'u_id' : invitee['u_id'], 'name_first' : invitee['name_first'], 'name_last' : invitee['name_last']}
        channel_invited['all_members'].append(invitee_member_info)

    return {}

def channel_details(token, channel_id):
    global data
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
    global data
    # Check channel_id
    num_users = len(data["users"])
    num_channels = len(data["channels"])
    u_id = 0
    for x in range(num_users):
        if data["users"][x]["token"] == token:
            u_id = data["users"][x]["u_id"]
    correct_channel_id = False
    isValid_token = False
    channel_index = -1

    for x in range(num_channels):
        if data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check token
            num_members = len(data["channels"][x]["all_members"])
            for i in range(num_members):
                if u_id in data["channels"][x]["all_members"][i]["u_id"]:
                    isValid_token = True
                    break
            break
    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isValid_token == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    # Check whether start > no. messages in channel
    if  start > len(data["channels"][channel_index]["messages"]):
        raise   InputError("Start is greater than the total number of messages in the channel")
    
    # Initialise return dictionary
    returnDict = {}
    returnDict["messages"] = []
    returnDict["start"] = start
    returnDict["end"] = 50
    num_messages = 50
    if len(data["channels"][channel_index]["messages"]) <= 50:
        returnDict["end"] = -1
        num_messages = len(data["channels"][channel_index]["messages"])
    for x in range(num_messages):
        returnDict["messages"].append(data["channels"][channel_index]["messages"][x])
    return returnDict

def channel_leave(token, channel_id):
    global data
    # Check channel_id
    num_users = len(data["users"])
    num_channels = len(data["channels"])
    u_id = 0
    for x in range(num_users):
        if data["users"][x]["token"] == token:
            u_id = data["users"][x]["u_id"]
    correct_channel_id = False
    isValid_token = False
    channel_index = -1
    member_index = -1

    for x in range(num_channels):
        if data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check token
            num_members = len(data["channels"][x]["all_members"])
            for i in range(num_members):
                if data["channels"][x]["all_members"][i]["u_id"] == u_id:
                    member_index = i
                    isValid_token = True
                    break
            break
    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isValid_token == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    # Check if user is an owner_member
    num_owners = len(data["channels"][channel_index]["owner_members"])
    for owner_index in range(num_owners):
        if data["channels"][channel_index]["owner_members"][owner_index]["u_id"] == u_id:
            remove_target = data["channels"][channel_index]["owner_members"][owner_index]
            data["channels"][channel_index]["owner_members"].remove(remove_target)
            break
    # Remove member
    remove_target = data["channels"][x]["all_members"][member_index]
    data["channels"][x]["all_members"].remove(remove_target)
    return {}

def channel_join(token, channel_id):
    global data
    # Check channel id
    num_channels = len(data["channels"])
    isChannelPublic = True
    correct_channel_id = False
    channel_index = -1
    for x in range(num_channels):
        if data["channels"][x]["channel_id"] == channel_id:
            correct_channel_id = True
            channel_index = x
            # Check if the channel is private
            if data["channels"][x]["is_public"] == False:
                isChannelPublic = False
                break
            break

    if correct_channel_id == False:
        raise InputError("Channel ID is not a valid channel")
    if isChannelPublic == False:
        raise AccessError("Channel is private")
    # Add user to channel
    num_users = len(data["users"])
    user_dictionary = {}
    for x in range(num_users):
        if data["users"][x]["token"] == token:
            user_dictionary = data["users"][x]
            break
    data["channels"][channel_index]["all_members"].append(user_dictionary)
    return {}

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }