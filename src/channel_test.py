#test functions for channel_invite
def channel_invite_invalid_id():
    with pytest.raise(InputError) as e:
        channel.channel_invite("valid_token", "valid_channel_id", "")
        channel.channel_invite("valid_token", "", "valid_u_id")
        channel.channel_invite("valid_token", "invalid_channel_id", "valid_u_id")
        channel.channel_invite("valid_token", "valid_channel_id", "invalid_u_id")
        channel.channel_invite("valid_token", "invalid_channel_id", "invalid_u_id")

def channel_invite_invalid_token():
    with pytest.raise(AccessError) as e:
        channel.channel_invite("", "valid_channel_id", "valid_u_id")
        channel.channel_invite("invalid_token", "valid_channel_id", "valid_u_id")s
