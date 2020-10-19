import user
import pytest
from error import InputError
from other import clear

# Test FUNCTIONS FOR USER_PROFILE
# Success for displaying user profile
def test_user_profile_success():
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

# Failure for displaying user profile
def test_user_profile_invalid_u_id():
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user_profile(token, -1)

# TEST FUNCTIONS FOR 