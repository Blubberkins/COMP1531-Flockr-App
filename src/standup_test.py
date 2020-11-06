import time
import pytest
import channel
import channels
import auth
import standup
from other import clear
from error import InputError
from error import AccessError

#Test functions for standup_start
def test_standup_start_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    invalid_channel_id = -1

    with pytest.raises(InputError):
        standup.standup_start(login_owner['token'], invalid_channel_id, 10)

def test_standup_start_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError):
        standup.standup_start("", channel_id, 10)
        standup.standup_start(login_user['token'], channel_id["channel_id"], 10)

def test_standup_start_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    standup.standup_start(login_owner['token'], channel_id["channel_id"], 10)
    standup_info = standup.standup_active(login_owner['token'], channel_id["channel_id"])
    assert standup_info['is_active'] == True

#Test functions for standup_active
def test_standup_active_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    invalid_channel_id = -1

    with pytest.raises(InputError):
        standup.standup_active(login_owner['token'], invalid_channel_id)

def test_standup_active_invalid_token(): 
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError):
        standup.standup_active("", channel_id["channel_id"])
        standup.standup_active(login_user['token'], channel_id["channel_id"])

def test_standup_active_successful():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    standup_info = standup.standup_active(login_owner['token'], channel_id["channel_id"])
    assert standup_info['is_active'] == False
    assert standup_info['time_finish'] == None

    standup.standup_start(login_owner['token'], channel_id["channel_id"], 10)
    standup_info = standup.standup_active(login_owner['token'], channel_id["channel_id"])
    assert standup_info['is_active'] == True

#Test functions for standup_send
def test_standup_send_invalid_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    invalid_channel_id = -1

    with pytest.raises(InputError):
        standup.standup_active(login_owner['token'], invalid_channel_id, "sample message")

def test_standup_send_invalid_message():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    standup.standup_start(login_owner['token'], channel_id["channel_id"], 10)

    with pytest.raises(InputError):
        standup.standup_send(login_owner['token'], channel_id["channel_id"], "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce")

def test_standup_send_no_active_standup():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        standup.standup_send(login_owner['token'], channel_id["channel_id"], "sample message")

def test_standup_send_invalid_token():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    standup.standup_start(login_owner['token'], channel_id["channel_id"], 10)

    with pytest.raises(AccessError):
        standup.standup_send("", channel_id["channel_id"], "sample message")
        standup.standup_send(login_user['token'], channel_id["channel_id"], "sample message")

def test_standup_send_successful():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    standup.standup_start(login_owner['token'], channel_id["channel_id"], 10)

    standup.standup_send(login_owner['token'], channel_id["channel_id"], "sample message")
    standup.standup_send(login_owner['token'], channel_id["channel_id"], "example message")

    with pytest.raises(InputError):
        channel.channel_messages(login_owner['token'], channel_id['channel_id'], 0)

    time.sleep(10)

    channel_messages = channel.channel_messages(login_owner['token'], channel_id['channel_id'], 0)
    assert channel_messages['messages'][0]['message'] == 'sample message'
    assert channel_messages['messages'][1]['message'] == 'example message'
    