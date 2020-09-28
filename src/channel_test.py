#test functions for channel_invite
def channel_invite_invalid_id():
    register_user = auth.auth_register("user@email.com", "password123", "Channel", "Test")
    login_user = auth.auth_login("user@email.com", "password123")
    channel_id = channels.channels_create(login_user[1], "channel", 0)
    invalid_channel_id += 100
    invalid_u_id = login_user[0] + 100

    with pytest.raise(InputError) as e:
        channel.channel_invite(login_user[1], channel_id, )
        channel.channel_invite(login_user[1], , login_user[0])
        channel.channel_invite(login_user[1], invalid_channel_id, login_user[0])
        channel.channel_invite(login_user[1], channel_id, invalid_u_id)
        channel.channel_invite(login_user[1], invalid_channel_id, invalid_u_id)

def channel_invite_invalid_token():
    register_user = auth.auth_register("user@email.com", "password123", "Channel", "Test")
    login_user = auth.auth_login("user@email.com", "password123")
    channel_id = channels.channels_create(login_user[1], "channel", 0)

    with pytest.raise(AccessError) as e:
        channel.channel_invite("", channel_id, login_user[0])
        channel.channel_invite("invalid_token", channel_id, login_user[0])

def channel_invite_success():
    register_user = auth.auth_register("user@email.com", "password123", "Channel", "Test")
    login_user = auth.auth_login("user@email.com", "password123")
    channel_id = channels.channels_create(login_user[1], "channel", 0)

    channel.channel_invite(login_user[1], channel_id, login_user[0])
