from model import create_connection, retrieve_user_id
import threading
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
    #print("get_connected_users() called...")
    return state_manager.get_connected_users()

def set_character_pos(x, y):
    #print("set_character_pos() called...")
    return state_manager.set_character_pos(x, y)

def get_character_pos():
    #print("get_character_pos() called...")
    return state_manager.get_character_pos()

def set_friend_picture_pos(x, y):
    return state_manager.set_friend_picture_pos(x, y)
    
def get_friend_picture_pos():
    return state_manager.get_friend_picture_pos()

def set_friend_preset(preset):
    return state_manager.set_friend_preset(preset)

def get_friend_preset():
    return state_manager.get_friend_preset()


def receive_friend_preset(received_preset):
    print(f"\n\n()()()\n receiving preset: {received_preset} \n ()()()\n\n")
    if 'preset_data' in received_preset:
        clothe = received_preset['preset_data']['clothe']
        hair = received_preset['preset_data']['hair']
        expression = received_preset['preset_data']['expression']
        position = received_preset['preset_data']['position']
    else:
        clothe = received_preset['clothe']
        hair = received_preset['hair']
        expression = received_preset['expression']
        position = received_preset['position']
    try:
        if user_id:
            set_friend_picture_pos(position['x'], position['y'])
            preset = {'clothe': clothe, 'hair': hair, 'expression': expression}
            set_friend_preset(preset)
            #return {'clothe': clothe, 'hair': hair, 'expression': expression}
        else:
            print("Invalid user_id in the friend.json file.")
    except:
        print('\n no friend found...')
        preset = {'clothe': 1, 'hair': 1, 'expression': 1}
        #return {'clothe': 1, 'hair': 1, 'expression': 1}
