import pytest
import channel
import channels
import auth
import message
from other import clear
from error import InputError
from error import AccessError
# Test functions for channel_invite
def test_channel_invite_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    invalid_channel_id = -1
    invalid_u_id = -1

    with pytest.raises(InputError):
        channel.channel_invite(login_owner['token'], invalid_channel_id, login_user['u_id'])
        channel.channel_invite(login_owner['token'], channel_id['channel_id'], invalid_u_id)
        channel.channel_invite(login_owner['token'], invalid_channel_id, invalid_u_id)

def test_channel_invite_already_member():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        channel.channel_invite(login_owner['token'], channel_id, login_owner['u_id'])

def test_channel_invite_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError):
        channel.channel_invite("", channel_id['channel_id'], login_user['u_id'])
        channel.channel_invite(login_user['token'], channel_id['channel_id'], login_owner['u_id'])

def test_channel_invite_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channel_details = channel.channel_details(login_owner['token'], channel_id['channel_id'])
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_details
def test_channel_details_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = -1

    with pytest.raises(InputError):
        channel.channel_details(login_owner['token'], invalid_channel_id)

def test_channel_details_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError):
        channel.channel_details(login_user['token'], channel_id['channel_id'])
        channel.channel_details("", channel_id['channel_id'])

def test_channel_details_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    channel_details = channel.channel_details(login_owner['token'], channel_id['channel_id'])
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channel_details = channel.channel_details(login_user['token'], channel_id['channel_id'])
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_messages
def test_channel_messages_invalid_start_index():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel_id2 = channels.channels_create(login_owner['token'], "channel", True)
    
    message.message_send(login_owner['token'], channel_id2["channel_id"], 'example message')

    with pytest.raises(InputError):
        channel.channel_messages(login_owner['token'], channel_id['channel_id'], 0)
        channel.channel_messages(login_owner['token'], channel_id2['channel_id'], 1)


def test_channel_messages_invalid_channel():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = 1

    with pytest.raises(InputError):
        channel.channel_messages(login_owner['token'], invalid_channel_id, 0)


def test_channel_messages_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel_id2 = channels.channels_create(login_owner['token'], "channel", False)

    with pytest.raises(AccessError):
        channel.channel_messages(login_user['token'], channel_id['channel_id'], 0)
        channel.channel_messages(login_owner['token'], channel_id2['channel_id'], 0)


def test_channel_messages_one_message_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner['token'], channel_id['channel_id'], 'example message')
    channel_messages = channel.channel_messages(login_owner['token'], channel_id['channel_id'], 0)

    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1
    assert channel_messages['messages'][0]['message_id'] == 1
    assert channel_messages['messages'][0]['u_id'] == login_owner['u_id']
    assert channel_messages['messages'][0]['message'] == 'example message'

def test_channel_messages_max_messages_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)   

    x = 0
    while x < 50:
        message.message_send(login_owner['token'], channel_id['channel_id'], 'example message')
        x += 1
    
    channel_messages = channel.channel_messages(login_owner['token'], channel_id['channel_id'], 0) 
    channel_messages2 = channel.channel_messages(login_owner['token'], channel_id['channel_id'], 1) 
    
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == 50
    assert channel_messages2['start'] == 1
    assert channel_messages2['end'] == -1


# Tests for channel_leave
def test_channel_leave_invalid_channel_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = -1

    with pytest.raises(InputError):
        channel.channel_leave(login_owner['token'], invalid_channel_id)
    
def test_channel_leave_not_in_channel():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    
    owner_channel = channels.channels_create(login_owner['token'], "channel_1", True)
    user_channel = channels.channels_create(login_user['token'], "channel_2", True)

    with pytest.raises(AccessError):  
        channel.channel_leave(login_owner['token'], user_channel['channel_id'])
        channel.channel_leave(login_user['token'], owner_channel['channel_id'])

def test_channel_leave_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel.channel_leave(login_owner['token'], channel_id['channel_id'])

    channel_list = channels.channels_listall(login_owner['token'])
    assert channel_list == {'channels': []}

# Tests for channel_join
def test_channel_join_invalid_channel_id():    
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    
    channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = -1

    with pytest.raises(InputError):
        channel.channel_join(login_user['token'], invalid_channel_id)

def test_channel_join_private_channel():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    with pytest.raises(AccessError):
        channel.channel_join(login_user['token'], channel_id['channel_id'])

def test_public_channel_join_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel.channel_join(login_user['token'], channel_id['channel_id'])

    channel_details = channel.channel_details(login_user['token'], channel_id['channel_id'])

    assert channel_details['all_members'] == [{'u_id': login_owner['u_id'], 'name_first': "Owner", 'name_last': "Test"}, {'u_id': login_user["u_id"], 'name_first': "User", 'name_last': "Test"}]


# Test for channel_addowner
def test_channel_addowner_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    
    with pytest.raises(InputError):
        channel.channel_addowner(login_owner['token'], channel_id['channel_id'], login_user['u_id'])
    
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    invalid_channel_id = -1
    invalid_u_id = -1

    with pytest.raises(InputError):
        channel.channel_addowner(login_owner['token'], invalid_channel_id, login_user['u_id'])
        channel.channel_addowner(login_owner['token'], channel_id['channel_id'], invalid_u_id)
        channel.channel_addowner(login_owner['token'], invalid_channel_id, invalid_u_id)

def test_channel_addowner_already_owner():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        channel.channel_addowner(login_owner['token'], channel_id['channel_id'], login_owner['u_id'])

def test_channel_addowner_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    with pytest.raises(AccessError):
        channel.channel_addowner(login_user['token'], channel_id['channel_id'], login_user['u_id'])
        channel.channel_addowner("", channel_id['channel_id'], login_user['u_id'])


def test_channel_addowner_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channel.channel_addowner(login_owner['token'], channel_id['channel_id'], login_user['u_id'])
    channel_details = channel.channel_details(login_owner['token'], channel_id['channel_id'])
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_removeowner
def test_channel_removeowner_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    invalid_channel_id = -1
    invalid_u_id = -1

    with pytest.raises(InputError):
        channel.channel_removeowner(login_owner['token'], invalid_channel_id, login_user['u_id'])
        channel.channel_removeowner(login_owner['token'], channel_id['channel_id'], invalid_u_id)
        channel.channel_removeowner(login_owner['token'], invalid_channel_id, invalid_u_id)

def test_channel_removeowner_not_owner():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    with pytest.raises(InputError):
        channel.channel_removeowner(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

def test_channel_removeowner_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    with pytest.raises(AccessError):
        channel.channel_removeowner(login_user['token'], channel_id['channel_id'], login_owner['u_id'])
        channel.channel_removeowner("", channel_id['channel_id'], login_owner['u_id'])

def test_channel_removeowner_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channel.channel_addowner(login_owner['token'], channel_id['channel_id'], login_user['u_id'])
    channel.channel_removeowner(login_user['token'], channel_id['channel_id'], login_owner['u_id'])
    channel_details = channel.channel_details(login_owner['token'], channel_id['channel_id'])
    assert channel_details['owner_members'] == [{'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]
