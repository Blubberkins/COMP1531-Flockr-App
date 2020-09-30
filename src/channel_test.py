import channel
import channels
import auth
import message
import pytest
from error import InputError
from error import AccessError
# Test functions for channel_invite
def test_channel_invite_invalid_id():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True) # Create channels last param should be a boolean

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    invalid_channel_id = -1
    invalid_u_id = -1

    with pytest.raises(InputError) as e:
        channel.channel_invite(login_owner['token'], invalid_channel_id, login_user['u_id'])
        channel.channel_invite(login_owner['token'], channel_id, invalid_u_id)
        channel.channel_invite(login_owner['token'], invalid_channel_id, invalid_u_id)

def test_channel_invite_invalid_token():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError) as e:
        channel.channel_invite("", channel_id, login_user['u_id'])
        channel.channel_invite(login_user['token'], channel_id, login_user['u_id'])

def test_channel_invite_success():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channel_details = channel.channel_details(login_owner['token'], channel_id)
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_details
def test_channel_details_invalid_id():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = -1

    with pytest.raises(InputError) as e:
        channel.channel_details(login_owner['token'], invalid_channel_id)

def Test_channel_details_invalid_token():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError) as e:
        channel.channel_details(login_user['token'], channel_id)

def test_channel_details_success():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    channel_details = channel.channel_details(login_owner['token'], channel_id)
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channel_details = channel.channel_details(login_user['token'], channel_id)
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_messages

def test_channel_messages_invalid_start_index():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel_id2 = channels.channels_create(login_owner['token'], "channel", True)
    
    message.message_send(login_owner['token'], channel_id2, 'example message')

    with pytest.raises(InputError) as e:
        channel.channel_messages(login_owner['token'], channel_id, 0)
        channel.channel_messages(login_owner['token'], channel_id2, 1)
    pass

def test_channel_messages_invalid_channel():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    invalid_channel_id = channel_id - 1

    with pytest.raises(InputError) as e:
        channel.channel_messages(login_owner['token'], invalid_channel_id, 0)
    pass

def test_channel_messages_invalid_token():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel_id2 = channels.channels_create(login_owner['token'], "channel", False)

    with pytest.raises(AccessError) as e:
        channel.channel_messages(login_user['token'], channel_id, 0)
        channel.channel_messages(login_owner['token'], channel_id2, 0)
    pass

def test_channel_messages_one_message_succes():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner['token'], channel_id, 'example message')
    channel_messages = channel.channel_messages(login_owner['token'], channel_id, 0)

    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1
    assert channel_messages['messages'] == [{'message_id': 1, 'u_id': login_owner['u_id'],'message': 'example message', 'time_created': 0}]

def test_channel_messages_multiple_messages_success():
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner['token'], channel_id, 'example message')
    message.message_send(login_owner['token'], channel_id, 'example message')
    message.message_send(login_owner['token'], channel_id, 'example message')
    channel_messages = channel.channel_messages(login_owner['token'], channel_id, 0) 
       
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1
    assert channel_messages['messages'] == [{'message_id': 1, 'u_id': login_owner['u_id'],'message': 'example message', 'time_created': 0}, {'message_id': 2, 'u_id': login_owner['u_id'],'message': 'example message', 'time_created': 0}
    , {'message_id': 3, 'u_id': login_owner['u_id'],'message': 'example message', 'time_created': 0}]
