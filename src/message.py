from datetime import datetime, timezone
import threading
from data import data
from error import AccessError, InputError

def message_send(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id
        Args:
            token: String which is used as an authorisation hash
            channel_id: Integer number of the channel the message is to be sent to
            message: A string of the message to be sent
        Raises:
    '''
    global data
    # Check InputError
    valid_channel_id = False
    for channel in data["channels"]:
        if channel["channel_id"] == channel_id:
            valid_channel_id = True
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
    for users in channel["all_members"]:
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
    message_dict["u_id"] = u_id
    message_dict["message"] = message

    # Add channel_id data for database
    message_dict["channel_id"] = channel_id
    message_dict["is_pinned"] = False
    message_dict["reacted_by"] = []
    return_dict = {}
    return_dict["message_id"] = data["num_messages"]
    data["messages"].append(message_dict)
    data["num_messages"] += 1
    return return_dict

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel
        Args:
            token: String which is used as an authorisation hash
            message_id: Integer which is used as a unique identifier for a message
        Raises:
    '''

    global data
    # Check Input Error
    does_message_exist = False
    for msg in data["messages"]:
        if msg["message_id"] == message_id:
            does_message_exist = True
            break
    if not does_message_exist:
        raise InputError("Message has already been deleted")

    # Check AccessError
    message_owner_or_flock_owner = False
    for users in data["users"]:
        if users["token"] == token:
            if msg["u_id"] == users['u_id']:
                message_owner_or_flock_owner = True
            if users['permission_id'] == 1:
                message_owner_or_flock_owner = True
            break
    if not message_owner_or_flock_owner:
        raise AccessError("User is not a flock owner or the original user who sent the message")

    data["messages"].remove(msg)
    return {}

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted.
    '''

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
    for msg in data["messages"]:
        if msg["message_id"] == message_id:
            if msg["u_id"] == u_id:
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
    '''
    Given a message within a channel the authorised user is part of, add a "react" to that particular message
    '''

    global data

    # Test whether the react_id is 1
    if react_id != 1:
        raise InputError("Invalid react ID")

    # Test whether message exists
    is_real_message = False
    message_channel_id = -1
    for msg in data["messages"]:
        if msg["message_id"] == message_id:
            is_real_message = True
            message_channel_id = msg["channel_id"]
            break
    if not is_real_message:
        raise InputError("Specified message does not exist")

    # Test whether the user is allowed to react to that message
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            u_id = user["u_id"] 
            break
    
    is_in_channel = False
    for channel in data["channels"]:
        if channel["channel_id"] == message_channel_id:
            for users in channel["all_members"]:
                if users["u_id"] == u_id:
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
    '''
    Given a message within a channel the authorised user is part of, remove a "react" to that particular message
    '''

    global data

    # Test whether the react_id is 1
    if react_id != 1:
        raise InputError("Invalid react ID")

    # Test whether message exists
    is_real_message = False
    message_channel_id = -1
    for msg in data["messages"]:
        if msg["message_id"] == message_id:
            is_real_message = True
            message_channel_id = msg["channel_id"]
            break
    if not is_real_message:
        raise InputError("Specified message does not exist")

    # Test whether the user is allowed to react to that message
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            u_id = user["u_id"] 
            break
    
    is_in_channel = False
    for channel in data["channels"]:
        if channel["channel_id"] == message_channel_id:
            for users in channel["all_members"]:
                if users["u_id"] == u_id:
                    is_in_channel = True
                    break
            break
    if not is_in_channel:
        raise InputError("User is not currently in the channel of the message they are trying to react to")

    # Test whether the message is not already reacted by the user
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

def message_pin(token, message_id):
    """
    Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend
        Args:
            token: String which is used as an authorisation hash
            message_id: Integer which is used as a unique identifier for a message
        Raises:
            InputError: An error that occurs when message_id is not a valid message or message with ID message_id is already pinned
            AccessError: An error that occurs when the user is not a member of the channel that the message is within or the user is not an owner of the channel
    """

    # checking for valid token and retrieving user id
    token_exist = False
    u_id = -1
    for user in data["users"]:

        if user["token"] == token:
            token_exist = True
            u_id = user["u_id"]
            break

    if token_exist == False:
        raise AccessError("Token does not exist")

    # checking for valid message and whether message is already pinned, and retrieving channel id for the channel the message is sent in
    message_exist = False
    is_pinned = False
    for message in data['messages']:

        if message_id == message['message_id']:

            if message['is_pinned'] == True:
                is_pinned = True

            message_exist = True
            channel_id = message['channel_id']
            break

    if message_exist == False:
        raise InputError("Message is not a valid message")

    if is_pinned == True:
        raise InputError("Message is already pinned")

    # checking if user is an owner in the channel the message is in
    is_owner = False
    for channel in data['channels']:

        if channel_id == channel['channel_id']:
            
            for user in channel['owner_members']:

                if u_id == user['u_id']:
                    is_owner = True
                    break

            break

    if is_owner == False:
        raise AccessError("User is not a member of the channel or an owner in the channel")

    # pin message if above errors aren't raised
    for message in data['messages']:

        if message_id == message['message_id']:
            message['is_pinned'] = True
            break

    return {}

def message_unpin(token, message_id):
    """
    Given a message within a channel, remove it's mark as unpinned
        Args:
            token: String which is used as an authorisation hash
            message_id: Integer which is used as a unique identifier for a message
        Raises:
            InputError: An error that occurs when message_id is not a valid message or message with ID message_id is already unpinned
            AccessError: An error that occurs when the user is not a member of the channel that the message is within or the user is not an owner of the channel
    """

    # checking for valid token and retrieving user id
    token_exist = False
    u_id = -1
    for user in data["users"]:

        if user["token"] == token:
            token_exist = True
            u_id = user["u_id"]
            break

    if token_exist == False:
        raise AccessError("Token does not exist")

    # checking for valid message and whether message is already pinned, and retrieving channel id for the channel the message is sent in
    message_exist = False
    is_unpinned = False
    for message in data['messages']:

        if message_id == message['message_id']:

            if message['is_pinned'] == False:
                is_unpinned = True

            message_exist = True
            channel_id = message['channel_id']
            break

    if message_exist == False:
        raise InputError("Message is not a valid message")

    if is_unpinned == True:
        raise InputError("Message is already unpinned")

    # checking if user is an owner in the channel the message is in
    is_owner = False
    for channel in data['channels']:

        if channel_id == channel['channel_id']:
            
            for user in channel['owner_members']:

                if u_id == user['u_id']:
                    is_owner = True
                    break

            break

    if is_owner == False:
        raise AccessError("User is not a member of the channel or an owner in the channel")

    # unpin message if above errors aren't raised
    for message in data['messages']:

        if message_id == message['message_id']:
            message['is_pinned'] = False
            break

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
    valid_token = False
    for user in data["users"]:
        if token == user["token"]:
            valid_token = True
            break
    if not valid_token:
        raise AccessError("Invalid permissions")
    
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
    is_user_in_channel = False
    u_id = -1
    for user in data["users"]:
        if user["token"] == token:
            u_id = user["u_id"]
            break
    for channel in data["channels"]:
        if channel == channel["channel_id"]:
            for user in channel["all_members"]:
                if u_id == user["u_id"]:
                    is_user_in_channel = True
                    break
   
    if not is_user_in_channel:
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
    
