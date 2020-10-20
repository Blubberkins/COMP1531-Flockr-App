import user
import pytest
from error import InputError
from other import clear

# TEST FUNCTIONS FOR USER_PROFILE
# Success for user profile
def test_user_profile_success1():
    """Tests for success when a registered user can view own profile."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]
    u_id = register_user1[1]

    user_info = user.user_profile(token, u_id) 
    user = {
        "u_id" : 1,
        "email" : "validemail@gmail.com",
        "name_first" : "New",
        "name_last" : "User",
        "handle_str" : "newuser",
    }
    assert user_info == user

def test_user_profile_success2():
    """Tests for success when a registered user can view another user's profile."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    user1_token = register_user1[0]
    register_user2 = auth.auth_register("pythonthings@gmail.com", "pythonrules123", "Python", "Programmer")
    user2_u_id = register_user1[1]

    user_info = user.user_profile(user1_token, user2_u_id) 
    user = {
        "u_id" : 2,
        "email" : "pythonthings@gmail.com",
        "name_first" : "Python",
        "name_last" : "Programmer",
        "handle_str" : "pythonprogrammer",
    }
    assert user_info == user

# Failure for user profile
def test_user_profile_invalid_u_id():
    """Tests for failure to display a registered user's own profile."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile(token, -1)

# TEST FUNCTIONS FOR USER_PROFILE_SETNAME
# Success for setname
def test_user_profile_setname_success():
    """Tests for success when a user changes their first and last name."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]
    u_id = register_user1[1]
    user_info = user.user_profile(token, u_id) 
    name_first = user_info["name_first"]
    name_last = user_info["name_last"]

    assert name_first == "New"
    assert name_last == "User"

    user.user_profile_setname(token, "Flock", "Owner")
    updated_user_info = user.user_profile(token, u_id) 
    updated_name_first = updated_user_info["name_first"]
    updated_name_last = updated_user_info["name_last"]
    
    assert updated_name_first == "Flock"
    assert updated_name_last == "Owner"

# Failure for setname
def test_user_profile_setname_invalid_firstname():
    """Tests for failure when a user inputs an invalid first name."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile_setname(token, "", "Owner")
        user.user_profile_setname(token, "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "Owner")

def test_user_profile_setname_invalid_lastname():
    """Tests for failure when a user inputs an invalid last name."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile_setname(token, "Python", "")
        user.user_profile_setname(token, "Python", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")

def test_user_profile_setname_invalid_firstlastname():
    """Tests for failure when a user inputs invalid first and last names."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile_setname(token, "", "")
        user.user_profile_setname(token, "", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
        user.user_profile_setname(token, "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "")
        user.user_profile_setname(token, "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")   

# TEST FUNCTIONS FOR USER_PROFILE_SETEMAIL
# Success for set email
def test_user_profile_setemail_success():
    """Tests for success when a user changes their email."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]
    u_id = register_user1[1]
    user_info = user.user_profile(token, u_id) 
    user_email = user_info["email"]

    assert user_email == "validemail@gmail.com"

    user.user_profile_setemail(token, "newemail@gmail.com")
    updated_user_info = user.user_profile(token, u_id) 
    updated_email = updated_user_info["email"]
    
    assert updated_email = "newemail@gmail.com"
# Failure for set email
def test_user_profile_invalid_email():
    """Tests for failure when a user inputs an invalid email address."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile_setemail(token, "")
        user.user_profile_setemail(token, "              ")
        user.user_profile_setemail(token, "email")
        user.user_profile_setemail(token, "email.com")
        user.user_profile_setemail(token, "@@@@@@")
        user.user_profile_setemail(token, "email@email")
        
        
def test_user_profile_email_already_in_use():
    """Tests for failure when a user inputs a email that is already in use."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token1 = register_user1[0]
    register_user2 = auth.auth_register("differentemail@gmail.com", "321wordpass", "Different", "User")
    token2 = register_user2[0]
    register_user3 = auth.auth_register("randomperson@gmail.com", "987drowssap", "Random", "User")
    token3 = register_user3[0]

    with pytest.raises(InputError):
        user.user_profile_setemail(token2, "validemail@gmail.com")
        user.user_profile_setemail(token1, "differentemail@gmail.com")
        user.user_profile_setemail(token3, "validemail@gmail.com")
        user.user_profile_setemail(token3, "differentemail@gmail.com")
       
# TEST FUNCTIONS FOR USER_PROFILE_SETHANDLE
# Success for set handle
def test_user_profile_sethandle_success():
    """Tests for success when a user changes their handle."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]
    u_id = register_user1[1]
    user_info = user.user_profile(token, u_id) 
    user_handle = user_info["handle_str"]

    assert user_handle == "newuser"

    user.user_profile_sethandle(token, "newhandle")
    updated_user_info = user.user_profile(token, u_id) 
    updated_handle = updated_user_info["handle_str"]
    
    assert updated_handle = "newhandle"
# Failure for set handle
def test_user_profile_invalid_handle():
    """Tests for failure when a user inputs an invalid handle."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token = register_user1[0]

    with pytest.raises(InputError):
        user.user_profile_sethandle(token, "")
        user.user_profile_sethandle(token, "12")
        user.user_profile_sethandle(token, "abcdefghijklmnopqrstuvwxyz")
        user.user_profile_sethandle(token, "                          ")

def test_user_profile_email_already_in_use():
    """Tests for failure when a user inputs a handle that is already in use."""
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "New", "User")
    token1 = register_user1[0]
    register_user2 = auth.auth_register("differentemail@gmail.com", "321wordpass", "Different", "User")
    token2 = register_user2[0]
    register_user3 = auth.auth_register("randomperson@gmail.com", "987drowssap", "Random", "User")
    token3 = register_user3[0]

    with pytest.raises(InputError):
        user.user_profile_sethandle(token2, "newuser")
        user.user_profile_sethandle(token1, "differentuser")
        user.user_profile_sethandle(token3, "newuser)
        user.user_profile_sethandle(token3, "differentuser")