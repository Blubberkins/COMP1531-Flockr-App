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
    """Tests that the server has been set up properly."""
    assert url.startswith("http")

# Register user function
def register_owner(url):
    """Registers an owner."""
    register_owner = {
        "email": "owner@gmail.com",
        "password": "password123",
        "name_first": "Flock",
        "name_last": "Owner",
    }
    r = requests.post(f"{url}/auth/register", json=register_owner)
    return r.json()

# Register user function
def register_user(url):
    """Registers a user."""
    register_user = {
        "email": "user@gmail.com",
        "password": "password321",
        "name_first": "New",
        "name_last": "User",
    }
    r = requests.post(f"{url}/auth/register", json=register_user)
    return r.json() 

# Get user profile
def get_user_profile(url, token, u_id):
    """Gets the user's profile."""
    user_info = {
        "token": token,
        "u_id": u_id,
    }
    r = requests.get(f"{url}/user/profile", json=user_info)
    return r.json()

# TEST FUNCTIONS FOR HTTP_USER_PROFILE
# Success for user profile
def test_http_user_profile_success1(url):
    """Tests for success when a registered user can view own profile."""
    clear()
    login_owner = register_owner(url)
    payload = get_owner_profile(url, login_owner["token"], login_owner["u_id"])
    assert payload["user"] == [{"u_id": 1, "email": "owner@gmail.com", "name_first": "Flock", "name_last": "Owner", "handle_str": "flockowner"}]

def test_http_user_profile_success2(url):
    """Tests for success when a registered user can view another user's profile."""
    clear()
    login_owner = register_owner(url)
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"] == [{"u_id": 2, "email": "user@gmail.com", "name_first": "New", "name_last": "User", "handle_str": "newuser"}]

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
    r = requests.get(f"{url}/user/profile", json=invalid_user_info)
    payload = r.json()
    assert payload['message'] == "User does not exist"
    assert payload['code'] == 400

# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETNAME
# Success for set name
def test_http_user_profile_setname_success(url):
    """Tests for success when a user changes their first and last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["name_first"] == ["New"]
    assert payload["user"]["name_last"] == ["User"]

    new_name= {
        "token": login_owner["token"],
        "name_first": "Python",
        "name_last": "Programmer",
    }
    requests.put(f"{url}/user/profile/setname", json=new_name)
    r = requests.get(f"{url}/user/profile", json=user_info)
    payload = r.json()
    assert payload["user"]["name_first"] == new_name["name_first"]
    assert payload["user"]["name_last"] == new_name["name_last"]

# Failure for set name
def test_http_user_profile_setname_invalid_firstname(url):
    """Tests for failure when a user inputs an invalid first name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["name_first"] == ["New"]
    assert payload["user"]["name_last"] == ["User"]

    empty_name_first = {
        "token": login_user["token"],
        "name_first": "",
        "name_last": "Programmer",
    }
    requests.put(f"{url}/user/profile/setname", json=empty_name_first)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid first name"
    assert payload["code"] == 400

    invalid_name_first = {
        "token": login_user["token"],
        "name_first": "Pythonpythonpythonpythonpythonpythonpythonpythonpython",
        "name_last": "Programmer",
    }
    requests.put(f"{url}/user/profile/setname", json=invalid_name_first)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid first name"
    assert payload["code"] == 400

def test_http_user_profile_setname_invalid_lastname(url):
    """Tests for failure when a user inputs an invalid last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["name_first"] == ["New"]
    assert payload["user"]["name_last"] == ["User"]

    empty_name_last = {
        "token": login_user["token"],
        "name_first": "Python",
        "name_last": "",
    }
    requests.put(f"{url}/user/profile/setname", json=empty_name_last)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid last name"
    assert payload["code"] == 400

    invalid_name_first = {
        "token": login_owner["token"],
        "name_first": "Python",
        "name_last": "Programmerprogrammerprogrammerprogrammerprogrammerprogrammer",
    }
    requests.put(f"{url}/user/profile/setname", json=invalid_name_last)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid last name"
    assert payload["code"] == 400

def test_http_user_profile_setname_invalid_firstlastname(url):
    """Tests for failure when a user inputs an invalid firs and last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["name_first"] == ["New"]
    assert payload["user"]["name_last"] == ["User"]

    empty_name = {
        "token": login_user["token"],
        "name_first": "",
        "name_last": "",
    }
    requests.put(f"{url}/user/profile/setname", json=empty_name)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid first name"
    assert payload["code"] == 400

    invalid_name = {
        "token": login_user["token"],
        "name_first": "Pythonpythonpythonpythonpythonpythonpythonpythonpython",
        "name_last": "Programmerprogrammerprogrammerprogrammerprogrammerprogrammer",
    }
    requests.put(f"{url}/user/profile/setname", json=invalid_name)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid first name"
    assert payload["code"] == 400

# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETEMAIL
# Success for set email
def test_http_user_profile_setemail_success():
    """Tests for success when a user changes their email."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["email"] == ["user@gmail.com"]

    new_email = {
        "token": login_user["token"],
        "email": "pythoniscool@gmail.com",
    }
    requests.put(f"{url}/user/profile/setemail", json=new_email)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["email"] == new_email["email"]
    
# Failure for set email
def test_http_user_profile_invalid_email():
    """Tests for failure when a user inputs an invalid email address."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["email"] == ["user@gmail.com"]

    empty_email = {
        "token": login_user["token"],
        "email": "",
    }
    requests.put(f"{url}/user/profile/setemail", json=empty_email)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid email"
    assert payload["code"] == 400

    invalid_email = {
        "token": login_user["token"],
        "email": "email@email",
    }
    requests.put(f"{url}/user/profile/setemail", json=invalid_email)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid email"
    assert payload["code"] == 400
        
def test_http_user_profile_email_already_in_use():
    """Tests for failure when a user inputs a email that is already in use."""
    clear()
    login_owner = register_owner(url)
    login_user = register_user(url)

    owner_email = {
        "token": login_user["token"],
        "email": "owner@gmail.com",
    }
    requests.put(f"{url}/user/profile/setemail", json=owner_email)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Email is already in use"
    assert payload["code"] == 400
       
# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETHANDLE
# Success for set handle
def test_http_user_profile_sethandle_success():
    """Tests for success when a user changes their handle."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["handle"] == "newuser"

    new_handle = {
        "token": login_user["token"],
        "handle": "pythonprogrammer",
    }
    requests.put(f"{url}/user/profile/sethandle", json=new_handle)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["handle"] == new_handle["handle"]
    
# Failure for set handle
def test_http_user_profile_invalid_handle():
    """Tests for failure when a user inputs an invalid handle."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["handle"] == "newuser"

    empty_handle = {
        "token": login_user["token"],
        "handle": "",
    }
    requests.put(f"{url}/user/profile/sethandle", json=empty_handle)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid handle"
    assert payload["code"] == 400

    invalid_handle = {
        "token": login_user["token"],
        "handle": "iamaprettygoodpythonprogrammer",
    }
    requests.put(f"{url}/user/profile/sethandle", json=invalid_handle)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid handle"
    assert payload["code"] == 400

def test_user_profile_handle_already_in_use():
    """Tests for failure when a user inputs a handle that is already in use."""
    clear()
    login_owner = register_user(url)
    login_user = register_user(url)
    payload = get_user_profile(url, login_user)
    assert payload["user"]["handle"] == "newuser"

    user_handle = {
        "token": login_owner["user"]["token"],
        "handle": login_user["user"]["handle"],
    }
    requests.put(f"{url}/user/profile/sethandle", json=user_handle)
    payload = get_owner_profile(url, login_owner)
    assert payload["message"] == "Invalid handle"
    assert payload["code"] == 400

    owner_handle = {
        "token": login_user["user"]["token"],
        "handle": login_owner["user"]["handle"],
    }
    requests.put(f"{url}/user/profile/sethandle", json=owner_handle)
    payload = get_user_profile(url, login_user)
    assert payload["message"] == "Invalid handle"
    assert payload["code"] == 400
