from time import sleep
from subprocess import Popen, PIPE
import json
import re
import signal
import pytest
import requests
from error import InputError
from error import AccessError


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

#tests for http_channel_invite
def test_http_channel_invite_invalid_id(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

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

    invalid_both_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': invalid_id
    }

    with pytest.raises(InputError):
        requests.post(f"{url}/channel/invite", json=invalid_u_id)
        requests.post(f"{url}/channel/invite", json=invalid_channel_id)
        requests.post(f"{url}/channel/invite", json=invalid_both_id)

def test_http_channel_invite_invalid_token(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

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

    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/invite", json=empty_token)
        requests.post(f"{url}/channel/invite", json=invalid_token)

def test_http_channel_invite_success(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

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

#tests for http_channel_details
def test_http_channel_details_invalid_id(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    invalid_channel_id = -1

    invalid_id = {
        'token': login_owner,
        'channel_id': invalid_channel_id
    }
    with pytest.raises(InputError):
        requests.get(f"{url}/channel/details", json=invalid_id)

def test_http_channel_details_invalid_token(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    empty_token = {
        'token': "",
        'channel_id': channel_id['channel_id']
    }

    invalid_token = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }

    with pytest.raises(AccessError):
        requests.get(f"{url}/channel/details", json=empty_token)
        requests.get(f"{url}/channel/details", json=invalid_token)

def test_http_channel_details_success(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    get_details = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=get_details)
    channel_details = r.json()
    assert channel_details['name'] == "channel"
    assert channel_details['owner_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]
    assert channel_details['all_members'] == [{'u_id' : login_owner['u_id'], 'name_first' : 'Owner', 'name_last' : 'Test'}]

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    make_user_owner_fail = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    with pytest.raises(InputError):
        requests.post(f"{url}/channel/addowner", json=make_user_owner_fail)
   
    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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

    invalid_both_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': invalid_id
    }

    with pytest.raises(InputError):
        requests.post(f"{url}/channel/addowner", json=invalid_channel_id)
        requests.post(f"{url}/channel/addowner", json=invalid_u_id)
        requests.post(f"{url}/channel/addowner", json=invalid_both_id)

def test_http_channel_addowner_already_owner(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    make_owner_owner = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_owner['u_id']
    }

    with pytest.raises(InputError):
        requests.post(f"{url}/channel/addowner", json=make_owner_owner)

def test_http_channel_addowner_invalid_token(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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

    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/addowner", json=empty_token)
        requests.post(f"{url}/channel/addowner", json=invalid_token)

def test_http_channel_addowner_success(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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

    invalid_both_id = {
        'token': login_owner['token'],
        'channel_id': invalid_id,
        'u_id': invalid_id
    }

    with pytest.raises(InputError):
        requests.post(f"{url}/channel/removeowner", json=invalid_channel_id)
        requests.post(f"{url}/channel/removeowner", json=invalid_u_id)
        requests.post(f"{url}/channel/removeowner", json=invalid_both_id)

def test_http_channel_removeowner_not_owner(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    remove_owner_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }

    with pytest.raises(InputError):
        requests.post(f"{url}/channel/removeowner", json=remove_owner_user)

def test_http_channel_removeowner_invalid_token(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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

    with pytest.raises(AccessError):
        requests.post(f"{url}/channel/removeowner", json=empty_token)
        requests.post(f"{url}/channel/removeowner", json=invalid_token)

def test_http_channel_removeowner_success(url):
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    login_owner = r.json()

    channels_create = {
        'token': login_owner['token'],
        'name': "channel",
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create)
    channel_id = r.json()

    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    login_user = r.json()

    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

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
    