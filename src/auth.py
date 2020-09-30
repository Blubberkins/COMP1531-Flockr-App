import data
from error import InputError
from error import AccessError

def auth_login(email, password):
    # Check if email is valid
    if check(email) == False:
        raise InputError("Invalid email")
    
    # Check if email and password are associated with a registered account
    for i in len(data["users"]): 
        elif email != data["users"][i]["email"]:
            raise InputError("No account found")   
        elif password != data["users"][i]["password"]:
            raise InputError("Incorrect password")
        elif email != data["users"][i]["email"] and password == data["users"][i]["password"]:
            return {
                "u_id": data["users"][i]["u_id"],
                "token": email,
            }

def auth_logout(token):
    # Check if token matches a registered email
    for i in len(data["users"]):
        if token != data["users"][i]["email"]:
            raise AccessError("Invalid token")
            return {
                "is_success": False,
            }

    # Using check email function to check whether function is email, based on assumption that token is user email
    if check(token) == False:
        raise AccessError("Invalid token")
        return {
            "is_success": False,
        }
    else:
        # Invalidate token and log the user out
        token = "invalid"
        return {
            "is_success": True,
        }

def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
