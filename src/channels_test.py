import channels
import channel
import auth
import pytest
from error import InputError

#
# TEST FUNCTIONS FOR CHANNELS_LIST
#

# No channels are available
def test_channels_list_no_channels():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login = auth.auth_login("validemail@gmail.com", "password123")

    channels_list = channels.channels_list(login['token'])

    assert channels_list == []

# Owner creates one public channel
def test_channels_list_create_one_public_channel():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one private channel
def test_channels_list_create_one_private_channel():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", False)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one public channel and one private channel
def test_channels_list_create_one_public_one_private_channel():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == [{"channel_id" : channel_id_1, "name" : "channel 1"}, {"channel_id" : channel_id_2, "name" : "channel 2"}]

# Owner creates one public channel and user does not join that channel
def test_channels_list_not_join_one_public_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channels.channels_create(login_owner['token'], "channel", True)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == []

# Owner creates one public channel and user joins that channel
def test_channels_list_join_one_public_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id)

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one private channel and user does not join that channel
def test_channels_list_not_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channels.channels_create(login_owner['token'], "channel 1", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == []

# Owner creates one private channel and user joins that channel
def test_channels_list_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one public and one private channel and user joins the public channel
def test_channels_list_join_one_public_not_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id_1)

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == [{"channel_id" : channel_id_1, "name" : "channel 1"}]

# Owner creates one public and one private channel and user joins the private channel
def test_channels_list_not_join_one_public_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_invite(login_owner['token'], channel_id_2, login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == [{"channel_id" : channel_id_2, "name" : "channel 2"}]

# Owner creates one public and one private channel and user joins both channels
def test_channels_list_join_one_public_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User")
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id_1)
    channel.channel_invite(login_owner['token'], channel_id_2, login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == [{"channel_id" : channel_id_1, "name" : "channel 1"}, {"channel_id" : channel_id_2, "name" : "channel 2"}]

#
# TEST FUNCTIONS FOR CHANNELS_LISTALL
#

# No channels are available
def test_channels_listall_no_channels():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login = auth.auth_login("validemail@gmail.com", "password123")

    channels_listall = channels.channels_list(login['token'])

    assert channels_listall == []

# Owner creates one public channel and user does not join that channel
def test_channels_listall_not_join_one_public_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one public channel and user joins that channel
def test_channels_listall_join_one_public_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id)

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one private channel and user does not join that channel
def test_channels_listall_not_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channels.channels_create(login_owner['token'], "channel 1", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == []

# Owner creates one private channel and user joins that channel
def test_channels_listall_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_invite(login_owner['token'], channel_id, login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id, "name" : "channel"}]

# Owner creates one public and one private channel and user joins the public channel
def test_channels_listall_join_one_public_not_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id_1)

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id_1, "name" : "channel 1"}]

# Owner creates one public and one private channel and user joins the private channel
def test_channels_listall_not_join_one_public_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_invite(login_owner['token'], channel_id_2, login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id_1, "name" : "channel 1"}, {"channel_id" : channel_id_2, "name" : "channel 2"}]

# Owner creates one public and one private channel and user joins both channels
def test_channels_listall_join_one_public_join_one_private_channel():
    auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 
    login_owner = auth.auth_login("validemail1@gmail.com", "password123")

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    auth.auth_register("validemail2@gmail.com", "password123", "New", "User")
    login_user = auth.auth_login("validemail2@gmail.com", "password123")

    channel.channel_join(login_user['token'], channel_id_1)
    channel.channel_invite(login_owner['token'], channel_id_2, login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == [{"channel_id" : channel_id_1, "name" : "channel 1"}, {"channel_id" : channel_id_2, "name" : "channel 2"}]

#
# TEST FUNCTIONS FOR CHANNELS_CREATE
#

# Create one public channel successfully
def test_channels_list_public_success():
    auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 
    login = auth.auth_login("validemail@gmail.com", "password123")

    channel_id = channels.channels_create(login['token'], "channel", True)

