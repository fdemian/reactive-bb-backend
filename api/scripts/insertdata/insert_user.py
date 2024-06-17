from api.scripts.add_user import do_save_user

# TEST DATA
user = {
    "username": "user",
    "password": "password",
    "email": "user@email.com",
    "name": "name",
    "avatar": None,
    "failed_attempts": 0,
    "lockout_time": None,
    "type": "U",
    "status": "",
    "about": "",
    "banned": False,
    "banReason": None,
}

user2 = {
    "username": "user2",
    "password": "password",
    "email": "user2@email.com",
    "name": "name 2",
    "avatar": None,
    "failed_attempts": 0,
    "lockout_time": None,
    "type": "U",
    "status": "",
    "about": "",
    "banned": False,
    "banReason": None,
}

banned_user = {
    "username": "banned",
    "password": "bannedpass",
    "email": "banned@email.com",
    "name": "name 2",
    "avatar": None,
    "failed_attempts": 0,
    "lockout_time": None,
    "type": "U",
    "status": "",
    "about": "",
    "banned": True,
    "banReason": '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"",'
                 '"text":"BAN_REASON","type":"text","version":1}],"direction":"ltr","format":"","indent":0,'
                 '"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root",'
                 '"version":1}}',
}

mod_user = {
    "username": "mod",
    "password": "modpass",
    "email": "mod@email.com",
    "name": "Mod Erator",
    "avatar": None,
    "failed_attempts": 0,
    "lockout_time": None,
    "type": "M",
    "status": "",
    "about": "",
    "banned": False,
    "banReason": None,
}

admin_user = {
    "username": "admin",
    "password": "admin",
    "email": "admin@email.com",
    "name": "Mod Erator",
    "avatar": None,
    "failed_attempts": 0,
    "lockout_time": None,
    "type": "A",
    "status": "",
    "about": "",
    "banned": False,
    "banReason": None,
}


def insert_test_user(session, user_to_insert):
    user_to_insert = do_save_user(user_to_insert, session, is_valid=True)
    return user_to_insert.id
