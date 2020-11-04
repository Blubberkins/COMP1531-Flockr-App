import channels
import channel
import auth
import pytest
from error import InputError
from other import clear

#
# TEST FUNCTIONS FOR CHANNELS_LIST
#

# No channels are available
def test_channels_list_no_channels():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner")

    channels_list = channels.channels_list(login['token'])

    assert channels_list == {"channels" : []}

# Owner creates one public channel
def test_channels_list_create_one_public_channel():
    clear()

    login_owner = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one private channel
def test_channels_list_create_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", False)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public channel and one private channel
def test_channels_list_create_one_public_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)
    channels_list = channels.channels_list(login_owner['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

# Owner creates one public channel and user does not join that channel
def test_channels_list_not_join_one_public_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : []}

# Owner creates one public channel and user joins that channel
def test_channels_list_join_one_public_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_join(login_user['token'], channel_id['channel_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one private channel and user does not join that channel
def test_channels_list_not_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channels.channels_create(login_owner['token'], "channel 1", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : []}

# Owner creates one private channel and user joins that channel
def test_channels_list_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public and one private channel and user joins the public channel
def test_channels_list_join_one_public_not_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_join(login_user['token'], channel_id_1['channel_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}]}

# Owner creates one public and one private channel and user joins the private channel
def test_channels_list_not_join_one_public_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_invite(login_owner['token'], channel_id_2['channel_id'], login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

# Owner creates one public and one private channel and user joins both channels
def test_channels_list_join_one_public_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User")

    channel.channel_join(login_user['token'], channel_id_1['channel_id'])
    channel.channel_invite(login_owner['token'], channel_id_2['channel_id'], login_user['u_id'])

    channels_list = channels.channels_list(login_user['token'])

    assert channels_list == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

#
# TEST FUNCTIONS FOR CHANNELS_LISTALL
#

# No channels are available
def test_channels_listall_no_channels():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner") 

    channels_listall = channels.channels_list(login['token'])

    assert channels_listall == {"channels" : []}

# Owner creates one public channel and user does not join that channel
def test_channels_listall_not_join_one_public_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public channel and user joins that channel
def test_channels_listall_join_one_public_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_join(login_user['token'], channel_id['channel_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one private channel and user does not join that channel
def test_channels_listall_not_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one private channel and user joins that channel
def test_channels_listall_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id = channels.channels_create(login_owner['token'], "channel", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_invite(login_owner['token'], channel_id['channel_id'], login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id['channel_id'], "name" : "channel"}]}

# Owner creates one public and one private channel and user joins the public channel
def test_channels_listall_join_one_public_not_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_join(login_user['token'], channel_id_1['channel_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

# Owner creates one public and one private channel and user joins the private channel
def test_channels_listall_not_join_one_public_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User") 

    channel.channel_invite(login_owner['token'], channel_id_2['channel_id'], login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

# Owner creates one public and one private channel and user joins both channels
def test_channels_listall_join_one_public_join_one_private_channel():
    clear()

    login_owner = auth.auth_register("validemail1@gmail.com", "password123", "New", "Owner") 

    channel_id_1 = channels.channels_create(login_owner['token'], "channel 1", True)
    channel_id_2 = channels.channels_create(login_owner['token'], "channel 2", False)

    login_user = auth.auth_register("validemail2@gmail.com", "password123", "New", "User")

    channel.channel_join(login_user['token'], channel_id_1['channel_id'])
    channel.channel_invite(login_owner['token'], channel_id_2['channel_id'], login_user['u_id'])

    channels_listall = channels.channels_listall(login_user['token'])

    assert channels_listall == {"channels" : [{"channel_id" : channel_id_1['channel_id'], "name" : "channel 1"}, {"channel_id" : channel_id_2['channel_id'], "name" : "channel 2"}]}

#
# TEST FUNCTIONS FOR CHANNELS_CREATE
#

# Create one public channel successfully with channel name 20 characters long
def test_channels_create_public_success():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner")

    channel_id = channels.channels_create(login['token'], "abcdefghijklmnopqrst", True)
    channel_details = channel.channel_details(login['token'], channel_id['channel_id'])

    assert channel_details == {"name" : "abcdefghijklmnopqrst", 
    "owner_members" : [{"u_id" : login['u_id'], "name_first" : "New", "name_last" : "Owner"}],
    "all_members" : [{"u_id" : login['u_id'], "name_first" : "New", "name_last" : "Owner"}]}

# Create one public channel unsuccessfully with channel name > 20 characters long
def test_channels_create_public_unsuccess():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner")

    with pytest.raises(InputError):
        channels.channels_create(login['token'], "abcdefghijklmnopqrstu", True)
    
# Create one private channel successfully with channel name 20 characters long
def test_channels_create_private_success():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner")

    channel_id = channels.channels_create(login['token'], "abcdefghijklmnopqrst", False)
    channel_details = channel.channel_details(login['token'], channel_id['channel_id'])

    assert channel_details == {"name" : "abcdefghijklmnopqrst", 
    "owner_members" : [{"u_id" : login['u_id'], "name_first" : "New", "name_last" : "Owner"}],
    "all_members" : [{"u_id" : login['u_id'], "name_first" : "New", "name_last" : "Owner"}]}

# Create one private channel unsuccessfully with channel name > 20 characters long
def test_channels_create_private_unsuccess():
    clear()

    login = auth.auth_register("validemail@gmail.com", "password123", "New", "Owner")

    with pytest.raises(InputError):
        channels.channels_create(login['token'], "abcdefghijklmnopqrstu", False)