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
    """Tests that the server has been set up properly."""
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
    r = requests.post(url + "auth/register", json=register_owner)
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
    r = requests.post(url + "auth/register", json=register_user)
    return r.json()

#create channel function
def create_channel(url, login_owner):
    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(url + "channels/create", json=channels_create)
    return r.json()

#invite user function
def inv_user(url, login_owner, login_user, channel_id):
    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(url + "channel/invite", json=invite_user)

#message send function
def msg_send(url, user, channel, message):
    message_send = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'message': message
    }
    requests.post(url + "message/remove", json=message_send)

#create unique channel function
def create_unique_channel(url, user, name, is_public):
    channel = {
        'token': user['token'],
        'name': name,
        'is_public': is_public
    }
    r = requests.post(url + "channels/create", json=channel)
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

    r = requests.post(url + "channel/invite", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "<p>Invitee does not exist</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/invite", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "<p>Invalid channel id</p>"
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

    r = requests.post(url + "channel/invite", json=empty_token)
    payload = r.json()
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/invite", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "<p>Inviter is not part of this channel</p>"
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
    requests.post(url + "channel/invite", json=success_invite)

    r = requests.get(url + "channel/details", params={'token': login_owner['token'], 'channel_id': channel_id['channel_id']})
    channel_details = r.json()
    assert channel_details["all_members"] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}, {'u_id' : login_user['u_id'], 'name_first' : 'User', 'name_last' : 'Test'}]

    r = requests.post(url + "channel/invite", json=success_invite)
    payload = r.json()
    assert payload['message'] == "<p>Invitee is already invited to this channel</p>"
    assert payload['code'] == 400

#tests for http_channel_details
def test_http_channel_details_invalid_id(url):
    clear()
    login_owner = reg_owner(url)

    create_channel(url, login_owner)

    invalid_channel_id = -1

    r = requests.get(url + "channel/details", params={'token': login_owner['token'], 'channel_id': invalid_channel_id})
    payload = r.json()
    assert payload['message'] == "<p>Invalid channel id</p>"
    assert payload['code'] == 400

def test_http_channel_details_invalid_token(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    r = requests.get(url + "channel/details", params={'token': "", 'channel_id': channel_id['channel_id']})
    payload = r.json()
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    r = requests.get(url + "channel/details", params={'token': login_user['token'], 'channel_id': channel_id['channel_id']})
    payload = r.json()
    assert payload['message'] == "<p>User is not authorised</p>"
    assert payload['code'] == 400

def test_http_channel_details_success(url):
    clear()
    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    r = requests.get(url + "channel/details", params={'token': login_owner['token'], 'channel_id': channel_id['channel_id']})
    channel_details = r.json()
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]

    login_user = reg_user(url)

    inv_user(url, login_owner, login_user, channel_id)

    r = requests.get(url + "channel/details", params={'token': login_owner['token'], 'channel_id': channel_id['channel_id']})
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
    r = requests.post(url + "channel/addowner", json=make_user_owner_fail)
    payload = r.json()
    assert payload['message'] == "<p>Target is not part of the channel</p>"
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

    r = requests.post(url + "channel/addowner", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "<p>Invalid channel id</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/addowner", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "<p>Target is not part of the channel</p>"
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

    r = requests.post(url + "channel/addowner", json=make_owner_owner)
    payload = r.json()
    assert payload['message'] == "<p>Target is already an owner of this channel</p>"
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

    r = requests.post(url + "channel/addowner", json=empty_token)
    payload = r.json()
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/addowner", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "<p>User is not authorised</p>"
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
    requests.post(url + "channel/addowner", json=make_user_owner)

    r = requests.get(url + "channel/details", params={'token': login_owner['token'], 'channel_id': channel_id['channel_id']})
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
    requests.post(url + "channel/addowner", json=make_user_owner)

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

    r = requests.post(url + "channel/removeowner", json=invalid_channel_id)
    payload = r.json()
    assert payload['message'] == "<p>Invalid channel id</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/removeowner", json=invalid_u_id)
    payload = r.json()
    assert payload['message'] == "<p>Target is not an owner of this channel</p>"
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

    r = requests.post(url + "channel/removeowner", json=remove_owner_user)
    payload = r.json()
    assert payload['message'] == "<p>Target is not an owner of this channel</p>"
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

    r = requests.post(url + "channel/removeowner", json=empty_token)
    payload = r.json()
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    r = requests.post(url + "channel/removeowner", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "<p>User is not authorised</p>"
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
    requests.post(url + "channel/removeowner", json=remove_owner)

    r = requests.get(url + "channel/details", params={'token': login_user['token'], 'channel_id': channel_id['channel_id']})
    channel_details = r.json()
    assert channel_details['owner_members'] == [{'u_id': login_user['u_id'], 'name_first': 'User', 'name_last': 'Test'}]

# Tests for channel_messages   
def test_http_channel_messages_invalid_start_index(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(url, login_owner, "channel", True)
    channel_id2 = create_unique_channel(url, login_owner, "channel2", True)

    msg_send(url, login_owner, channel_id, "example message") 

    r = requests.get(url + "channel/messages", params={"token": login_owner["token"], "channel_id": channel_id["channel_id"], "start": 0})
    payload = r.json()
    assert payload["message"] == "<p>Start is greater than the total number of messages in the channel</p>"
    assert payload["code"] == 400

    r = requests.get(url + "channel/messages", params={"token": login_owner["token"], "channel_id": channel_id2["channel_id"], "start": 1})
    payload = r.json()
    assert payload["message"] == "<p>Start is greater than the total number of messages in the channel</p>"
    assert payload["code"] == 400
    
def test_http_channel_messages_invalid_channel(url):
    clear()
    login_owner = reg_owner(url)
    create_unique_channel(url, login_owner, "channel", True)

    r = requests.get(url + "channel/messages", params={"token": login_owner["token"], "channel_id": -1, "start": 0})
    payload = r.json()
    assert payload["message"] == "<p>Channel ID is not a valid channel</p>"
    assert payload["code"] == 400
    
def test_http_channel_messages_invalid_token(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(url, login_owner, "channel", True)
    channel_id2 = create_unique_channel(url, login_owner, "channel2", True)
    login_user = reg_user(url)

    r = requests.get(url + "channel/messages", params={"token": login_user["token"], "channel_id": channel_id["channel_id"], "start": 0})
    payload = r.json()
    assert payload["message"] == "<p>Channel ID is not a valid channel</p>"
    assert payload["code"] == 400
    
    r = requests.get(url + "channel/messages", params={"token": login_user["token"],"channel_id": channel_id2["channel_id"],"start": 0})
    payload = r.json()
    assert payload["message"] == "<p>Channel ID is not a valid channel</p>"
    assert payload["code"] == 400

def test_http_channel_messages_one_message_success(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(url, login_owner, "channel", True)

    msg_send(url, login_owner, channel_id, "example message")

    r = requests.get(url + "channel/messages", params={"token": login_owner["token"], "channel_id": channel_id["channel_id"], "start": 0})
    message = r.json()
    assert message['start'] == 0
    assert message['end'] == -1
    assert message['messages'][0]['message_id'] == 1
    assert message['messages'][0]['u_id'] == login_owner['u_id']
    assert message['messages'][0][0]['message'] == 'example message'

def test_http_channel_messages_max_messages_success(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(url, login_owner, "channel", True)

    x = 0
    while x < 50:
        msg_send(url, login_owner, channel_id, "example message")
        x += 1

    messages = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"],
        "start": 0
    }

    r = requests.get(url + "channel/messages", json=messages)
    message = r.json()
    assert message['start'] == 0
    assert message['end'] == 50

    r = requests.get(url + "channel/messages", params={"token": login_owner["token"],"channel_id": channel_id["channel_id"],"start": 1})
    message = r.json()
    assert message['start'] == 1
    assert message['end'] == -1

#tests for channel_leave
def test_http_channel_leave_invalid_channel_id(url):
    clear()
    login_owner = reg_owner(url)
    create_unique_channel(url, login_owner, "channel", True)
    
    invalid_channel = {
        "token": login_owner["token"],
        "channel_id": -1,
    }

    r = requests.post(url + 'channel/leave', json=invalid_channel)
    payload = r.json()
    assert payload["message"] == "<p>Channel ID is not a valid channel</p>"
    assert payload["code"] == 400

def test_http_channel_leave_not_in_channel(url):
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    owner_channel = create_unique_channel(url, login_owner, "channel_1", True)
    user_channel = create_unique_channel(url, login_user, "channel_2", True)

    invalid_user_1 = {
        "token": login_owner["token"],
        "channel_id": user_channel["channel_id"]
    }

    r = requests.post(url + 'channel/leave', json=invalid_user_1)
    payload = r.json()
    assert payload["message"] == "<p>Authorised user is not a member of channel with channel_id</p>"
    assert payload["code"] == 400

    invalid_user_2 = {
        "token": login_user["token"],
        "channel_id": owner_channel["channel_id"]
    }

    r = requests.post(url + 'channel/leave', json=invalid_user_2)
    payload = r.json()
    assert payload["message"] == "<p>Authorised user is not a member of channel with channel_id</p>"
    assert payload["code"] == 400

def test_http_channel_leave_success(url):
    clear()
    login_owner = reg_owner(url)
    channel_id = create_unique_channel(url, login_owner, "channel", True)

    user = {
        "token": login_owner["token"],
        "channel_id": channel_id["channel_id"]
    }
    
    requests.post(url + 'channel/leave', json=user)

    r = requests.get(url + 'channels/listall', params={"token": login_owner["token"]})
    payload = r.json()
    assert payload["channels"] == []

#tests for channel_join
def test_http_channel_join_invalid_channel_id(url):
    clear()
    login_owner = reg_owner(url)
    reg_user(url)

    create_unique_channel(url, login_owner, "channel", True)

    invalid_channel = {
        "token": login_owner["token"],
        "channel_id": -1
    }

    r = requests.post(url + 'channel/join', json=invalid_channel)
    payload = r.json()

    assert payload["message"] == "<p>Channel ID is not a valid channel</p>"
    assert payload["code"] == 400

def test_http_channel_join_private_channel(url):
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id = create_unique_channel(url, login_owner, "channel", False)

    user = {
        "token": login_user["token"],
        "channel_id": channel_id["channel_id"]
    }

    r = requests.post(url + 'channel/join', json=user)
    payload = r.json()

    assert payload["message"] == "<p>Channel is private</p>"
    assert payload["code"] == 400

def test_http_public_channel_join_success(url):
    clear()
    login_owner = reg_owner(url)
    login_user = reg_user(url)

    channel_id = create_unique_channel(url, login_owner, "channel", True)
    
    user = {
        "token": login_user["token"],
        "channel_id": channel_id["channel_id"]
    }
    requests.post(url + 'channel/join', json=user)

    r = requests.get(url + 'channel/details', params={"token": login_user["token"],"channel_id": channel_id["channel_id"]})
    payload = r.json()
    
    assert payload["channel_details"]["all_members"] == [{'u_id': login_owner['u_id'], 'name_first': "Owner", 'name_last': "Test"}, {'u_id': login_user["u_id"], 'name_first': "User", 'name_last': "Test"}]
