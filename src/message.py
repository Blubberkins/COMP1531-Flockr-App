from datetime import datetime, timezone
from data import data
import channel
import channels
from error import AccessError, InputError

def message_send(token, channel_id, message):
    global data
    # Check InputError
    valid_channel_id = False
    channel_index = 0
    for channels in data["channels"]:
        if channels["channel_id"] == channel_id:
            index = channels
            break
    if valid_channel_id == False:
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
    for users in data["channels"][channel_index]:
        if users["u_id"] == u_id:
            valid_token == True
            break
    if valid_token == False:
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
    return return_dict

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }