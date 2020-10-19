import user
import pytest
from error import InputError
from other import clear

# TEST FUNCTIONS FOR USER_PROFILE
# Success for user profile
def test_user_profile_success():
    """Tests for success when displaying a user profile."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]
    u_id = register_user1[1]
    user_info = user_profile(token, u_id) 
    user = {
        "u_id" : 1,
        "email" : "validemail@gmail.com",
        "name_first" : "New",
        "name_last" : "User",
        "handle_str" : "newuser",
    }
    assert user_info == user

# Failure for user profile
def test_user_profile_invalid_u_id():
    """Tests for failure to display a user profile."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user_profile(token, -1)

"""
TEST FUNCTIONS FOR USER_PROFILE_SETNAME, USER_PROFILE_SETEMAIL, USER_PROFILE_SETHANDLE
Given the nature of blackbox testing and the absence of return values for the previously mentioned functions, 
blackbox tests are unable to be written for these features.
"""
