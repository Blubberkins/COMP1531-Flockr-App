import auth
import other
import pytest
from error import InputError
from error import AccessError

#test functions for users_all
def test_users_all_invalid_token():
    other.clear()
    with pytest.raises(AccessError):
        other.users_all("invalid_token")
        other.users_all("")

def test_users_all_successful():
    other.clear()
    first_user = auth.auth_register("user1@email.com", "password123", "First", "User")
    assert other.users_all(first_user['token']) == [{'u_id' : first_user['u_id'], 'email' : "user1@email.com", 'name_first' : "First", 'name_last' : "User", 'handle_str' : "firstuser"}]

    second_user = auth.auth_register("user2@email.com", "password321", "Second", "User")
    assert other.users_all(second_user['token']) == [{'u_id' : first_user['u_id'], 'email' : "user1@email.com", 'name_first' : "First", 'name_last' : "User", 'handle_str' : "firstuser"},
                                                    {'u_id' : second_user['u_id'], 'email' : "user2@email.com", 'name_first' : "Second", 'name_last' : "User", 'handle_str' : "seconduser"}]

#test functions for admin_userpermission_change
def test_admin_userpermission_change_invalid_id():
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")
    invalid_u_id = -1
    invalid_permission_id = -1

    with pytest.raises(InputError):
        other.admin_userpermission_change(login_owner['token'], invalid_u_id, 1)
        other.admin_userpermission_change(login_owner['token'], login_user['u_id'], invalid_permission_id)
        other.admin_userpermission_change(login_owner['token'], invalid_u_id, invalid_permission_id)

def test_admin_userpermission_change_invalid_token():
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    with pytest.raises(AccessError):
        other.admin_userpermission_change("", login_user['u_id'], 1)
        other.admin_userpermission_change(login_user['token'], login_owner['u_id'], 2)

def test_admin_userpermission_change_success():
    other.clear()
    login_owner = auth.auth_register("owner@email.com", "password123", "Owner", "Test")
    login_user = auth.auth_register("user@email.com", "password321", "User", "Test")

    other.admin_userpermission_change(login_owner['token'], login_user['u_id'], 1)
    other.admin_userpermission_change(login_user['token'], login_owner['u_id'], 2)

    with pytest.raises(AccessError):
        other.admin_userpermission_change(login_owner['token'], login_user['u_id'], 2)
