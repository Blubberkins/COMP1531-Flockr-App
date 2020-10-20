from data import data
from error import InputError
from error import AccessError
import re

def valid_email(email):  
    # Pass the regular expression and the string into the search() method 
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):  
        return True   
    else:         
        return False

def user_profile(token, u_id):
    """Returns information about a valid user.

    Args:
        token: A string which acts an authorisation hash.
        u_id: A unique integer associated with a registered user's account.

    Returns:
        A dictionary containing information about a user, including there user_id, email, first name, last name and handle.
    
    Raises:
        InputError: When user with u_id is not a valid user.
    """

    user = {}
    user["u_id"] = u_id
    user["email"] = email   
    user["name_first"] = name_first
    user["name_last"] = name_last 
    user["handle_str"] = handle
  
    return {
        'user': {
        	'u_id': 1,
        	'email': 'cs1531@cse.unsw.edu.au',
        	'name_first': 'Hayden',
        	'name_last': 'Jacobs',
        	'handle_str': 'hjacobs',
        },
    }

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    global data
    # Check if token called is valid
    if token == "invalid_token":
        raise AccessError "Invalid permissions"

    # Check if email is valid
    if not valid_email(email):
        raise InputError("Invalid email")

    # Check if email is already in use
    if data["users"] != []:
        for user in data["users"]:
            if email == user["email"]
                raise InputError "Email is already in use"

    # If all checks valid, then set user's email to passed in email
    for user in data["users"]:
        if token == user["token"]:
            user["email"] == email

    return {}

def user_profile_sethandle(token, handle_str):
    global data
    # Check if token called is valid
    if token == "invalid_token":
        raise AccessError "Invalid permissions"
    
    # Check if handle is valid
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Invalid handle")

    # Check if handle is already in use
    if data["users"] != []:
        for user in data["users"]:
            if handle_str == user["handle_str"]
                raise InputError "Handle is already in use"

    # If all checks valid, then set user's handle to passed in handle_str
    for user in data["users"]:
        if token == user["token"]:
            user["handle_str"] == handle_str

    return {}