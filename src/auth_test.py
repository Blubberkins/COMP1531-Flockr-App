import auth
import pytest
from error import InputError

# Test functions for auth_login
def test_login_successful():
    register = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    login = auth.auth_login("validemail@gmail.com", "python123")
    assert register["u_id"] == login["u_id"]
    assert register["token"] == login["token"]

def test_login_unsuccessful():
    auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    with pytest.raises(InputError) as e:
        auth.auth_login("", "") 
        auth.auth_login("validemail", "") 
        auth.auth_login("validemail@gmail.com", "") 
        auth.auth_login("", "123") 
        auth.auth_login("", "python123") 
        auth.auth_login("unregistered@gmail.com", "haha") 
       
# def test_login_valid_email(): 

def test_login_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_login("", "python123") 
        auth.auth_login("email", "python123") 
        auth.auth_login("email.com", "python123") 

def test_login_registered_email():
    register = auth.auth_register("registered@gmail.com", "python123", "New", "User")
    login = auth.auth_login("registered@gmail.com", "python123")
    assert register["u_id"] == login["u_id"]
    assert register["token"] == login["token"]

def test_login_unregistered_email():
    auth.auth_register("registered@gmail.com", "Validpassword1!", "New", "User")
    with pytest.raises(InputError) as e:
        auth.auth_login("", "Validpassword1!") 
        auth.auth_login("unregistered@gmail.com", "Validpassword1!") 

# def test_login_valid_password():
    
def test_login_invalid_password():
    with pytest.raises(InputError) as e:
        auth.auth_login("registered@gmail.com", "") 
        auth.auth_login("registered@gmai.com", "123") 

# Test functions for auth_logout
def test_logout_successful():
    auth.auth_register("registered@gmail.com", "Validpassword1!", "New", "User")
    login = auth.auth_login("registered@gmail.com", "Validpassword1!")
    token = login["token"]
    result = auth.auth_logout(token)
    assert result["is_success"] == True

# def test_logout_unsuccessful():
   
# Test functions for auth_register
# Success for register
def test_register_success():
    auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
    auth.auth_register("validemail@gmail.com", "           ", "Firstname", "Lastname")
    auth.auth_register("validemail@ourearth.org", "password123", "Firstname", "Lastname")
    auth.auth_register("validemail@gmail.com", "password123", "123456789", "Lastname")
    auth.auth_register("validemail@gmail.com", "password123", "123456789", "@#$%^&(*")

# Failure for register

def test_register_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_register("invalidemail.com", "password123", "Firstname", "Lastname")
        auth.auth_register("@@@@@@@@@@@@@@@@", "password123", "Firstname", "Lastname")
        auth.auth_register("invalid@email", "password123", "Firstname", "Lastname")

def test_register_already_used_email():
    auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
        auth.auth_register("validemail@gmail.com", "differentpassword123", "NewFirstname", "NewLastname")
        
def test_register_invalid_password():
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "pass", "Firstname", "Lastname")
    with pytest.raises(InputError) as e:    
        auth.auth_register("validemail@gmail.com", "", "Firstname", "Lastname")
    with pytest.raises(InputError) as e:    
        auth.auth_register("validemail@gmail.com", "123@b", "Firstname", "Lastname")

def test_register_invalid_first_name():
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "", "Lastname")
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "Lastname")

def test_register_invalid_last_name():
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "")

    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")



