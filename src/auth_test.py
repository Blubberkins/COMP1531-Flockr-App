import auth
import pytest
from error import InputError
from other import clear

# TEST FUNCTIONS FOR AUTH_LOGIN
# Success for login
def test_login_success():
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    auth.auth_logout(register_user1["token"])
    login_user1 = auth.auth_login("validemail@gmail.com", "python123")
    assert register_user1["u_id"] == login_user1["u_id"]
    assert register_user1["token"] == login_user1["token"]

    register_user2 = auth.auth_register("registered@gmail.com", "helloworld123", "New", "Account")
    auth.auth_logout(register_user2["token"]) 
    login_user2 = auth.auth_login("registered@gmail.com", "helloworld123")
    assert register_user2["u_id"] == login_user2["u_id"]
    assert register_user2["token"] == login_user2["token"]

    register_user3 = auth.auth_register("pythonrules@gmail.com", "bigpython123", "New", "Person")
    auth.auth_logout(register_user3["token"]) 
    login_user3 = auth.auth_login("pythonrules@gmail.com", "bigpython123")
    assert register_user3["u_id"] == login_user3["u_id"]
    assert register_user3["token"] == login_user3["token"]

# Failure for login
def test_login_empty():
    clear()
    register_user = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    auth.auth_logout(register_user["token"])
    with pytest.raises(InputError) as e:
        auth.auth_login("", "") 

def test_login_invalid_email():
    clear()
    register_user = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    auth.auth_logout(register_user["token"])
    with pytest.raises(InputError) as e:
        auth.auth_login("", "python123") 
        auth.auth_login("     ", "python123") 
        auth.auth_login("email", "python123") 
        auth.auth_login("email.com", "python123") 
        auth.auth_login("@@@@@@@@@", "python123") 

def test_login_unregistered_email():
    clear()
    register_user = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    auth.auth_logout(register_user["token"])
    with pytest.raises(InputError) as e:
        auth.auth_login("email@gmail.com", "python123") 
        auth.auth_login("ilikepython@helloworld.com", "python123") 
        auth.auth_login("programming@computer.com", "python123") 
        auth.auth_login("unregistered@gmail.com", "python123") 
        auth.auth_login("helloworld@web.com", "python123")        
    
def test_login_invalid_password():
    clear()
    register_user = auth.auth_register("validemail@gmail.com", "python123", "New", "User") 
    auth.auth_logout(register_user["token"])
    with pytest.raises(InputError) as e:
        auth.auth_login("validemail@gmail.com", "") 
        auth.auth_login("validemail@gmail.com", " ")
        auth.auth_login("validemail@gmail.com", "123")  
        auth.auth_login("validemail@gmail.com", "pass")       
        auth.auth_login("validemail@gmali.com", "!!!!!") 

# TEST FUNCTIONS FOR AUTH_LOGOUT
# Success for logout
def test_logout_success():
    clear()
    register_user = auth.auth_register("registered@gmail.com", "python123", "New", "User")
    
    assert auth.auth_logout(register_user["token"])["is_success"] == True

'''
# Failure for logout - UNSURE OF THIS, MAY BE REMOVED FOR FINAL SUBMISSION
def test_logout_failure():
    clear()
    auth.auth_register("registered@gmail.com", "python123", "New", "User")
    result = auth.auth_logout("invalid_token")
    assert result["is_success"] == False
'''        
# TEST FUNCTIONS FOR AUTH_REGISTER
# Success for register
def test_register_success():
    clear()
    register_user1 = auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
    assert register_user1["token"] == "validemail@gmail.com"
    register_user2 = auth.auth_register("validemail2@gmail.com", "           ", "Firstname", "Lastname")
    assert register_user2["token"] == "validemail2@gmail.com"
    register_user3 = auth.auth_register("validemail3@ourearth.org", "password123", "Firstname", "Lastname")
    assert register_user3["token"] == "validemail3@ourearth.org"

# Failure for register
def test_register_invalid_email():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("invalidemail.com", "password123", "Firstname", "Lastname")
        auth.auth_register("@@@@@@@@@@@@@@@@", "password123", "Firstname", "Lastname")
        auth.auth_register("invalid@email", "password123", "Firstname", "Lastname")

def test_register_already_used_email():
    clear()
    auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "Lastname")
        auth.auth_register("validemail@gmail.com", "differentpassword123", "NewFirstname", "NewLastname")
        
def test_register_invalid_password():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "pass", "Firstname", "Lastname")
        auth.auth_register("validemail@gmail.com", "", "Firstname", "Lastname")   
        auth.auth_register("validemail@gmail.com", "123@b", "Firstname", "Lastname")

def test_register_invalid_first_name():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "", "Lastname")
        auth.auth_register("validemail@gmail.com", "password123", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "Lastname")

def test_register_invalid_last_name():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "")
        auth.auth_register("validemail@gmail.com", "password123", "Firstname", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz")
