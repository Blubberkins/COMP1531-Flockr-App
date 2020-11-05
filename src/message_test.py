import message
import channel
import channels
import auth
import pytest
from error import AccessError, InputError
from other import clear


# Tests for message_send
def test_message_send_input_error():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    non_existent_channel_id = -1
    
    with pytest.raises(InputError):
        message.message_send(login_owner["token"], channel_id["channel_id"], "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce")
        message.message_send(login_owner["token"], channel_id["channel_id"], "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores e")
        message.message_send(login_owner["token"], channel_id["channel_id"], "Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie, musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li grammatica, li pronunciation e li plu commun vocabules. Omnicos directe al desirabilite de un nov lingua franca: On refusa continuar payar custosi traductores. At solmen va esser necessi far uniform grammatica, pronunciation e plu sommun paroles. Ma quande lingues coalesce, li grammatica del resultant lingue es plu simplic e regulari quam ti del coalescent lingues. Li nov lingua franca va esser plu simplic e regulari quam li existent Europan lingues. It va esser tam simplic quam Occidental in fact, it va esser Occidental. A un Angleso it va semblar un simplificat Angles, quam un skeptic Cambridge amico dit me que Occidental es. Li Europan lingues es membres del sam familie. Lor separat existentie es un myth. Por scientie, musica, sport etc, litot Europa usa li sam vocabular. Li lingues differe solmen in li g")
        message.message_send(login_owner["token"], non_existent_channel_id, "sample message")

def test_message_send_access_error():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    with pytest.raises(AccessError):
        message.message_send(login_user["token"], channel_id["channel_id"], "sample message")

def test_message_send_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_join(login_user["token"], channel_id["channel_id"])

    assert message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") == {"message_id": 0}
    assert message.message_send(login_user["token"], channel_id["channel_id"], "sample message") == {"message_id": 1}
    assert message.message_send(login_owner["token"], channel_id["channel_id"], "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores.") == {"message_id": 2}
    assert message.message_send(login_user["token"], channel_id["channel_id"], "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores.") == {"message_id": 3}

# Tests for message_remove
def test_message_remove_no_messages():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        message.message_remove(login_owner['token'], 1)

def test_message_remove_removed_message():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message")
    message.message_remove(login_owner["token"], 0)

    with pytest.raises(InputError):
        message.message_remove(login_owner["token"], 0)

def test_message_remove_not_message_sender():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_join(login_user["token"], channel_id["channel_id"])

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message")

    with pytest.raises(AccessError):
        message.message_remove(login_user, 0)

def test_message_admin_remove_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_join(login_user["token"], channel_id["channel_id"])

    message.message_send(login_user["token"], channel_id["channel_id"], "sample message")

    assert message.message_remove(login_owner["token"], 0) == {}

# Tests for message_edit
def test_message_edit_1000_characters():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message")

    with pytest.raises(InputError):
        message.message_edit(login_owner["token"], 0, "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce")
        message.message_edit(login_owner["token"], 0, "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur? At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores e")

def test_message_edit_not_message_sender():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_join(login_user["token"], channel_id["channel_id"])

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message")

    with pytest.raises(AccessError):
        message.message_edit(login_user["token"], 0, "edited message")

def test_message_owner_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")
    channel.channel_join(login_user["token"], channel_id["channel_id"])

    message.message_send(login_user["token"], channel_id["channel_id"], "sample message") 

    assert message.message_edit(login_owner["token"], 0, "edited message") == {}

def test_message_edit_empty_edit():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    assert message.message_edit(login_owner["token"], 0, "") == {}
    
# Tests for message/react

def test_message_react_message_does_not_exist():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, 1)

def test_message_react_removed_message():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_remove(login_owner["token"], 0)

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, 1)

def test_message_react_message_in_private_channel():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", False)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_react(login_user["token"], 0, 1)

def test_message_react_react_id_0():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, 0)

def test_message_react_negative_react_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, -1)
        message.message_react(login_owner["token"], 0, -100)
        message.message_react(login_owner["token"], 0, -100000)

def test_message_react_invalid_positive_react_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, 2)
        message.message_react(login_owner["token"], 0, 100)
        message.message_react(login_owner["token"], 0, 100000)

def test_message_react_already_reacted():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_react(login_owner["token"], 0, 1)

    with pytest.raises(InputError):
        message.message_react(login_owner["token"], 0, 1)

def test_message_react_blackbox_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    assert message.message_react(login_owner["token"], 0, 1) == {}

def test_message_react_whitebox_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_react(login_owner["token"], 0, 1)
    message_data = channel.channel_messages(login_owner["token"], channel_id["channel_id"], 0)
    assert message_data["messages"][0]["reacts"]["react_id"] == 1
    assert message_data["messages"][0]["reacts"]["u_ids"] == [login_owner["u_id"]]
    assert message_data["messages"][0]["reacts"]["is_this_user_reacted"] == True

# Tests for message_unreact

def test_message_unreact_message_does_not_exist():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, 1)

def test_message_unreact_removed_message():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_remove(login_owner["token"], 0)

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, 1)

def test_message_unreact_message_in_private_channel():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", False)
    login_user = auth.auth_register("user@email.com", "password123", "User", "Test")

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_unreact(login_user["token"], 0, 1)

def test_message_unreact_react_id_0():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, 0)

def test_message_unreact_negative_react_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, -1)
        message.message_unreact(login_owner["token"], 0, -100)
        message.message_unreact(login_owner["token"], 0, -100000)

def test_message_unreact_invalid_positive_react_id():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, 2)
        message.message_unreact(login_owner["token"], 0, 100)
        message.message_unreact(login_owner["token"], 0, 100000)

def test_message_unreact_message_has_no_reacts():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message")

    with pytest.raises(InputError):
        message.message_unreact(login_owner["token"], 0, 1)

def test_message_unreact_blackbox_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_react(login_owner["token"], 0, 1)
    assert message.message_unreact(login_owner["token"], 0, 1) == {}

def test_message_unreact_whitebox_success():
    clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    channel_id = channels.channels_create(login_owner['token'], "channel", True)

    message.message_send(login_owner["token"], channel_id["channel_id"], "sample message") 
    message.message_react(login_owner["token"], 0, 1)
    message.message_unreact(login_owner["token"], 0, 1)
    message_data = channel.channel_messages(login_owner["token"], channel_id["channel_id"], 0)
    assert message_data["messages"][0]["reacts"]["react_id"] == 1
    assert message_data["messages"][0]["reacts"]["u_ids"] == []
    assert message_data["messages"][0]["reacts"]["is_this_user_reacted"] == False
