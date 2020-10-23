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
    server = Popen(["python3", "simple.py"], stderr=PIPE, stdout=PIPE)
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

# Register owner function
def reg_owner(url):
    """Registers an owner, the original owner of the Flock."""
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    return r.json()

# Register user function
def reg_user(url):
    """Registers a user."""
    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    return r.json()

#create channel function
def create_channel(url, login_owner):
    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    return r.json()

#invite user function
def inv_user(url, login_owner, login_user, channel_id):
    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

#message send function
def msg_send(user, channel, message):
    message_send = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': message
    }
    requests.post(f"{url}/message/remove", json=message_send)

#create unique channel function
def create_unique_channel(user, name, is_public):
    channel = {
        'token': user['token'],
        'name': name,
        'is_public': is_public
    }
    r = requests.post(f"{url}/channels/create", json=channel)
    return r.json()

#tests for http_channel_invite
def test_http_channel_invite_invalid_id(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    invalid_id = -1

    invalid_u_id = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': invalid_id
    }

    invalid_channel_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': login_user['u_id']
    }

    r = requests.post(f"{url}/channel/invite", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "Invitee does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/invite", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "Invalid channel id"
    assert payload['code'] == 400

def test_http_channel_invite_invalid_token(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    empty_token = {
        'token': "",
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    invalid_token = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    r = requests.post(f"{url}/channel/invite", json=empty_token)
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/invite", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "Inviter is not part of this channel"
    assert payload['code'] == 400

def test_http_channel_invite_success(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    success_invite = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=success_invite)

    get_details = {
        login_owner['token'],
        channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json

    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

    r = requests.post(f"{url}/channel/invite", json=success_invite)
    payload = r.json()
    assert payload['message'] == "Invitee is already invited to this channel"
    assert payload['code'] == 400

#tests for http_channel_details
def test_http_channel_details_invalid_id(url):
    clear()
    login_owner = reg_owner(url)

    create_channel(url, login_owner)

    invalid_channel_id = -1

    invalid_id = {
        'token': login_owner,
        'channel_id': invalid_channel_id
    }
    r = requests.get(f"{url}/channel/details", json=invalid_id)
    payload = r.json()
    assert payload['message'] == "Invalid channel id"
    assert payload['code'] == 400

def test_http_channel_details_invalid_token(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    empty_token = {
        'token': "",
        'channel_id': channel_id['channel_id']
    }

    invalid_token = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }

    r = requests.get(f"{url}/channel/details", json=empty_token)
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.get(f"{url}/channel/details", json=invalid_token)
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

def test_http_channel_details_success(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    get_details = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json()
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    get_details = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json()
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

#tests http_channel_addowner
def test_http_channel_addowner_invalid_id(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    make_user_owner_fail = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    r = requests.post(f"{url}/channel/addowner", json=make_user_owner_fail)
    payload = r.json()
    assert payload['message'] == "Target is not part of the channel"
    assert payload['code'] == 400

    inv_user(url, login_owner, login_user, channel_id)

    invalid_id = -1

    invalid_channel_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': login_user['u_id']
    }

    invalid_u_id = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': invalid_id
    }

    r = requests.post(f"{url}/channel/addowner", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "Invalid channel id"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/addowner", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "Target is not part of the channel"
    assert payload['code'] == 400

def test_http_channel_addowner_already_owner(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    make_owner_owner = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_owner['u_id']
    }

    r = requests.post(f"{url}/channel/addowner", json=make_owner_owner)
    payload = r.json()
    assert payload['message'] == "Target is already an owner of this channel"
    assert payload['code'] == 400

def test_http_channel_addowner_invalid_token(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    empty_token = {
        'token': "",
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    invalid_token = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    r = requests.post(f"{url}/channel/addowner", json=empty_token)
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/addowner", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

def test_http_channel_addowner_success(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    make_user_owner = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/addowner", json=make_user_owner)

    get_details = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json()
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

#tests http_channel_removeowner
def test_http_channel_removeowner_invalid_id(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    make_user_owner = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/addowner", json=make_user_owner)

    invalid_id = -1

    invalid_channel_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': login_user['u_id']
    }

    invalid_u_id = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': invalid_id
    }

    r = requests.post(f"{url}/channel/removeowner", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "Invalid channel id"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/removeowner", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "Target is not an owner of this channel"
    assert payload['code'] == 400

def test_http_channel_removeowner_not_owner(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    remove_owner_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    r = requests.post(f"{url}/channel/removeowner", json=remove_owner_user)
    payload = r.json()
    assert payload['message'] == "Target is not an owner of this channel"
    assert payload['code'] == 400

def test_http_channel_removeowner_invalid_token(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    empty_token = {
        'token': "",
        'channel_id': channel_id['channel_id'],
        'u_id': login_owner['u_id']
    }

    invalid_token = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_owner['u_id']
    }

    r = requests.post(f"{url}/channel/removeowner", json=empty_token)
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/channel/removeowner", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

def test_http_channel_removeowner_success(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    remove_owner = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_owner['u_id']
    }
    requests.post(f"{url}/channel/removeowner", json=remove_owner)

    get_details = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json()
    assert channel_details['owner_members'] == [{'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

# Tests for channel_messages   
def test_http_channel_messages_invalid_start_index(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(login_owner, "channel", True)
    channel_id2 = create_unique_channel(login_owner, "channel2", True)

    msg_send(login_owner, channel_id, "example message")

    invalid_start1 = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"],
        "start": 0
    }

    r = requests.get(f"{url}/channel/messages", json=invalid_start1)
    payload = r.json()
    assert payload["message"] == "Start is greater than the total number of messages in the channel"
    assert payload["code"] == 400

    invalid_start2 = {
        "token": login_owner["token"],
        "channel_id": channel_id2["channel_id"],
        "start": 1
    }

    r = requests.get(f"{url}/channel/messages", json=invalid_start2)
    payload = r.json()
    assert payload["message"] == "Start is greater than the total number of messages in the channel"
    assert payload["code"] == 400
    
def test_http_channel_messages_invalid_channel(url):
    clear()
    login_owner = reg_owner(url)
    create_unique_channel(login_owner, "channel", True)

    invalid_channel = {
        "token": login_owner["token"],
        "channel_id": -1,
        "start": 0
    }

    r = requests.get(f"{url}/channel/messages", json=invalid_channel)
    payload = r.json()
    assert payload["message"] == "Channel ID is not a valid channel"
    assert payload["code"] == 400
    
def test_http_channel_messages_invalid_token(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(login_owner, "channel", True)
    channel_id2 = create_unique_channel(login_owner, "channel2", True)
    login_user = reg_user(url)

    invalid_token = {
        "token": login_user["token"],
        "channel_id": channel_id["channel_id"],
        "start": 0
    }

    r = requests.get(f"{url}/channel/messages", json=invalid_token)
    payload = r.json()
    assert payload["message"] == "Channel ID is not a valid channel"
    assert payload["code"] == 400

    invalid_token2 = {
        "token": login_user["token"],
        "channel_id": channel_id2["channel_id"],
        "start": 0
    }
    
    r = requests.get(f"{url}/channel/messages", json=invalid_token2)
    payload = r.json()
    assert payload["message"] == "Channel ID is not a valid channel"
    assert payload["code"] == 400

def test_http_channel_messages_one_message_success(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(login_owner, "channel", True)

    msg_send(login_owner, channel_id, "example message")

    messages = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"],
        "start": 0
    }

    r = requests.get(f"{url}/channel/messages", json=messages)
    message = r.json
    assert message['start'] == 0
    assert message['end'] == -1
    assert message['messages'][0]['message_id'] == 1
    assert message['messages'][0]['u_id'] == login_owner['u_id']
    assert message['messages'][0][0]['message'] == 'example message'

def test_http_channel_messages_max_messages_success():
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(login_owner, "channel", True)

    for x in range(50):
        msg_send(login_owner, channel_id, "example message")

    messages = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"],
        "start": 0
    }

    r = requests.get(f"{url}/channel/messages", json=messages)
    message = r.json
    assert message['start'] == 0
    assert message['end'] == 50
    
    messages = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"],
        "start": 1
    }

    r = requests.get(f"{url}/channel/messages", json=messages)
    message = r.json
    assert message['start'] == 1
    assert message['end'] == -1

#tests for channel_leave
def test_http_channel_leave_invalid_channel_id():
    clear()
    login_owner = reg_owner(url)
    create_unique_channel(login_owner, "channel", True)

    