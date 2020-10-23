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



def register_user1(url):
    register_user1 = {
        'email': "validemail@gmail.com",
        'password': "python123",
        'name_first': "New",
        'name_last': "User"
    }
    r = requests.post(f"{url}/auth/register", json=register_user1)
    return r.json()

def register_user2(url):
    register_user2 = {
        'email': "differentvalidemail@gmail.com",
        'password': "python123",
        'name_first': "New",
        'name_last': "User"
    }
    r = requests.post(f"{url}/auth/register", json=register_user2)
    return r.json()

def login_user1(url):
    login_user1 = {
        'email': "validemail@gmail.com",
        'password': "python123",
    }
    r = requests.post(f"{url}/auth/login", json=login_user1)
    return r.json()

def login_user2(url):
    login_user2 = {
        'email': "differentvalidemail@gmail.com",
        'password': "python123",
    }
    r = requests.post(f"{url}/auth/login", json=login_user2)
    return r.json()

def logout_user1(url, registered_user1):
    logout_user1 = {
        'token': registered_user1['token'],
    }

    r = requests.post(f"{url}/auth/logout", json=logout_user1)
    return r.json()

def logout_user2(url, registered_user1):
    logout_user2 = {
        'token': registered_user2['token'],
    }

    r = requests.post(f"{url}/auth/logout", json=logout_user2)
    return r.json()


def test_url(url):
    '''
    A simple sanity test to check that your server is set up properly
    '''
    assert url.startswith("http")

def test_http_login_success(url):
    clear()

    registered_user1 = register_user1()
    is_success1 = logout_user1(registered_user1)
    loggedin_user1 = login_user1()
    assert registered_user1["token"] == loggedin_user1["token"]

    registered_user2 = register_user2()
    is_success2 = logout_user2(registered_user2)
    loggedin_user2 = login_user2()
    assert registered_user1["token"] == loggedin_user2["token"]

# Failure to log in

def test_http_login_empty():
    clear()

    registered_user1 = register_user1()
    is_success1 = logout_user1(registered_user1)

    empty_login = {
        'email' : '',
        'password' : '',
    }

    r = requests.post(f"{url}/auth/login", json=empty_login)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

def test_http_login_invalid_email():
    clear()

    registered_user1 = register_user1()
    is_success1 = logout_user1(registered_user1)

    invalid_email1 = {
        'email' : 'email',
        'password' : '',
    }

    r = requests.post(f"{url}/auth/login", json=invalid_email1)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

    invalid_email2 = {
        'email' : 'email.com',
        'password' : '',
    }

    r = requests.post(f"{url}/auth/login", json=invalid_email2)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

def test_http_login_unregistered_email():
    clear()

    registered_user1 = register_user1()
    is_success1 = logout_user1(registered_user1)

    unregistered_email = {
        'email' : 'unusedemail@gmail.com',
        'password' : 'python123',
    }
    r = requests.post(f"{url}/auth/login", json=unregistered_email)
    payload = r.json()
    assert payload['message'] == "Invalid email or password"
    assert payload['code'] == 400

def test_http_login_invalid_password():
    clear()

    registered_user1 = register_user1()
    is_success1 = logout_user1(registered_user1)

    incorrect_password = {
        'email' : 'validemail@gmail.com',
        'password' : '123python',
    }

    r = requests.post(f"{url}/auth/login", json=incorrect_password)
    payload = r.json()
    assert payload['message'] == "Invalid email or password"
    assert payload['code'] == 400

# TESTS FOR HTTP_AUTH_LOGOUT

# Success

def test_http_logout_success():
    clear()
    registered_user1 = register_user1()
    loggedout_user1 = logout_user1(registered_user1)

    assert loggedout_user1["is_success"] == True

def test_http_logout_failure():
    clear()
    registered_user1 = register_user1()
    invalid_logout = {
        'token' : "invalid_token"
    }

    r = requests.post(f"{url}/auth/login", json=invalid_logout)
    payload = r.json()

    assert payload["is_success"] == False