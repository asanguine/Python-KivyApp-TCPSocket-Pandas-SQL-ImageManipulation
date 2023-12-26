from model import create_connection, update_preset, retrieve_user_id, retrieve_preset, generate_user_id, create_presets_table
from img_combine import combine_images, body_parts, images_count
import json, threading
from state_manager import StateManager

DB_CONNECTION = create_connection()
user_id = retrieve_user_id(DB_CONNECTION)
user_info_lock = threading.Lock()
file_path='friend.json'

connected_users = []

state_manager = StateManager()

def set_connected_users(users):
    state_manager.set_connected_users(users)

def get_connected_users():
    print("get_connected_users() called...")
    return state_manager.get_connected_users()

def set_character_pos(x, y):
    print("set_character_pos() called...")
    return state_manager.set_character_pos(x, y)

def get_character_pos():
    print("get_character_pos() called...")
    return state_manager.get_character_pos()

def set_friend_picture_pos(x, y):
    return state_manager.set_friend_picture_pos(x, y)
    
def get_friend_picture_pos():
    return state_manager.get_friend_picture_pos()

#################


def get_friend_preset():
    print("\nget_friend_preset() called ...")
    try:
        with open(file_path, 'r') as friend_file:
            data = json.load(friend_file)
            user_id = data.get('user_id', '')
            clothe = data.get('clothe', 1)
            hair = data.get('hair', 1)
            expression = data.get('expression', 1)

            if user_id:
                return {'clothe': clothe, 'hair': hair, 'expression': expression}
            else:
                print("Invalid user_id in the friend.json file.")
    except:
        print('\n no friend found...')
        return {'clothe': 1, 'hair': 1, 'expression': 1}
