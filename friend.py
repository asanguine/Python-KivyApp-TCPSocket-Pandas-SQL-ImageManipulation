from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from img_combine import combine_images, body_parts, images_count
import time

DB_CONNECTION = create_connection()
user_id = retrieve_user_id(DB_CONNECTION)

from state_manager import StateManager

state_manager = StateManager()

def set_connected_users(users):
    state_manager.set_connected_users(users)

def get_connected_users():
    return state_manager.get_connected_users()






connected_users=[]
def set_connected_users(users):
    global connected_users
    connected_users = users

def print_users():
    global connected_users
    print("printing connected usres....")
    print(f"Connected users: {connected_users}")

#output  = {'user_id': 'b814c6e8-4615-496e-ae21-2ad1280ab6b1',
#           'preset_data': {'clothe': 3, 'hair': 3, 'expression': 1}}

def remove_yourself_from_list(users, _user_id):
    print("removing yourself from the list...")
    for user in users:
        print(f'user: {user}')
        if user['user_id']==_user_id:
            users.remove(user)

def get_friend_preset(users):
    print("getting friend preset...")
    #print_users(connected_users)
    try:
        friend_preset = users[0]['preset_data']
        print(f'friend preset: {friend_preset}')
        return friend_preset
    except:
        print('no friend found...')
        return {'clothe': 1, 'hair': 1, 'expression': 1}

def get_connected_users():
    print(f'connectec users: {connected_users}')
    return connected_users

# def get_friend_image_source():
#     print
#     source = combine_images(body_parts(get_friend_preset(connected_users)['clothe'],
#                                        get_friend_preset(connected_users)['hair'],
#                                        get_friend_preset(connected_users)['expression']))
#     return source