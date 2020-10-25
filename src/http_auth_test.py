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

def register_user1(url):
    register_user1 = {
        'email': "validemail@gmail.com",
        'password': "python123",
        'name_first': "New",
        'name_last': "User"
    }
    r = requests.post(f"{url}/auth/register", json=register_user1)
    user = r.json()
    return user

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

def logout_user2(url, registered_user2):
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

# TEST FUNCTIONS FOR HTTP_AUTH_LOGIN
# Success for login
def test_http_login_success(url):
    clear()

    registered_user1 = register_user1(url)
    logout_user1(url, registered_user1)
    loggedin_user1 = login_user1(url)
    assert registered_user1["u_id"] == loggedin_user1["u_id"]
    assert registered_user1["token"] == loggedin_user1["token"]

    registered_user2 = register_user2(url)
    logout_user2(url,registered_user2)
    loggedin_user2 = login_user2(url)
    assert registered_user2["u_id"] == loggedin_user2["u_id"]
    assert registered_user2["token"] == loggedin_user2["token"]

# Failure for login
def test_http_login_empty(url):
    clear()

    registered_user1 = register_user1(url)
    logout_user1(url, registered_user1)

    empty_login = {
        'email': '',
        'password': '',
    }

    r = requests.post(f"{url}/auth/login", json=empty_login)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

def test_http_login_invalid_email(url):
    clear()

    registered_user1 = register_user1(url)
    logout_user1(url, registered_user1)

    invalid_email1 = {
        'email': 'email',
        'password': '',
    }

    r = requests.post(f"{url}/auth/login", json=invalid_email1)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

    invalid_email2 = {
        'email': 'email.com',
        'password': '',
    }

    r = requests.post(f"{url}/auth/login", json=invalid_email2)
    payload = r.json()
    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

def test_http_login_unregistered_email(url):
    clear()

    registered_user1 = register_user1(url)
    logout_user1(url, registered_user1)

    unregistered_email = {
        'email': 'unusedemail@gmail.com',
        'password': 'python123',
    }
    r = requests.post(f"{url}/auth/login", json=unregistered_email)
    payload = r.json()
    assert payload['message'] == "Invalid email or password"
    assert payload['code'] == 400

def test_http_login_invalid_password(url):
    clear()

    registered_user1 = register_user1(url)
    logout_user1(url, registered_user1)

    incorrect_password = {
        'email' : 'validemail@gmail.com',
        'password' : '123python',
    }

    r = requests.post(f"{url}/auth/login", json=incorrect_password)
    payload = r.json()
    assert payload['message'] == "Invalid email or password"
    assert payload['code'] == 400

# TEST FUNCTIONS FOR HTTP_AUTH_LOGOUT
# Success for logout
def test_http_logout_success(url):
    clear()

    registered_user1 = register_user1(url)
    loggedout_user1 = logout_user1(url, registered_user1)

    assert loggedout_user1["is_success"] == [True]

# Failure for logout
def test_http_logout_failure(url):
    clear()
    
    register_user1(url)
    invalid_logout = {
        'token' : "invalid_token"
    }

    r = requests.post(f"{url}/auth/login", json=invalid_logout)
    payload = r.json()

    assert payload["is_success"] == [False]

# TEST FUNCTIONS FOR AUTH_REGISTER
# Success for register

def test_http_register_success(url):
    clear()

    registered_user1 = register_user1(url)

    assert registered_user1["u_id"] == 1

    registered_user2 = register_user2(url)

    assert registered_user2["u_id"] == 2

# Failure for register

def test_http_register_invalid_email(url):
    clear()

    register_invalid_email = {
        'email' : "invalidemail.com",
        'password' : "python123",
        'name_first' : "New",
        'name_last' : "User",
    }

    r = requests.post(f"{url}/auth/register", json=register_invalid_email)
    payload = r.json()

    assert payload['message'] == "Invalid email"
    assert payload['code'] == 400

def test_http_register_already_used_email(url):
    clear()

    registered_user1 = register_user1(url)
    assert registered_user1["u_id"] == 1

    register_existing_email = {
        'email' : "validemail@gmail.com",
        'password' : "differentpassword123",
        'name_first' : "Old",
        'name_last' : "User",
    }
    
    r = requests.post(f"{url}/auth/register", json=register_existing_email)
    payload = r.json()

    assert payload['message'] == "Email is already in use"
    assert payload['code'] == 400

def test_http_register_invalid_password(url):
    clear()

    short_password = {
        'email' : "validemail@gmail.com",
        'password' : "pass",
        'name_first' : "New",
        'name_last' : "User",
    }

    r = requests.post(f"{url}/auth/register", json=short_password)
    payload = r.json()

    assert payload['message'] == "Invalid password"
    assert payload['code'] == 400

    no_password = {
        'email' : "differentvalidemail@gmail.com",
        'password' : "",
        'name_first' : "New",
        'name_last' : "User",
    }

    r = requests.post(f"{url}/auth/register", json=no_password)
    payload = r.json()

    assert payload['message'] == "Invalid password"
    assert payload['code'] == 400

def test_http_register_invalid_first_name(url):
    clear()

    short_first_name = {
        'email' : "validemail@gmail.com",
        'password' : "python123",
        'name_first' : "",
        'name_last' : "User",
    }

    r = requests.post(f"{url}/auth/register", json=short_first_name)
    payload = r.json()

    assert payload['message'] == "Invalid first name"
    assert payload['code'] == 400


    long_first_name = {
        'email' : "notthesamevalidemail@gmail.com",
        'password' : "python123",
        'name_first' : "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
        'name_last' : "User",
    }

    r = requests.post(f"{url}/auth/register", json=long_first_name)
    payload = r.json()

    assert payload['message'] == "Invalid first name"
    assert payload['code'] == 400

def test_http_register_invalid_last_name(url):
    clear()

    short_last_name = {
        'email' : "validemail@gmail.com",
        'password' : "python123",
        'name_first' : "New",
        'name_last' : "",
    }

    r = requests.post(f"{url}/auth/register", json=short_last_name)
    payload = r.json()

    assert payload['message'] == "Invalid last name"
    assert payload['code'] == 400


    long_last_name = {
        'email' : "notthesamevalidemail@gmail.com",
        'password' : "python123",
        'name_first' : "New",
        'name_last' : "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
    }

    r = requests.post(f"{url}/auth/register", json=long_last_name)
    payload = r.json()

    assert payload['message'] == "Invalid last name"
    assert payload['code'] == 400
