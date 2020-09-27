import auth
import pytest
from error import InputError

# Test functions for auth_login
def test_login_valid_email():
    result = auth.auth_login("registered@gmail.com", "Validpassword1!")
    # check u_id and token exist

def test_login_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_login("email", "Validpassword1!") 

def test_login_registered_email():
    auth.auth_register("registered@gmail.com", "Validpassword1!", "New", "User")
    assert auth.auth_login("registered@gmail.com", "Validpassword1!")

def test_login_unregistered_email():
    auth.auth_register("registered@gmail.com", "Validpassword1!", "New", "User")
    with pytest.raises(InputError) as e:
        auth.auth_login("unregistered@gmail.com", "Validpassword1!") 

def test_login_valid_password():

def test_login_invalid_password():

# Test functions for auth_logout
def test_logout_successful():
    result = auth.auth_login("registered@gmail.com", "Validpassword1!")
    # Need to check whether the active token has become inactive to successfully log out
    assert auth.auth_logout(result[1]) == True)

def test_logout_unsuccessful():
    # Need to check whether login was successful in first place
    result = auth.auth_login("email", "password")
    assert auth.auth_logout(result(1)) == False)
   
# Test functions for auth_register
def test_register():
