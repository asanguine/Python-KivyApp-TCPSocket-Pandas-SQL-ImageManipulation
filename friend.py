#from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from img_combine import combine_images, body_parts, images_count

# DB_CONNECTION = create_connection()
# user_id = retrieve_user_id(DB_CONNECTION)

from state_manager import StateManager

connected_users = []

state_manager = StateManager()

def set_connected_users(users):
    state_manager.set_connected_users(users)


def get_connected_users():
    print("get_connected_users() called...")
    return state_manager.get_connected_users()


def remove_yourself_from_list(users, _user_id):
    print("\nremove_yourself_from_list() called...")
    for user in users:
        print(f'user: {user}')
        if user['user_id']==_user_id:
            users.remove(user)

import threading
user_info_lock = threading.Lock()

def get_friend_preset():
    print("\nget_friend_preset() called ...")
    with user_info_lock:
        users =  get_connected_users()

    print(f'users: {users}')
    try:

        friend_preset = users[0]['preset_data']
        print(f'\ntry: friend preset: {friend_preset}')
        return friend_preset
    except:
        print('\n no friend found...')
        return {'clothe': 1, 'hair': 1, 'expression': 1}
