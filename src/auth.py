from data import data
from error import InputError
from error import AccessError
import re
import hashlib
import jwt

def valid_email(email):  
    # Pass the regular expression and the string into the search() method 
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if re.search(regex, email):  
        return True   
    else:         
        return False

def encode_jwt(email):
    SECRET = "COMP1531"
    non_encoded_token = {'email' : email}
    token = jwt.encode(non_encoded_token, SECRET, algorithm ='HS256').decode('utf-8')
    return token
#print(encode_jwt("hi"))

def decode_jwt(token):
    SECRET = "COMP1531"
    email = jwt.decode(token, SECRET, algorithm = 'HS256')
    return email[("email")]

def auth_login(email, password):
    global data

    # Check if email is valid
    if not valid_email(email):
        raise InputError("Invalid email")
    
    # Check if email and password are associated with a registered account
    password = hashlib.sha256(password.encode()).hexdigest()

    if data["users"] != []:
        for user in data["users"]:            
            if email == user["email"] and password == user["password"]:
                return {
                    "u_id": user["u_id"],
                    "token": encode_jwt(email),
                }
        raise InputError("Invalid email or password")    
               
def auth_logout(token):
    global data

    # Check if token matches a registered email
    for user in data["users"]: 
        if token != "invalid_token" and decode_jwt(token) == user["email"]:
            # Invalidate token and log the user out
            token = "invalid_token"
            return {
                "is_success": True,
            }

    # If token does not match a registered email, return false
    return {
        "is_success": False,
    }

def auth_register(email, password, name_first, name_last):
    global data
    
    u_id = len(data["users"]) + 1
            
    # Check if email is valid
    if not valid_email(email):
        raise InputError("Invalid email")
    
    # Check if email is already in use
    if data["users"] != []:
        for user in data["users"]:
            if email == user["email"]:
                raise InputError("Email is already in use")        
 
    # Check if password is valid
    if len(password) < 6:
        raise InputError("Invalid password")
            
    # Check if first name is valid
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("Invalid first name")

    # Check if last name is valid
    if len(name_last) < 1 or len(name_last) > 50:     
        raise InputError("Invalid last name")

    # Create handle
    handle = (name_first + name_last)[:20].lower()
    
    # Check if handles are the same
    for user in data["users"]: 
        duplicate_count = 2

        # If same handle exists
        if handle == user["handle_str"]:
            is_duplicate = True

            # While the new created handle is still true, i.e. user2 and user2
            while is_duplicate:
                # Attach a number to the end of handle
                handle = handle[:19] + str(duplicate_count)
                duplicate_count += 1
                # If new handle is unique, i.e. user2 and user3
                if handle != user["handle_str"]:
                    is_duplicate = False

    # Create a dictionary for the users' details and add this to the list of users
    user = {}
    user["u_id"] = u_id
    user["email"] = email   
    user["name_first"] = name_first
    user["name_last"] = name_last 
    user["handle_str"] = handle
    user["password"] = hashlib.sha256(password.encode()).hexdigest()
    user["token"] = encode_jwt(email)
    if u_id == 1:
        user["permission_id"] = 1
    else:
        user["permission_id"] = 2
    data["users"].append(user)
    
    return {
        "u_id": u_id,
        "token": encode_jwt(email),
    }
