# COMP1531 Major Project Assumptions

## Auth
* The u_id returned from auth_register and auth_login should match when logging in with the same details which have just been registered with.
* Space bars are considered characters for password length.
* First and last name contain no spaces may contain symbols such as !@#$%^&*(
* Registering will login the user.

## Channel
* The channel_details function returns a dictionary
* Users will be able to see public channels, and can join them (channel_join)
* Users invited to a channel do not need to join them after

## Channels
* The name of a new channel can include space bars (considered as characters) and symbols.
* The names of new channels can be the same as existing channels.