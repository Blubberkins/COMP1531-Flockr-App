from error import InputError
from error import AccessError

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
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }