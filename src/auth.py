import data
from error import InputError
from error import AccessError
import re

def check(email):  
# Pass the regular expression and the string into the search() method 
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if (re.search(regex,email)):  
        return True   
    else:         
        return False

# data.data["accounts"][email] = password
def auth_login(email, password):
    # Check if email is valid
    if check(email) == False:
        raise InputError("Invalid email")
    
    # Check if email and password are associated with a registered account
    for i in len(data.data["accounts"]): 
        if email != data.data["accounts"]["email"]:
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
    
    

    u_id = len(data["users"]) + 1
            
   #need check all valid 

    if check(email) == False:
        
        raise InputError("Invalid email")

    for i in len(data["users"]):
        if email == data["users"][i]["email"]:
            raise InputError("Email is already in use")
          

    #EMAIL IS VALID CHECK PASSWORD

    if len(password) < 6:

        raise InputError("Invalid password")
            
    
    
    #PASSWORD IS VALID CHECK FIRST_NAME

    if len(name_first) < 1 or len(name_first) > 50:

        raise InputError("Invalid first name")

    #FIRST NAME IS VALID CHECK LAST NAME

    if len(name_last) < 1 or len(name_last) > 50:  
        
        raise InputError("Invalid last name")


    #Creating handle

    handle = name_first + name_last
    handle = handle[:20].lower()
    
    
    #For if handles are the same
    for i in len(data["users"]):
        duplicate_count = 2

        #If same handle exists
        if handle == data["users"][i]["handle_str"]:
            is_duplicate = True

            #While the new created handle is still true ie user2 and user2
            while is_duplicate == True:
                #attach a number to the end of handle
                handle = handle[:19] + str(duplicate_count)
                duplicate_count += 1
                #if new handle is unique ie. user2 and user3
                if handle != data["users"][i]["handle_str"]:
                    is_duplicate = False

    data.data["users"][u_id - 1]["u_id"] = u_id
    data.data["users"][u_id - 1]["email"] = email   
    data.data["users"][u_id - 1]["name_first"] = name_first
    data.data["users"][u_id - 1]["name_last"] = name_last 
    data.data["users"][u_id - 1]["handle_str"] = handle

    data.data["accounts"][u_id - 1]["email"] = email
    data.data["accounts"][u_id - 1]["password"] = password

    return {
        'u_id': u_id,
        'token': email,
    }
