from datetime import datetime, timezone
from data import data
from error import AccessError, InputError
from channel import channel_messages

def message_send(token, channel_id, message):
    global data
    # Check InputError
    valid_channel_id = False
    channel_index = 0
    '''for channels in data["channels"]:
        if channels["channel_id"] == channel_id:
            valid_channel_id = True
            channel_index = channels
            break'''
    for x in range(len(data["channels"])):
        if data["channels"][x]["channel_id"] == channel_id:
            valid_channel_id = True
            channel_index = x
            break
    if not valid_channel_id:
        raise InputError("Invalid channel")
    if len(message) > 1000:
        raise InputError("Message is larger than 1000 characters")

    # Check AccessError
    valid_token = False
    u_id = -1
    for users in data["users"]:
        if users["token"] == token:
            u_id = users["u_id"]
            break
    for users in data["channels"][channel_index]["all_members"]:
        if users["u_id"] == u_id:
            valid_token = True
            break
    if not valid_token:
        raise AccessError("The user has not joined the channel they are trying to post to")

    # Add message
    message_dict = {}
    current_time = datetime.now()
    current_time = current_time.replace(tzinfo=timezone.utc).timestamp()
    message_dict["time_created"] = current_time
    message_dict["message_id"] = data["num_messages"]
    return_dict = {}
    return_dict["message_id"] = data["num_messages"]
    message_dict["u_id"] = u_id
    message_dict["message"] = message
    # Add channel_id data for database
    message_dict["channel_id"] = channel_id
    data["messages"].append(message_dict)
    # Remove channel_id key for return value
    #return_dict.pop("channel_id")
    data["num_messages"] += 1
    return return_dict

def message_remove(token, message_id):
    global data
    # Check Input Error
    does_message_exist = False
    message_index = 0
    for x in range(len(data["messages"])):
        if data["messages"][x]["message_id"] == message_id:
            does_message_exist = True
            message_index = x
            break
    if not does_message_exist:
        raise InputError("Message has already been deleted")

    # Check AccessError
    u_id = -1
    u_id_permission = -1
    for users in data["users"]:
        if users["token"] == token:
            u_id = users["u_id"]
            u_id_permission = users["permission_id"]
            break
    message_owner_or_flock_owner = False
    if data["messages"][message_index]["u_id"] == u_id:
        message_owner_or_flock_owner = True
    if u_id_permission == 1:
        message_owner_or_flock_owner = True
    if not message_owner_or_flock_owner:
        raise AccessError("User is not a flock owner or the original user who sent the message")

    data["messages"].pop(message_index)
    return {}

def message_edit(token, message_id, message):
    global data
    # Check message length
    if len(message) > 1000:
        raise InputError("Message is larger than 1000 characters")

    # Check AccessError
    u_id = -1
    u_id_permission = -1
    for users in data["users"]:
        if users["token"] == token:
            u_id = users["u_id"]
            u_id_permission = users["permission_id"] 
            break
    message_owner_or_flock_owner = False
    message_index = -1
    for x in range(len(data["messages"])):
        if data["messages"][x]["message_id"] == message_id:
            message_index = x
            break
    if data["messages"][message_index]["u_id"] == u_id:
        message_owner_or_flock_owner = True
    if u_id_permission == 1:
        message_owner_or_flock_owner = True
    if not message_owner_or_flock_owner:
        raise AccessError("User is not a flock owner or the original user who sent the message")

    if message == "":
        return message_remove(token, message_id)
    data["messages"][message_index]["message"] = message
    return {}
    
def message_react(token, message_id, react_id):
    global data

    # Test whether the react_id is 1
    if react_id != 1:
        raise InputError("Invalid react ID")

    # Test whether message exists
    message_index = -1
    message_channel_id = -1
    is_real_message = False
    for x in range(len(data["messages"])):
        if data["messages"][x]["message_id"] == message_id:
            is_real_message = True
            message_index = x
            message_channel_id = data["messages"][x]["channel_id"]
            break
    if not is_real_message:
        raise InputError("Specified message does not exist")

    # Test whether the user is allowed to react to that message
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            user["u_id"] = u_id
            break
    
    is_in_channel = False
    for x in range(len(data["channels"])):
        if data["channels"][x]["channel_id"] == message_channel_id:
            for index in range(len(data["channels"][x]["all_members"])):
                if data["channels"][x]["all_members"][index]["u_id"] == u_id:
                    is_in_channel = True
                    break
            break
    if not is_in_channel:
        raise InputError("User is not currently in the channel of the message they are trying to react to")

    # Test whether the message is already reacted by the user
    is_reacted = False
    for message in data["messages"]:
        if message["message_id"] == message_id:
            if u_id in message["reacted_by"]:
                is_reacted = True
                break
    if is_reacted:
        raise InputError("User has already reacted to this message")

    # Add user to reacted_by
    for message in data["messages"]:
        if message["message_id"] == message_id:
            message["reacted_by"].append(u_id)
            break
    
    return {}

def message_unreact(token, message_id, react_id):
    global data

    # Test whether the react_id is 1
    if react_id != 1:
        raise InputError("Invalid react ID")

    # Test whether message exists
    message_index = -1
    message_channel_id = -1
    is_real_message = False
    for x in range(len(data["messages"])):
        if data["messages"][x]["message_id"] == message_id:
            is_real_message = True
            message_index = x
            message_channel_id = data["messages"][x]["channel_id"]
            break
    if not is_real_message:
        raise InputError("Specified message does not exist")

    # Test whether the user is allowed to react to that message
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            user["u_id"] = u_id
            break
    
    is_in_channel = False
    for x in range(len(data["channels"])):
        if data["channels"][x]["channel_id"] == message_channel_id:
            for index in range(len(data["channels"][x]["all_members"])):
                if data["channels"][x]["all_members"][index]["u_id"] == u_id:
                    is_in_channel = True
                    break
            break
    if not is_in_channel:
        raise InputError("User is not currently in the channel of the message they are trying to react to")

    # Test whether the message is already reacted by the user
    is_reacted = False
    for message in data["messages"]:
        if message["message_id"] == message_id:
            if u_id in message["reacted_by"]:
                is_reacted = True
                break
    if not is_reacted:
        raise InputError("User has not reacted to this message yet")

    # Remove user from reacted_by
    for message in data["messages"]:
        if message["message_id"] == message_id:
            message["reacted_by"].remove(u_id)
            break

    return {}




