from time import sleep
from subprocess import Popen, PIPE
import json
import re
import signal
import pytest
import requests
from error import InputError
from error import AccessError
from other import clear


# Use this fixture to get the URL of the server.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

#
# JSON FUNCTIONS USED FOR TESTING
#

# register owner function
def reg_owner(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    return r.json()

# register user function
def reg_user(url):
    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    return r.json()

# join channel function
def join_channel(url, login_user, channel_id):
    join_public_channel = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }
    requests.post(f"{url}/channel/join", json=join_public_channel)

# create public channel function
def create_public_channel(url, login_owner, channel_name):
    channels_create_public = {
        'token': login_owner['token'],
        'name': channel_name,
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create_public)
    return r.json()

# send message function
def send_message(url, login_user, channel_id, message):
    message_send = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id'],
        'message': message
    }
    r = requests.post(f"{url}/message/send", json=message_send)
    return r.json()

# search message function
def search(login_user, query_str):
    r = requests.get(f"{url}/search", params={'token': login_user['token'], 'query_str': query_str})
    return r.json()

#
# TEST FUNCTIONS FOR USERS_ALL
#

def test_http_users_all_invalid_token(url):
    clear()

    r = requests.get(f"{url}/users/all", params={'token': "invalid_token"})
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.get(f"{url}/users/all", params={'token': ""})
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

def test_http_users_all_successful(url):
    clear()

    login_owner = reg_owner(url)

    r = requests.get(f"{url}/users/all", params={'token': login_owner['token']})
    all_users = r.json()
    assert all_users['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}]

    login_user = reg_user(url)

    r = requests.get(f"{url}/users/all", params={'token': login_owner['token']})
    all_users = r.json()
    assert all_users['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}, {'u_id' : login_user['u_id'], 'email' : "user@email.com", 'name_first' : "User", 'name_last' : "Test", 'handle_str' : "usertest"}]

#
# TEST FUNCTIONS FOR ADMIN_USERPERMISSION_CHANGE
#

def test_http_admin_userpermission_change_invalid_id(url):
    clear()

    login_owner = reg_owner(url)
    login_user = reg_user(url)
    invalid_id = -1

    invalid_u_id = {
        'token': login_owner['token'],
        'u_id': invalid_id,
        'permission_id': 1
    }

    invalid_permission_id = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': invalid_id
    }

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_u_id)
    payload = r.json
    assert payload['message'] == "Target does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_permission_id)
    payload = r.json
    assert payload['message'] == "Permission id is not valid"
    assert payload['code'] == 400

def test_http_admin_userpermission_change_invalid_token(url):
    clear()

    login_owner = reg_owner(url)
    login_user = reg_user(url)

    empty_token = {
        'token': "",
        'u_id': login_user['u_id'],
        'permission_id': 1
    }

    invalid_token = {
        'token': login_user['token'],
        'u_id': login_owner['u_id'],
        'permission_id': 2
    }

    r = requests.post(f"{url}/admin/userpermission/change", json=empty_token)
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_token)
    payload = r.json
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

def test_http_admin_userpermission_change_successful(url):
    clear()

    login_owner = reg_owner(url)
    login_user = reg_user(url)

    make_user_owner = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': 1
    }
    requests.post(f"{url}/admin/userpermission/change", json=make_user_owner)

    make_owner_user = {
        'token': login_user['token'],
        'u_id': login_owner['u_id'],
        'permission_id': 2
    }
    requests.post(f"{url}/admin/userpermission/change", json=make_owner_user)

    owner_denied = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': 2
    }
    r = requests.post(f"{url}/admin/userpermission/change", json=owner_denied)
    payload = r.json()
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

#
# TEST FUNCTIONS FOR SEARCH
#

def test_http_search_empty(url):
    """Checks that search returns nothing when given an empty string"""

    clear()
    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    send_message(url, login_owner, channel_id, "message")

    search_results = search(url, login_owner, "")

    assert search_results == {'messages': []}

def test_http_search_own_channel_single_message_complete(url):
    """Tests for success when user creates their own channel, sends a message, and searches for the complete message"""
    
    clear()
    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    message_id = send_message(url, login_owner, channel_id, "message")

    search_results = search(url, login_owner, "message")

    assert search_results['messages'][0]['message_id'] == message_id['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_http_search_own_channel_single_message_incomplete(url):
    """Tests for success when user creates their own channel, sends a message, and searches for part of the message"""
    
    clear()
    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    message_id = send_message(url, login_owner, channel_id, "message")

    search_results = search(url, login_owner, "ess")

    assert search_results['messages'][0]['message_id'] == message_id['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_http_search_other_channel_single_message_complete(url):
    """Tests for success when owner creates a channel, user joins the channel, owner sends a message, and user searches for the complete message"""
    
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    join_channel(url, login_user, channel_id)

    message_id = send_message(url, login_owner, channel_id, "message")

    search_results = search(url, login_user, "message")

    assert search_results['messages'][0]['message_id'] == message_id['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_http_search_other_channel_single_message_incomplete(url):
    """Tests for success when owner creates a channel, user joins the channel, owner sends a message, and user searches for part of the message"""
    
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    join_channel(url, login_user, channel_id)

    message_id = send_message(url, login_owner, channel_id, "message")

    search_results = search(url, login_user, "ess")

    assert search_results['messages'][0]['message_id'] == message_id['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"

def test_http_search_both_channels_two_messages_complete(url):
    """Tests for success when owner creates a channel, user joins the channel, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches for the complete messages"""
    
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id1 = create_public_channel(url, login_owner, "channel 1")
    join_channel(url, login_user, channel_id1)

    channel_id2 = create_public_channel(url, login_owner, "channel 2")

    message_id1 = send_message(url, login_owner, channel_id1, "message")
    message_id2 = send_message(url, login_user, channel_id2, "message")

    search_results = search(url, login_user, "message")

    assert search_results['messages'][0]['message_id'] == message_id1['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"
    assert search_results['messages'][1]['message_id'] == message_id2['message_id']
    assert search_results['messages'][1]['u_id'] == login_user['u_id']
    assert search_results['messages'][1]['message'] == "message"

def test_http_search_both_channels_two_messages_incomplete(url):
    """Tests for success when owner creates a channel, user joins the channel, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches for part of the messages"""
    
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id1 = create_public_channel(url, login_owner, "channel 1")
    join_channel(url, login_user, channel_id1)

    channel_id2 = create_public_channel(url, login_owner, "channel 2")

    message_id1 = send_message(url, login_owner, channel_id1, "message")
    message_id2 = send_message(url, login_user, channel_id2, "message")

    search_results = search(url, login_user, "ess")

    assert search_results['messages'][0]['message_id'] == message_id1['message_id']
    assert search_results['messages'][0]['u_id'] == login_owner['u_id']
    assert search_results['messages'][0]['message'] == "message"
    assert search_results['messages'][1]['message_id'] == message_id2['message_id']
    assert search_results['messages'][1]['u_id'] == login_user['u_id']
    assert search_results['messages'][1]['message'] == "message"

def test_http_search_own_channel_single_message_excluding_other_channel(url):
    """Tests for success when owner creates a channel but user does not join, user creates a channel, owner sends a message in their channel, user sends a message in their channel, and user searches the messages"""
    
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id1 = create_public_channel(url, login_owner, "channel 1")
    channel_id2 = create_public_channel(url, login_user, "channel 2")

    send_message(url, login_owner, channel_id1, "message")
    message_id2 = send_message(url, login_user, channel_id2, "message")

    search_results = search(url, login_user, "message")

    assert search_results['messages'][0]['message_id'] == message_id2['message_id']
    assert search_results['messages'][0]['u_id'] == login_user['u_id']
    assert search_results['messages'][0]['message'] == "message"
