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

# Register user function
def register_owner(url):
    """Registers an owner."""
    register_owner = {
        "email": "owner@email.com",
        "password": "password123",
        "name_first": "Flock",
        "name_last": "Owner",
    }
    r = requests.post(f"{url}/auth/register", json = register_owner)
    return r.json()

# Register user function
def register_user(url):
    """Registers a user."""
    register_user = {
        "email": "user@email.com",
        "password": "password321",
        "name_first": "New",
        "name_last": "User",
    }
    r = requests.post(f"{url}/auth/register", json = register_user)
    return r.json()

# TEST FUNCTIONS FOR HTTP_USER_PROFILE
# Success for user profile
def test_http_user_profile_success1(url):
    """Tests for success when a registered user can view own profile."""
    clear()
    login_owner = register_owner(url)
    owner_info = {
        "token": login_owner["token"],
        "u_id": login_owner["u_id"],
    }
    r = requests.get(f"{url}/user/profile", json = owner_info)
    payload = r.json()
    assert payload["user"] == [{"u_id": 1, "email": "owner@gmail.com", "name_first": "Flock", "name_last" : "Owner", "handle_str" : "flockowner"}]

def test_http_user_profile_success2(url):
    """Tests for success when a registered user can view another user's profile."""
    clear()
    login_owner = register_owner(url)
    login_user = register_user(url)
    user_info = {
        "token": login_owner["token"],
        "u_id": login_user["u_id"],
    }
    r = requests.get(f"{url}/user/profile", json = user_info)
    payload = r.json()
    assert payload["user"] == [{"u_id": 2, "email": "user@gmail.com", "name_first": "New", "name_last" : "User", "handle_str" : "newuser"}]

# Failure for user profile
def test_user_profile_invalid_u_id():
    """Tests for failure to display a registered user's own profile."""
    clear()
    login_owner = register_owner(url)
    invalid_u_id = -1
    invalid_user_info = {
        "token": login_owner["token"],
        "u_id": invalid_u_id,
    }
    r = requests.get(f"{url}/user/profile", json = invalid_user_info)
    payload = r.json()
    assert payload['message'] == "User does not exist"
    assert payload['code'] == 400

    

# put
#def test_http_user_profile_setname():

# put
#def test_http_user_profile_setemail():

# put
#def test_http_user_profile_sethandle():
