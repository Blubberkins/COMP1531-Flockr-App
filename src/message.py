from datetime import datetime, timezone
from data import data
from error import AccessError, InputError
import time
import threading

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

def message_sendlater(token, channel_id, message, time_sent):
    """Sends a message later at a time specified by the user.

    Args:
        token: A string which acts an authorisation hash.
        channel_id: An integer associated with a particular channel.
        message: A string which the user wants to send to a particular channel.
        time_sent: An integer representing a specific time which a message will be sent at.

    Raises:
        InputError: When channel ID is not a valid channel.
                    When message is more than 1000 characters.
                    When time sent is a time in the past.
        AccessError: When the user's token is invalid.
                     When the authorised user has not joined the channel they are trying to post to.
    """

    global data

    # Check if token is valid
    if token == "invalid_token":
        raise InputError("Invalid token")
    
    # Check if channel_id is valid
    channel_found = False
    for channel in data["channels"]:
        if channel_id == channel["channel_id"]:
            channel_found = True
            break
    
    if not channel_found:
        raise InputError("Invalid channel")

    # Check message length
    if len(message) > 1000:
        raise InputError("Message is larger than 1000 characters")
    
    # Check time_sent is not in the past 
    # Get the current time
    current_time = datetime.now()
    current_time = current_time.replace(tzinfo=timezone.utc).timestamp()

    if time_sent < current_time:
        raise InputError("Time has already passed")

    # Check if user is part of the channel they want to send a message to
    valid_token = False
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            u_id = user["u_id"]
            break
    for x in range(len(data["channels"])):
        if data["channels"][x]["channel_id"] == channel_id:
            channel_index = x
            break
    for user in data["channels"][channel_index]["all_members"]:
        if user["u_id"] == u_id:
            valid_token = True
            break
    if not valid_token:
        raise AccessError("The user has not joined the channel they are trying to post to")
    
    current_time = datetime.now()
    current_time = current_time.replace(tzinfo=timezone.utc).timestamp()

    time_period = time_sent - current_time
    timer = threading.Timer(time_period, message_send, [token, channel_id, message])
    timer.start()

    message_id = data["num_messages"] - 1

    return {
        "message_id": message_id
    }
