from time import sleep
from subprocess import Popen, PIPE
import json
import re
import signal
import pytest
import requests
from error import InputError, AccessError
from other import clear
from flask import request

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

# Test for url
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
    r = requests.post(url + "auth/register", json=register_owner)
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
    r = requests.post(url + "auth/register", json=register_user)
    return r.json() 

# Get user profile
def get_user_profile(url, token, u_id):
    """Gets the user's profile."""
    r = requests.get(url + "user/profile", params={"token": token, "u_id": u_id})
    return r.json()


# TEST FUNCTIONS FOR HTTP_USER_PROFILE
# Success for user profile
def test_http_user_profile_success1(url):
    """Tests for success when a registered user can view own profile."""
    clear()
    login_owner = register_owner(url)
    payload = get_user_profile(url, login_owner["token"], login_owner["u_id"])
    assert payload["user"] == {"u_id": 1, "email": "owner@gmail.com", "name_first": "Flock", "name_last": "Owner", "handle_str": "flockowner", "profile_img_url": ""}

def test_http_user_profile_success2(url):
    """Tests for success when a registered user can view another user's profile."""
    clear()
    register_owner(url)
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"] == {"u_id": 2, "email": "user@gmail.com", "name_first": "New", "name_last": "User", "handle_str": "newuser", "profile_img_url": ""}

# Failure for user profile
def test_http_user_profile_invalid_u_id(url):
    """Tests for failure to display a registered user's own profile."""
    clear()
    login_owner = register_owner(url)
    invalid_u_id = -1
    payload = get_user_profile(url, login_owner["token"], invalid_u_id)
    assert payload["message"] == "<p>Invalid user_id</p>"
    assert payload["code"] == 400

# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETNAME
# Success for set name
def test_http_user_profile_setname_success(url):
    """Tests for success when a user changes their first and last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["name_first"] == "New"
    assert payload["user"]["name_last"] == "User"

    new_name= {
        "token": login_user["token"],
        "name_first": "Python",
        "name_last": "Programmer",
    }
    requests.put(url + "user/profile/setname", json=new_name)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["name_first"] == new_name["name_first"]
    assert payload["user"]["name_last"] == new_name["name_last"]

# Failure for set name
def test_http_user_profile_setname_invalid_firstname(url):
    """Tests for failure when a user inputs an invalid first name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["name_first"] == "New"
    assert payload["user"]["name_last"] == "User"

    empty_name_first = {
        "token": login_user["token"],
        "name_first": "",
        "name_last": "Programmer",
    }
    r = requests.put(url + "user/profile/setname", json=empty_name_first)
    payload = r.json()
    assert payload["message"] == "<p>Invalid first name</p>"
    assert payload["code"] == 400

    invalid_name_first = {
        "token": login_user["token"],
        "name_first": "Pythonpythonpythonpythonpythonpythonpythonpythonpython",
        "name_last": "Programmer",
    }
    r = requests.put(url + "user/profile/setname", json=invalid_name_first)
    payload = r.json()
    assert payload["message"] == "<p>Invalid first name</p>"
    assert payload["code"] == 400

def test_http_user_profile_setname_invalid_lastname(url):
    """Tests for failure when a user inputs an invalid last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["name_first"] == "New"
    assert payload["user"]["name_last"] == "User"

    empty_name_last = {
        "token": login_user["token"],
        "name_first": "Python",
        "name_last": "",
    }
    r = requests.put(url + "user/profile/setname", json=empty_name_last)
    payload = r.json()
    assert payload["message"] == "<p>Invalid last name</p>"
    assert payload["code"] == 400

    invalid_name_last = {
        "token": login_user["token"],
        "name_first": "Python",
        "name_last": "Programmerprogrammerprogrammerprogrammerprogrammerprogrammer",
    }
    r = requests.put(url + "user/profile/setname", json=invalid_name_last)
    payload = r.json()
    assert payload["message"] == "<p>Invalid last name</p>"
    assert payload["code"] == 400

def test_http_user_profile_setname_invalid_firstlastname(url):
    """Tests for failure when a user inputs an invalid firs and last name."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["name_first"] == "New"
    assert payload["user"]["name_last"] == "User"

    empty_name = {
        "token": login_user["token"],
        "name_first": "",
        "name_last": "",
    }
    r = requests.put(url + "user/profile/setname", json=empty_name)
    payload = r.json()
    assert payload["message"] == "<p>Invalid first name</p>"
    assert payload["code"] == 400

    invalid_name = {
        "token": login_user["token"],
        "name_first": "Pythonpythonpythonpythonpythonpythonpythonpythonpython",
        "name_last": "Programmerprogrammerprogrammerprogrammerprogrammerprogrammer",
    }
    r = requests.put(url + "user/profile/setname", json=invalid_name)
    payload = r.json()
    assert payload["message"] == "<p>Invalid first name</p>"
    assert payload["code"] == 400

# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETEMAIL
# Success for set email
def test_http_user_profile_setemail_success(url):
    """Tests for success when a user changes their email."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["email"] == "user@gmail.com"

    new_email = {
        "token": login_user["token"],
        "email": "pythoniscool@gmail.com",
    }
    requests.put(url + "user/profile/setemail", json=new_email)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["email"] == new_email["email"]
    
# Failure for set email
def test_http_user_profile_invalid_email(url):
    """Tests for failure when a user inputs an invalid email address."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["email"] == "user@gmail.com"

    empty_email = {
        "token": login_user["token"],
        "email": "",
    }
    r = requests.put(url + "user/profile/setemail", json=empty_email)
    payload = r.json()
    assert payload["message"] == "<p>Invalid email</p>"
    assert payload["code"] == 400

    invalid_email = {
        "token": login_user["token"],
        "email": "email@email",
    }
    r = requests.put(url + "user/profile/setemail", json=invalid_email)
    payload = r.json()
    assert payload["message"] == "<p>Invalid email</p>"
    assert payload["code"] == 400
        
def test_http_user_profile_email_already_in_use(url):
    """Tests for failure when a user inputs a email that is already in use."""
    clear()
    login_owner = register_owner(url)
    login_user = register_user(url)
    owner_info = get_user_profile(url, login_owner["token"], login_owner["u_id"])
    assert owner_info["user"]["email"] == "owner@gmail.com"

    owner_email = {
        "token": login_user["token"],
        "email": owner_info["user"]["email"],
    }
    r = requests.put(url + "user/profile/setemail", json=owner_email)
    payload = r.json()
    assert payload["message"] == "<p>Email is already in use</p>"
    assert payload["code"] == 400
       
# TEST FUNCTIONS FOR HTTP_USER_PROFILE_SETHANDLE
# Success for set handle
def test_http_user_profile_sethandle_success(url):
    """Tests for success when a user changes their handle."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["handle_str"] == "newuser"

    new_handle = {
        "token": login_user["token"],
        "handle_str": "pythonprogrammer",
    }
    requests.put(url + "user/profile/sethandle", json=new_handle)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["handle_str"] == new_handle["handle_str"]
    
# Failure for set handle
def test_http_user_profile_invalid_handle(url):
    """Tests for failure when a user inputs an invalid handle."""
    clear()
    login_user = register_user(url)
    payload = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert payload["user"]["handle_str"] == "newuser"

    empty_handle = {
        "token": login_user["token"],
        "handle_str": "",
    }
    r = requests.put(url + "user/profile/sethandle", json=empty_handle)
    payload = r.json()
    assert payload["message"] == "<p>Invalid handle</p>"
    assert payload["code"] == 400

    invalid_handle = {
        "token": login_user["token"],
        "handle_str": "iamaprettygoodpythonprogrammer",
    }
    r = requests.put(url + "user/profile/sethandle", json=invalid_handle)
    payload = r.json()
    assert payload["message"] == "<p>Invalid handle</p>"
    assert payload["code"] == 400

def test_http_user_profile_handle_already_in_use(url):
    """Tests for failure when a user inputs a handle that is already in use."""
    clear()
    login_owner = register_owner(url)
    login_user = register_user(url)
    user_info = get_user_profile(url, login_user["token"], login_user["u_id"])
    assert user_info["user"]["handle_str"] == "newuser"

    new_owner_handle = {
        "token": login_owner["token"],
        "handle_str": user_info["user"]["handle_str"],
    }
    r = requests.put(url + "user/profile/sethandle", json=new_owner_handle)
    payload = r.json()
    assert payload["message"] == "<p>Handle is already in use</p>"
    assert payload["code"] == 400

    owner_info = get_user_profile(url, login_owner["token"], login_owner["u_id"])
    assert owner_info["user"]["handle_str"] == "flockowner"

    new_user_handle = {
        "token": login_user["token"],
        "handle_str": owner_info["user"]["handle_str"],
    }
    r = requests.put(url + "user/profile/sethandle", json=new_user_handle)
    payload = r.json()
    assert payload["message"] == "<p>Handle is already in use</p>"
    assert payload["code"] == 400

# TEST FUNCTIONS FOR HTTP_USER_PROFILE_UPLOADPHOTO
# Failure for upload photo
def test_http_user_profile_invalid_token(url):
    "Tests for failure when the token is invalid"
    clear()
    register_user(url)

    invalid_token = {
        "token" : "invalid_token",
        "img_url": "",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_token)
    payload = r.json()
    assert payload["message"] == "<p>Invalid permissions</p>"
    assert payload["code"] == 400

def test_http_user_profile_invalid_url(url):
    "Tests for failure when the user inputs an invalid url"
    clear()
    login_user = register_user(url)

    empty_url = {
        "token" : login_user["token"],
        "img_url": "",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=empty_url)
    payload = r.json()
    assert payload["message"] == "<p>Invalid url</p>"
    assert payload["code"] == 400

    invalid_url = {
        "token" : login_user["token"],
        "img_url": "ilikepython.jpeg",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_url)
    payload = r.json()
    assert payload["message"] == "<p>Invalid url</p>"
    assert payload["code"] == 400

def test_http_user_profile_image_not_jpg(url):
    "Tests for failure when the image is not a jpg/jpeg"
    clear()
    login_user = register_user(url)

    png = {
        "token" : login_user["token"],
        "img_url": "https://static.wikia.nocookie.net/hellokitty/images/3/33/Sanrio_Characters_My_Melody_Image029.png",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 200, 
        "y_end": 200
    }
    r = requests.post(url + "user/profile/uploadphoto", json=png)
    payload = r.json()
    assert payload["message"] == "<p>Image is not in jpg/jpeg format</p>"
    assert payload["code"] == 400

    gif = {
        "token" : login_user["token"],
        "img_url": "https://media1.tenor.com/images/b996ab4668b7bf2babacc91484b0d223/tenor.gif?itemid=10838396",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 200, 
        "y_end": 200
    }
    r = requests.post(url + "user/profile/uploadphoto", json=gif)
    payload = r.json()
    assert payload["message"] == "<p>Image is not in jpg/jpeg format</p>"
    assert payload["code"] == 400

def test_http_user_profile_x_start_out_of_bounds(url):
    "Tests for failure when the user inputs an invalid x1 value"
    clear()
    login_user = register_user(url)
    img_url = "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg"
    width = 1200

    invalid_x_start1 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": -100,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_start1)
    payload = r.json()
    assert payload["message"] == "<p>x1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_x_start2 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 2000,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_start2)
    payload = r.json()
    assert payload["message"] == "<p>x1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_x_start3 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": width,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_start3)
    payload = r.json()
    assert payload["message"] == "<p>x1 out of bounds</p>"
    assert payload["code"] == 400

def test_http_user_profile_y_start_out_of_bounds(url):  
    "Tests for failure when the user inputs an invalid y1 value"
    clear()
    login_user = register_user(url)
    img_url = "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg"
    height = 2134

    invalid_y_start1 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": -100, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_start1)
    payload = r.json()
    print("test 1")
    assert payload["message"] == "<p>y1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_y_start2 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": 2500, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_start2)
    payload = r.json()
    print("test 2")
    assert payload["message"] == "<p>y1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_y_start3 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": height, 
        "x_end": 500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_start3)
    payload = r.json()
    print("test 3")
    assert payload["message"] == "<p>y1 out of bounds</p>"
    assert payload["code"] == 400

def test_http_user_profile_x_end_out_of_bounds(url):
    "Tests for failure when the user inputs an invalid x2 value"
    clear()
    login_user = register_user(url)
 
    invalid_x_end1 = {
        "token" : login_user["token"],
        "img_url": "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg",
        "x_start": 0,
        "y_start": 0, 
        "x_end": -100, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_end1)
    payload = r.json()
    assert payload["message"] == "<p>x2 out of bounds</p>"
    assert payload["code"] == 400

    invalid_x_end2 = {
        "token" : login_user["token"],
        "img_url": "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 2500, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_end2)
    payload = r.json()
    assert payload["message"] == "<p>x2 out of bounds</p>"
    assert payload["code"] == 400

    invalid_x_end3 = {
        "token" : login_user["token"],
        "img_url": "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg",
        "x_start": 0,
        "y_start": 0, 
        "x_end": 0, 
        "y_end": 500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_x_end3)
    payload = r.json()
    assert payload["message"] == "<p>x2 out of bounds</p>"
    assert payload["code"] == 400

def test_http_user_profile_y_end_out_of_bounds(url):  
    "Tests for failure when the user inputs an invalid y2 value"
    clear()
    login_user = register_user(url)
    img_url = "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg"
    
    invalid_y_end1 = {
        "token": login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": -100
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_end1)
    payload = r.json()
    assert payload["message"] == "<p>y2 out of bounds</p>"
    assert payload["code"] == 400

    invalid_y_end2 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 2500
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_end2)
    payload = r.json()
    assert payload["message"] == "<p>y2 out of bounds</p>"
    assert payload["code"] == 400

    invalid_y_end3 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": 0, 
        "x_end": 500, 
        "y_end": 0
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_y_end3)
    payload = r.json()
    assert payload["message"] == "<p>y2 out of bounds</p>"
    assert payload["code"] == 400

def test_http_user_profile_all_out_of_bounds(url):  
    "Tests for failure when the user inputs invalid x1, y1, x2, y2 values"
    clear()
    login_user = register_user(url)
    img_url = "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg"

    invalid_all1 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": -1,
        "y_start": -1, 
        "x_end": -1, 
        "y_end": -1
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_all1)
    payload = r.json()
    assert payload["message"] == "<p>x1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_all2 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 3000,
        "y_start": 3000, 
        "x_end": 3000, 
        "y_end": 3000
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_all2)
    payload = r.json()
    assert payload["message"] == "<p>x1 out of bounds</p>"
    assert payload["code"] == 400

    invalid_all3 = {
        "token" : login_user["token"],
        "img_url": img_url,
        "x_start": 0,
        "y_start": 0, 
        "x_end": 0, 
        "y_end": 0
    }
    r = requests.post(url + "user/profile/uploadphoto", json=invalid_all3)
    payload = r.json()
    assert payload["message"] == "<p>x2 out of bounds</p>"
    assert payload["code"] == 400
