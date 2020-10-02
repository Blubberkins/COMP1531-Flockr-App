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
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

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