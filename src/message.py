from datetime import datetime, timezone
from data import data
from error import AccessError, InputError

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
    return_dict = {}
    current_time = datetime.now()
    current_time = current_time.replace(tzinfo=timezone.utc).timestamp()
    return_dict["time_created"] = current_time
    return_dict["message_id"] = data["num_messages"]
    return_dict["u_id"] = u_id
    return_dict["message"] = message
    # Add channel_id data for database
    return_dict["channel_id"] = channel_id
    data["messages"].append(return_dict)
    # Remove channel_id key for return value
    return_dict.pop("channel_id")
    data["num_messages"] += 1
    return return_dict

def message_remove(token, message_id):
    global data
    # Check Input Error
    does_message_exist = False
    message_index = 0
    for messages in data["messages"]:
        if messages["message_id"] == message_id:
            does_message_exist = True
            message_index = messages
            break
    if not does_message_exist:
        raise InputError("Message has already been deleted")

    # Check AccessError
    u_id = -1
    u_id_permission = -1
    for users in data["users"]:
        if users["token"] == token:
            u_id = users["u_id"]
            users["permission_id"] = u_id_permission
            break
    message_owner_or_flock_owner = False
    if data["messages"][message_index]["u_id"] == u_id:
        message_owner_or_flock_owner = True
    if u_id_permission == 1:
        message_owner_or_flock_owner = True
    if not message_owner_or_flock_owner:
        raise AccessError("User is not a flock owner or the original user who sent the message")

    data["messages"].pop(message_index)
    return {
    }

def message_edit(token, message_id, message):
    # Check message length
    if len(message) > 1000:
        raise InputError("Message is larger than 1000 characters")

    # Check AccessError
    u_id = -1
    u_id_permission = -1
    for users in data["users"]:
        if users["token"] == token:
            u_id = users["u_id"]
            users["permission_id"] = u_id_permission
            break
    message_owner_or_flock_owner = False
    message_index = -1
    for messages in data["messages"]:
        if messages["message_id"] == message_id:
            message_index = messages
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
    return {
    }
    