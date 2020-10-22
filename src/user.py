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
        AccessError: When the user's token is invalid.
    """

    global data

    if token == "invalid_token":
        raise AccessError("Invalid permissions")

    if data["users"] != []:
        for user in data["users"]:            
            if u_id == user["u_id"]:
                return {
                    "user": {
                        "u_id": user["u_id"],
                        "email": user["email"],
                        "name_first": user["name_first"],
                        "name_last": user["name_last"],
                        "handle_str": user["handle_str"],  
                    }
                }
        raise InputError("Invalid user_id")

def user_profile_setname(token, name_first, name_last):
    """Updates a user's first and last name.

    Args:
        token: A string which acts an authorisation hash.
        name_first: A string which is the user's new first name.
        name_last: A string which is the user's new last name.

    
    Raises:
        InputError: When name_first is not between 1 and 50 characters inclusively in length.
                    When name_last is not between 1 and 50 characters inclusively in length.
        AccessError: When the user's token is invalid.
    """

    global data 
    # Check if token is valid
    if token == "invalid_token":
        raise AccessError("Invalid permissions")

    # Check if first name is valid
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Invalid first name")

    # Check if last name is valid
    if len(name_last) < 1 or len(name_last) > 50:     
        raise InputError("Invalid last name")

    # If all checks valid, then set user's first and last name to passed in first and last names
    if data["users"] != []:
        for user in data["users"]:            
            if token == user["token"]:
                user["name_first"] = name_first
                user["name_last"] = name_last

    return {}

def user_profile_setemail(token, email):
    """Updates a user's email.

    Args:
        token: A string which acts an authorisation hash.
        email: A string which is the user's new email.

    Raises:
        InputError: When email entered is not a valid email.
                    When email address is already being used by another user.
        AccessError: When the user's token is invalid.
    """

    global data

    # Check if token called is valid
    if token == "invalid_token":
        raise AccessError("Invalid permissions")

    # Check if email is valid
    if not valid_email(email):
        raise InputError("Invalid email")

    # Check if email is already in use
    if data["users"] != []:
        for user in data["users"]:
            if email == user["email"]:
                raise InputError("Email is already in use")

    # If all checks valid, then set user's email to passed in email
    for user in data["users"]:
        if token == user["token"]:
            user["email"] = email

    return {}

def user_profile_sethandle(token, handle_str):
    """Updates a user's handle.

    Args:
        token: A string which acts an authorisation hash.
        handle_str: A string which is the user's new handle.

    Raises:
        InputError: When handle_str is not between 3 and 20 characters.
                    When handle is already used by another user.
        AccessError: When the user's token is invalid.
    """

    global data

    # Check if token called is valid
    if token == "invalid_token":
        raise AccessError("Invalid permissions")
    
    # Check if handle is valid
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Invalid handle")

    # Check if handle is already in use
    if data["users"] != []:
        for user in data["users"]:
            if handle_str == user["handle_str"]:
                raise InputError("Handle is already in use")

    # If all checks valid, then set user's handle to passed in handle_str
    for user in data["users"]:
        if token == user["token"]:
            user["handle_str"] = handle_str

    return {}
