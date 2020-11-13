import auth
import user
import pytest
from error import InputError, AccessError
from other import clear
import flask
from data import data

# TEST FUNCTIONS FOR USER_PROFILE_UPLOADPHOTO
# Failure for upload photo

def test_user_profile_invalid_token():
    "Tests for failure when the token is invalid"
    clear()
    user_info = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    img_url = "https://i.pinimg.com/originals/43/d8/55/43d855657208611181d1522c2699fe50.jpg"
    
    user.user_profile_uploadphoto(user_info["token"], img_url, 0, 0, 500, 500)
  
    hi = data["users"]
    assert hi[0]["profile_img_url"] == "/static/newuser.jpg"

