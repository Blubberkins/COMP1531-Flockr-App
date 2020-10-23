import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear
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

#register owner function
def reg_owner():
    register_owner = {
        'email': "owner@email.com",
        'password': "password123",
        'name_first': "Owner",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    return r.json()

#register user function
def reg_user():
    register_user = {
        'email': "user@email.com",
        'password': "password321",
        'name_first': "User",
        'name_last': "Test"
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    return r.json()

#testa for http_users_all
def test_http_users_all_invalid_token(url):
    clear()
    invalid_token = {
        'token': "invalid_token"
    }

    empty_token = {
        'token': ""
    }

    r = requests.get(f"{url}/users/all", json=invalid_token)
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.get(f"{url}/users/all", json=empty_token)
    payload = r.json()
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

def test_users_all_successful(url):
    clear()

    login_owner = reg_owner
    owner_token = {
        'token': login_owner['token']
    }

    r = requests.get(f"{url}/users/all", json=owner_token)
    users_owner = r.json()
