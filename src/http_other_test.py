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

#tests for users_all
def test_http_users_all_invalid_token(url):
    clear()

    invalid_token = {
        'token': "invalid_token"
    }

    empty_token = {
        'token' : ""
    }

    r = requests.get(f"{url}/users/all", json=invalid_token)
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.get(f"{url}/users/all", json=empty_token)
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

def test_http_users_all_successful(url):
    clear()

    login_owner = reg_owner()
    owner_token = {
        'token': login_owner['token']
    }

    r = requests.get(f"{url}/users/all", json=owner_token)
    all_users = r.json()
    assert all_users['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}]

    login_user = reg_user()

    r = requests.get(f"{url}/users/all", json=owner_token)
    all_users = r.json()
    assert all_users['users'] == [{'u_id' : login_owner['u_id'], 'email' : "owner@email.com", 'name_first' : "Owner", 'name_last' : "Test", 'handle_str' : "ownertest"}, {'u_id' : login_user['u_id'], 'email' : "user@email.com", 'name_first' : "User", 'name_last' : "Test", 'handle_str' : "usertest"}]

#tests for http_admin_userpermission_change
def test_http_admin_userpermission_change_invalid_id(url):
    clear()

    login_owner = reg_owner()
    login_user = reg_user()
    invalid_id = -1

    invalid_u_id = {
        'token': login_owner['token'],
        'u_id': invalid_id,
        'permission_id': 1
    }

    invalid_permission_id = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': invalid_id
    }

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_u_id)
    payload = r.json
    assert payload['message'] == "Target does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_permission_id)
    payload = r.json
    assert payload['message'] == "Permission id is not valid"
    assert payload['code'] == 400

def test_http_admin_userpermission_change_invalid_token(url):
    clear()

    login_owner = reg_owner()
    login_user = reg_user()

    empty_token = {
        'token': "",
        'u_id': login_user['u_id'],
        'permission_id': 1
    }

    invalid_token = {
        'token': login_user['token'],
        'u_id': login_owner['u_id'],
        'permission_id': 2
    }

    r = requests.post(f"{url}/admin/userpermission/change", json=empty_token)
    payload = r.json
    assert payload['message'] == "Token does not exist"
    assert payload['code'] == 400

    r = requests.post(f"{url}/admin/userpermission/change", json=invalid_token)
    payload = r.json
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400

def test_http_admin_userpermission_change_successful(url):
    clear()

    login_owner = reg_owner()
    login_user = reg_user()

    make_user_owner = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': 1
    }
    requests.post(f"{url}/admin/userpermission/change", json=make_user_owner)

    make_owner_user = {
        'token': login_user['token'],
        'u_id': login_owner['u_id'],
        'permission_id': 2
    }
    requests.post(f"{url}/admin/userpermission/change", json=make_owner_user)

    owner_denied = {
        'token': login_owner['token'],
        'u_id': login_user['u_id'],
        'permission_id': 2
    }
    r = requests.post(f"{url}/admin/userpermission/change", json=owner_denied)
    payload = r.json()
    assert payload['message'] == "User is not authorised"
    assert payload['code'] == 400
