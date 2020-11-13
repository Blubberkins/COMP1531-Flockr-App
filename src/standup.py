from datetime import datetime, timezone, timedelta
import threading
from message import message_sendlater
from data import data
from error import AccessError, InputError

#Token check helper function
def check_token(token, channel):
    token_exist = False
    for user in data['users']:
        if user['token'] == token:
            token_exist = True
            break
    if token_exist == False:
        raise AccessError("Token does not exist")

    token_true = False
    for member in channel['all_members']:
        if user['u_id'] == member['u_id']:
            token_true = True
            break
    if token_true == False:
        raise AccessError("User is not authorised")

#Channel check helper function
def check_channel(channel_id):
    channel_id_true = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel_id_true = True
            break   
    if channel_id_true == False:
        raise InputError("Invalid channel id")
    return channel

#Standup_start timer function
def standup_timer(channel):
    global data
    channel['stand_up']['is_active'] = False
    channel['stand_up']['time_finish'] = None
    

def standup_start(token, channel_id, length):
    global data

    channel = check_channel(channel_id)

    check_token(token, channel)

    if channel['stand_up']['is_active'] == True:
        raise InputError("A stand up is already active") 

    if length <= 0:
        raise InputError("Invalid length of time") 

    end_standup = datetime.now() + timedelta(seconds=length)
    end_standup = end_standup.replace(tzinfo=timezone.utc).timestamp()

    channel['stand_up']['is_active'] = True
    channel['stand_up']['time_finish'] = end_standup

    start_standup = threading.Timer(length, standup_timer, [channel])
    start_standup.start()

    return {"time_finish": end_standup}

def standup_active(token, channel_id):
    channel = check_channel(channel_id)

    check_token(token, channel)

    return {"is_active": channel['stand_up']['is_active'], "time_finish": channel['stand_up']['time_finish']}

def standup_send(token, channel_id, message):
    channel = check_channel(channel_id)

    check_token(token, channel)

    if len(message) > 1000:
        raise InputError("Message is larger than 1000 characters")

    if channel['stand_up']['is_active'] == False:
        raise InputError("There is no active stand up") 

    message_sendlater(token, channel_id, message, channel['stand_up']['time_finish'])

    return {}
    