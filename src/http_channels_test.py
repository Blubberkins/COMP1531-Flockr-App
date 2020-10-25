from time import sleep
from subprocess import Popen, PIPE
import json
import re
import signal
import pytest
import requests
from error import InputError
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

# invite user function
def inv_user(url, login_owner, channel_id, login_user):
    invite_user = {
        'token': login_owner['token'],
        'channel_id': channel_id['channel_id'],
        'u_id': login_user['u_id']
    }
    requests.post(f"{url}/channel/invite", json=invite_user)

# show channel details function
def chan_details(url, login_user, channel_id):
    channel_details = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }
    r = requests.get(f"{url}/channel/details", json=channel_details)
    return r.json()

# join channel function
def join_channel(url, login_user, channel_id):
    join_public_channel = {
        'token': login_user['token'],
        'channel_id': channel_id['channel_id']
    }
    requests.post(f"{url}/channel/join", json=join_public_channel)
    return r.json()

# create public channel function
def create_public_channel(url, login_owner, channel_name):
    channels_create_public = {
        'token': login_owner['token'],
        'name': channel_name,
        'is_public': True
    }
    r = requests.post(f"{url}/channels/create", json=channels_create_public)
    return r.json()

# create private channel function
def create_private_channel(url, login_owner, channel_name):
    channels_create_private = {
        'token': login_owner['token'],
        'name': channel_name,
        'is_public': False
    }
    r = requests.post(f"{url}/channels/create", json=channels_create_private)
    return r.json()

# list channels function
def list_channels(url, login_user):
    channels_list = {
        'token': login_user['token']
    }
    r = requests.get(f"{url}/channels/list", json=channels_list)
    return r.json()

# list channels function
def listall_channels(url, login_user):
    channels_listall = {
        'token': login_user['token']
    }
    r = requests.get(f"{url}/channels/listall", json=channels_listall)
    return r.json()


#
# TEST FUNCTIONS FOR CHANNELS_LIST
#

# No channels are available
def test_http_channels_list_no_channels(url):
    clear()

    login_user = reg_user(url)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels": []}

# Owner creates one public channel
def test_http_channels_list_create_one_public_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")
    channels_list = list_channels(url, login_owner)

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one private channel
def test_http_channels_list_create_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_private_channel(url, login_owner, "channel")
    channels_list = list_channels(url, login_owner)

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public channel and one private channel
def test_http_channels_list_create_one_public_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(ur, login_owner, "channel 2")
    channels_list = list_channels(url, login_owner)

    assert channels_list == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

# Owner creates one public channel and user does not join that channel
def test_http_channels_list_not_join_one_public_channel(url):
    clear()

    login_owner = reg_owner(url)

    create_public_channel(url, login_owner, "channel 1")

    login_user = reg_user(url)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels" : []}

# Owner creates one public channel and user joins that channel
def test_http_channels_list_join_one_public_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels": [{"channel_id": channel_id['channel_id'], "name": "channel"}]}

# Owner creates one private channel and user does not join that channel
def test_http_channels_list_not_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    create_private_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels": []}

# Owner creates one private channel and user joins that channel
def test_http_channels_list_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_private_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    inv_user(url, login_owner, channel_id, login_user)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels" : [{"channel_id": channel_id['channel_id'], "name": "channel"}]}

# Owner creates one public and one private channel and user joins the public channel
def test_http_channels_list_join_one_public_not_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id_1)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}]}

# Owner creates one public and one private channel and user joins the private channel
def test_http_channels_list_not_join_one_public_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    inv_user(url, login_owner, channel_id_2, login_user)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels": [{"channel_id": channel_id_2['channel_id'], "name": "channel 2"}]}

# Owner creates one public and one private channel and user joins both channels
def test_http_channels_list_join_one_public_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id_1)
    inv_user(url, login_owner, channel_id_2, login_user)

    channels_list = list_channels(url, login_user)

    assert channels_list == {"channels": [{"channel_id": channel_id_1['channel_id'], "name": "channel 1"}, {"channel_id": channel_id_2['channel_id'], "name": "channel 2"}]}

#
# TEST FUNCTIONS FOR CHANNELS_LISTALL
#

# No channels are available
def test_http_channels_listall_no_channels(url):
    clear()

    login_user = reg_user(url)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels" : []}

# Owner creates one public channel and user does not join that channel
def test_http_channels_listall_not_join_one_public_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    channels_listall = listall_channels(login_user)

    assert channels_listall == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public channel and user joins that channel
def test_http_channels_listall_join_one_public_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{"channel_id": channel_id['channel_id'], "name": "channel"}]}

# Owner creates one private channel and user does not join that channel
def test_http_channels_listall_not_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_private_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{'channel_id': channel_id['channel_id'], 'name': 'channel'}]}

# Owner creates one private channel and user joins that channel
def test_http_channels_listall_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_private_channel(url, login_owner, "channel")

    login_user = reg_user(url)

    inv_user(url, login_owner, channel_id, login_user)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{"channel_id": channel_id['channel_id'], "name": "channel"}]}

# Owner creates one public and one private channel and user joins the public channel
def test_http_channels_listall_join_one_public_not_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id_1)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{"channel_id": channel_id_1['channel_id'], "name": "channel 1"}, {"channel_id": channel_id_2['channel_id'], "name": "channel 2"}]}

# Owner creates one public and one private channel and user joins the private channel
def test_http_channels_listall_not_join_one_public_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    inv_user(login_owner, channel_id_2, login_user)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{"channel_id": channel_id_1['channel_id'], "name": "channel 1"}, {"channel_id": channel_id_2['channel_id'], "name": "channel 2"}]}

# Owner creates one public and one private channel and user joins both channels
def test_http_channels_listall_join_one_public_join_one_private_channel(url):
    clear()

    login_owner = reg_owner(url)

    channel_id_1 = create_public_channel(url, login_owner, "channel 1")
    channel_id_2 = create_private_channel(url, login_owner, "channel 2")

    login_user = reg_user(url)

    join_channel(url, login_user, channel_id_1)
    inv_user(url, login_owner, channel_id_2, login_user)

    channels_listall = listall_channels(url, login_user)

    assert channels_listall == {"channels": [{"channel_id": channel_id_1['channel_id'], "name": "channel 1"}, {"channel_id": channel_id_2['channel_id'], "name": "channel 2"}]}

#
# TEST FUNCTIONS FOR CHANNELS_CREATE
#

# Create one public channel successfully with channel name 20 characters long
def test_http_channels_create_public_success(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_public_channel(url, login_owner, "abcdefghijklmnopqrst")
    channel_details = chan_details(url, login_owner, channel_id)

    assert channel_details == {"name": "abcdefghijklmnopqrst",
                               "owner_members": [{"u_id": login_owner['u_id'], "name_first": "Owner", "name_last": "Test"}],
                               "all_members": [{"u_id": login_owner['u_id'], "name_first": "Owner", "name_last": "Test"}]}

# Create one public channel unsuccessfully with channel name > 20 characters long
def test_http_channels_create_public_unsuccess(url):
    clear()

    login_owner = reg_owner(url)

    payload = create_public_channel(url, login_owner, "abcdefghijklmnopqrstu")

    assert payload['message'] == "Name is more than 20 characters long."
    assert payload['code'] == 400

# Create one private channel successfully with channel name 20 characters long
def test_http_channels_create_private_success(url):
    clear()

    login_owner = reg_owner(url)

    channel_id = create_private_channel(url, login_owner, "abcdefghijklmnopqrst")
    channel_details = chan_details(url, login_owner, channel_id)

    assert channel_details == {"name": "abcdefghijklmnopqrst",
                               "owner_members": [{"u_id": login_owner['u_id'], "name_first": "Owner", "name_last": "Test"}],
                               "all_members" : [{"u_id": login_owner['u_id'], "name_first": "Owner", "name_last": "Test"}]}

# Create one private channel unsuccessfully with channel name > 20 characters long
def test_http_channels_create_private_unsuccess(url):
    clear()

    login_owner = reg_owner(url)

    payload = create_private_channel(url, login_owner, "abcdefghijklmnopqrstu")

    assert payload['message'] == "Name is more than 20 characters long."
    assert payload['code'] == 400
