import auth
import other
import message
import channel
import channels
import pytest
import data
from error import InputError
from error import AccessError

# test functions for users_all
def test_users_all_invalid_token():
    """tests for invalid token"""
    other.clear()
    with pytest.raises(AccessError):
        other.users_all("invalid_token")
        other.users_all("")

def test_users_all_successful():
    """tests for user_all sucess"""
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    r = other.users_all(login_owner['token'])
    assert r['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}]

    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")
    r = other.users_all(login_user['token'])
    assert r['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}, {'u_id' : login_user['u_id'], 'email' : "user@email.com", 'name_first' : "User", 'name_last' : "Test", 'handle_str' : "usertest"}]

# test functions for admin_userpermission_change
def test_admin_userpermission_change_invalid_id():
    """tests for invalid ids"""
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")
    invalid_u_id = -1
    invalid_permission_id = -1

    with pytest.raises(InputError):
        other.admin_userpermission_change(login_owner['token'], invalid_u_id, 1)
        other.admin_userpermission_change(login_owner['token'], login_user['u_id'], invalid_permission_id)
        other.admin_userpermission_change(login_owner['token'], invalid_u_id, invalid_permission_id)

def test_admin_userpermission_change_invalid_token():
    """tests for invalid token"""
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    with pytest.raises(AccessError):
        other.admin_userpermission_change("", login_user['u_id'], 1)
        other.admin_userpermission_change(login_user['token'], login_owner['u_id'], 2)

def test_admin_userpermission_change_success():
    """tests for change permission sucess"""
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    other.admin_userpermission_change(login_owner['token'], login_user['u_id'], 1)
    other.admin_userpermission_change(login_user['token'], login_owner['u_id'], 2)

    with pytest.raises(AccessError):
        other.admin_userpermission_change(login_owner['token'], login_user['u_id'], 2)

# test functions for search
def test_search_empty():
    """Checks that search returns nothing when given an empty string"""

    other.clear()
    login = auth.auth_register("user@email.com", "password123", "User", "Test")

    channel_id = channels.channels_create(login['token'], "channel", True)
    message.message_send(login['token'], channel_id, "message")

    assert other.search(login['token'], "") == {'messages': []}

def test_search_own_channel_single_message_complete():
    """Tests for success when user creates their own channel, sends a message, and searches for the complete message"""
    
    other.clear()
    login = auth.auth_register("user@email.com", "password123", "User", "Test")

    channel_id = channels.channels_create(login['token'], "channel", True)
    message_id = message.message_send(login['token'], channel_id, "message")

    search_results = other.search(login['token'], "message")

    assert search_results['messages'][0]['message_id'] == message_id
    assert search_results['messages'][0]['u_id'] == login['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_search_own_channel_single_message_incomplete():
    """Tests for success when user creates their own channel, sends a message, and searches for part of the message"""
    
    other.clear()
    login = auth.auth_register("user@email.com", "password123", "User", "Test")

    channel_id = channels.channels_create(login['token'], "channel", True)
    message_id = message.message_send(login['token'], channel_id, "message")

    search_results = other.search(login['token'], "ess")

    assert search_results['messages'][0]['message_id'] == message_id
    assert search_results['messages'][0]['u_id'] == login['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_search_other_channel_single_message_complete():
    """Tests for success when owner creates a channel, user joins the channel, owner sends a message, and user searches for the complete message"""
    
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel.channel_join(login_user['token'], channel_id['channel_id'])

    message_id = message.message_send(login_owner['token'], channel_id, "message")

    search_results = other.search(login_user['token'], "message")

    assert search_results['messages'][0]['message_id'] == message_id
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_search_other_channel_single_message_incomplete():
    """Tests for success when owner creates a channel, user joins the channel, owner sends a message, and user searches for part of the message"""
    
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channel.channel_join(login_user['token'], channel_id['channel_id'])

    message_id = message.message_send(login_owner['token'], channel_id, "message")

    search_results = other.search(login_user['token'], "ess")

    assert search_results['messages'][0]['message_id'] == message_id
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_search_both_channels_two_messages_complete():
    """Tests for success when owner creates a channel, user joins the channel, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches for the complete messages"""
    
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    channel_id1 = channels.channels_create(login_owner['token'], "channel1", True)
    channel.channel_join(login_user['token'], channel_id1['channel_id'])

    channel_id2 = channels.channels_create(login_user['token'], "channel2", True)

    message_id1 = message.message_send(login_owner['token'], channel_id1, "message")
    message_id2 = message.message_send(login_user['token'], channel_id2, "message")

    search_results = other.search(login_user['token'], "message")

    assert search_results['messages'][0]['message_id'] == message_id1
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"
    assert search_results['messages'][1]['message_id'] == message_id2
    assert search_results['messages'][1]['u_id'] == login_user['u_id']
    assert search_results['messages'][1]['message'] == "message"

def test_search_both_channels_two_messages_incomplete():
    """Tests for success when owner creates a channel, user joins the channel, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches for part of the messages"""
    
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    channel_id1 = channels.channels_create(login_owner['token'], "channel1", True)
    channel.channel_join(login_user['token'], channel_id1['channel_id'])

    channel_id2 = channels.channels_create(login_user['token'], "channel2", True)

    message_id1 = message.message_send(login_owner['token'], channel_id1, "message")
    message_id2 = message.message_send(login_user['token'], channel_id2, "messages")

    search_results = other.search(login_user['token'], "ess")

    assert search_results['messages'][0]['message_id'] == message_id1
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"
    assert search_results['messages'][1]['message_id'] == message_id2
    assert search_results['messages'][1]['u_id'] == login_user['u_id']
    assert search_results['messages'][1]['message'] == "message"

def test_search_own_channel_single_message_excluding_other_channel():
    """Tests for success when owner creates a channel but user does not join, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches the messages"""
    
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    channel_id1 = channels.channels_create(login_owner['token'], "channel1", True)
    channel_id2 = channels.channels_create(login_user['token'], "channel2", True)

    message.message_send(login_owner['token'], channel_id1, "message")
    message_id2 = message.message_send(login_user['token'], channel_id2, "message")

    search_results = other.search(login_user['token'], "message")

    assert search_results['messages'][0]['message_id'] == message_id2
    assert search_results['messages'][0]['u_id'] == login_user['u_id']
    assert search_results['messages'][0]['message'] == "message"
