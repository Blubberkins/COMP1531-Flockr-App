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

def test_http_login_success(url):
    clear()
    register_user1 = {
        'email': "validemail@gmail.com",
        'password': "python123",
        'name_first': "New",
        'name_last': "User"
    }
    r = requests.post(f"{url}/auth/register", json=register_user1)
    registered_user1 = r.json()

    logout_user1 = {
        'token': registered_user['token'],
    }

    r = requests.post(f"{url}/auth/logout", json = logout_user1)
    is_success1 = r.json()

    login_user1 = {
        'email': "validemail@gmail.com",
        'password': "python123",
    }
    r = requests.post(f"{url}/auth/login", json=login_user1)
    loggedin_user1 = r.json()

    assert registered_user1["token"] == loggedin_user1["token"]

    register_user2 = {
    'email': "differentvalidemail@gmail.com",
    'password': "python123",
    'name_first': "New",
    'name_last': "User"
    }
    r = requests.post(f"{url}/auth/register", json=register_user2)
    registered_user2 = r.json()

    logout_user2 = {
        'token': registered_user['token'],
    }

    r = requests.post(f"{url}/auth/logout", json = logout_user2)
    is_success2 = r.json()

    login_user2 = {
        'email': "validemail@gmail.com",
        'password': "python123",
    }
    r = requests.post(f"{url}/auth/login", json=login_user2)
    loggedin_user2 = r.json()

    assert registered_user1["token"] == loggedin_user2["token"]





