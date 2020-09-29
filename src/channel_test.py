import channel
import auth
import pytest
from error import InputError
from error import AccessError
#test functions for channel_invite
def test_channel_invite_invalid_id():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')

    auth.auth_register("user@email.com", "password123", "User", "Test")
    login_user = auth.auth_login("user@email.com", "password123")

    invalid_channel_id = -1
    invalid_u_id = -1

    with pytest.raises(InputError) as e:
        channel.channel_invite(login_owner['token'], invalid_channel_id, login_user['u_id'])
        channel.channel_invite(login_owner['token'], channel_id, invalid_u_id)
        channel.channel_invite(login_owner['token'], invalid_channel_id, invalid_u_id)

def test_channel_invite_invalid_token():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')

    auth.auth_register("user@email.com", "password123", "User", "Test")
    login_user = auth.auth_login("user@email.com", "password123")

    with pytest.raises(AccessError) as e:
        channel.channel_invite("", channel_id, login_user['u_id'])
        channel.channel_invite(login_user['token'], channel_id, login_user['u_id'])

def test_channel_invite_success():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')

    auth.auth_register("user@email.com", "password123", "User", "Test")
    login_user = auth.auth_login("user@email.com", "password123")
    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channel_details = channel.channel_details(login_owner['token'], channel_id)
    assert channel_details['all_members'] == [{u_id : login_owner['u_id'], name_first : Owner, name_last : Test}, {u_id : login_user['u_id'], name_first : User, name_last : Test}]

#tests for channel_details
def test_channel_details_invalid_id():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')
    invalid_channel_id = -1

    with pytest.raises(InputError) as e:
        channel.channel_details(login_owner['token'], invalid_channel_id)

def Test_channel_details_invalid_token():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')

    auth.auth_register("user@email.com", "password123", "User", "Test")
    login_user = auth.auth_login("user@email.com", "password123")

    with pytest.raises(AccessError) as e:
        channel.channel_details(login_user['token'], channel_id)

def test_channel_details_success():
    auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_owner = auth.auth_login("owner@email.com", "password123")
    channel_id = channels.channels_create(login_owner['token'], "channel", 'u_id')

    channel_details = channel.channel_details(login_owner['token'], channel_id)
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{u_id : login_owner['u_id'], name_first : Owner, name_last : Test}]
    assert channel_details['all_members'] == [{u_id : login_owner['u_id'], name_first : Owner, name_last : Test}]

    auth.auth_register("user@email.com", "password123", "User", "Test")
    login_user = auth.auth_login("user@email.com", "password123")
    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channel_details = channel.channel_details(login_user['token'], channel_id)
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{u_id : login_owner['u_id'], name_first : Owner, name_last : Test}]
    assert channel_details['all_members'] == [{u_id : login_owner['u_id'], name_first : Owner, name_last : Test}, {u_id : login_user['u_id'], name_first : User, name_last : Test}]