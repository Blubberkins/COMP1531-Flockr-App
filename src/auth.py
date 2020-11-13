from data import data
from error import InputError, AccessError
import re
import hashlib
import jwt
import random
import string
import smtplib
import threading
import time
import urllib.request
from PIL import Image

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

def decode_jwt(token):
    SECRET = "COMP1531"
    email = jwt.decode(token, SECRET, algorithm = 'HS256')
    return email[("email")]

def get_reset_code():
    # Creates a random string of letters and numbers to be used for resetting password
    chars = string.ascii_letters + string.digits
    result = ''.join(random.choice(chars) for char in range(8))
    return result

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
                user["token"] = encode_jwt(email)
                return {
                    "u_id": user["u_id"],
                    "token": user["token"],
                }
        raise InputError("Invalid email or password")    
               
def auth_logout(token):
    global data

    # Check if token matches a registered email
    for user in data["users"]: 
        if token != "invalid_token" and decode_jwt(token) == user["email"]:
            # Invalidate token and log the user out
            user["token"] = "invalid_token"
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

    # Set default profile picture
    img_url = "https://www.ballastpoint.com.au/wp-content/uploads/2017/11/White-Square.jpg"
    img_filename = f"{handle}.jpg"
    urllib.request.urlretrieve(img_url, f"src/static/{img_filename}")
    img = Image.open(f"src/static/{img_filename}")
    img.save(f"src/static/{img_filename}")
    
    # Create a dictionary for the users' details and add this to the list of users
    user = {}
    user["u_id"] = u_id
    user["email"] = email   
    user["name_first"] = name_first
    user["name_last"] = name_last 
    user["handle_str"] = handle
    user["password"] = hashlib.sha256(password.encode()).hexdigest()
    user["token"] = encode_jwt(email)
    user["profile_img_url"] = f"/imgurl/{img_filename}"
    
    if u_id == 1:
        user["permission_id"] = 1
    else:
        user["permission_id"] = 2
    data["users"].append(user)
    
    return {
        "u_id": u_id,
        "token": encode_jwt(email),
    }

def auth_passwordreset_request(email):
    global data
    # This code is influenced by "https://stackabuse.com/how-to-send-emails-with-gmail-using-python/"
    generatedcode = get_reset_code()
    message = "Your reset code is:\n" + generatedcode

    gmail_user = 'bigmanthebiggerman@gmail.com'
    gmail_password = 'python123!'

    sent_from = gmail_user
    to = [email]
    subject = "Reset password"
    body = message

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        for user in data["users"]: 
            if email == user["email"]:
                user["reset_code"] = generatedcode
    
    except:
        raise InputError("Unable to send reset code")
    return {}


def auth_passwordreset_reset(reset_code, new_password):
    global data

    if len(new_password) < 6:
        raise InputError("Invalid password")
    if len(reset_code) != 8:
        raise InputError("Reset code is not a valid reset code")
    # Assumes the caller of this function is the reset_code they enter in
    for user in data["users"]:
        if "reset_code" in user.keys():
            if reset_code == user["reset_code"]:
                user["password"] = new_password
                del user["reset_code"]
    return {}