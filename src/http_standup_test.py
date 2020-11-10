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

#Standup start function
def start_standup(url, token, channel_id, length):
    standup = {
        'token': token,
        'channel_id': channel_id,
        'length': length
    }
    r = requests.post(url + "standup/start", json=standup)
    return r.json()


def search_standup(url, token, channel_id):
    r = requests.get(url + "standup/active", params={'token': token, 'channel_id': channel_id})
    return r.json()

def send_standup(url, token, channel_id, message):
    send_info = {
        'token': token,
        'channel_id': channel_id,
        'message': message
    }
    r = requests.post(url + "standup/send", json=send_info)
    return r.json()

#Tests for http_standup_start
def test_http_standup_start_invalid_id(url):
    clear()

    login_owner = reg_owner(url)

    invalid_id = -1

    payload = start_standup(url, login_owner['token'], invalid_id, 10)
    assert payload['message'] == "<p>Invalid channel id</p>"
    assert payload['code'] == 400

def test_http_standup_start_invalid_length(url):
    clear()

    login_owner = reg_owner(url)
    channel_id = create_channel(url, login_owner)

    payload = start_standup(url, login_owner['token'], channel_id['channel_id'], 0)
    assert payload['message'] == "<p>Invalid length of time</p>"
    assert payload['code'] == 400

    payload = start_standup(url, login_owner['token'], channel_id['channel_id'], -1)
    assert payload['message'] == "<p>Invalid length of time</p>"
    assert payload['code'] == 400

    payload = start_standup(url, login_owner['token'], channel_id['channel_id'], -10)
    assert payload['message'] == "<p>Invalid length of time</p>"
    assert payload['code'] == 400

def test_http_standup_start_invalid_token(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    payload = start_standup(url, "", channel_id['channel_id'], 10)
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    payload = start_standup(url, login_user['token'], channel_id['channel_id'], 10)
    assert payload['message'] == "<p>User is not authorised</p>"
    assert payload['code'] == 400

def test_http_standup_start_success(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    start_standup(url, login_owner['token'], channel_id['channel_id'], 10)

    standup_info = search_standup(url, login_owner['token'], channel_id['channel_id'])
    assert standup_info['is_active'] == True

#Test functions for http_standup_active
def test_standup_active_invalid_id(url):
    clear()

    login_owner = reg_owner(url)

    invalid_id = -1

    standup_info = search_standup(url, login_owner['token'], invalid_id)
    assert standup_info['message'] == "<p>Invalid channel id</p>"
    assert standup_info['code'] == 400

def test_http_standup_active_invalid_token(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    standup_info = search_standup(url, "", channel_id['channel_id'])
    assert standup_info['message'] == "<p>Token does not exist</p>"
    assert standup_info['code'] == 400

    standup_info = search_standup(url, login_user['token'], channel_id['channel_id'])
    assert standup_info['message'] == "<p>User is not authorised</p>"
    assert standup_info['code'] == 400

def test_http_standup_active_successful(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    standup_info = search_standup(url, login_owner['token'], channel_id['channel_id'])
    assert standup_info['is_active'] == False
    assert standup_info['time_finish'] == None

    start_standup(url, login_owner['token'], channel_id['channel_id'], 10)
    standup_info = search_standup(url, login_owner['token'], channel_id['channel_id'])
    assert standup_info['is_active'] == True

#Test functions for http_standup_send
def test_http_standup_send_invalid_id(url):
    clear()

    login_owner = reg_owner(url)

    invalid_id = -1

    payload = send_standup(url, login_owner['token'], invalid_id, "sample message")
    assert payload['message'] == "<p>Invalid channel id</p>"
    assert payload['code'] == 400

def test_http_standup_send_invalid_message(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    start_standup(url, login_owner['token'], channel_id['channel_id'], 10)

    payload = send_standup(url, login_owner['token'], channel_id['channel_id'], "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce")
    assert payload['message'] == "<p>Message is larger than 1000 characters</p>"
    assert payload['code'] == 400

def test_http_standup_send_no_active_standup(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    payload = send_standup(url, login_owner['token'], channel_id['channel_id'], "sample message")
    assert payload['message'] == "<p>There is no active stand up</p>"
    assert payload['code'] == 400

def test_http_standup_send_invalid_token(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_channel(url, login_owner)

    login_user = reg_user(url)

    start_standup(url, login_owner['token'], channel_id['channel_id'], 10)

    payload = send_standup(url, "", channel_id['channel_id'], "sample message")
    assert payload['message'] == "<p>Token does not exist</p>"
    assert payload['code'] == 400

    payload = send_standup(url, login_user['token'], channel_id['channel_id'], "sample message")
    assert payload['message'] == "<p>User is not authorised</p>"
    assert payload['code'] == 400
