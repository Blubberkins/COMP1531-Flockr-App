import data # need to create a file which has a global variable that can be modified from any of the project files

def auth_login(email, password):
    for i in len(data["users"]):
        if email == data["users"][i]["email"] and password == data["users"][i]["password"]:
            return {
                'u_id': 1,
                'token': email,
            }

        else:

]
def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
