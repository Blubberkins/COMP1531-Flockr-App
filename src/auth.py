import data
from error import InputError

def auth_login(email, password):
    # Check if email and password are valid or associated with a registered account
    for i in len(data["users"]):
        if check(email) == False:
            raise InputError("Invalid email")
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
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
