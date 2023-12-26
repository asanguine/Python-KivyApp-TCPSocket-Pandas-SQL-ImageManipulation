import socket
import threading
import json
from model import create_connection
import friend

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
user_info_list = []
user_info_lock = threading.Lock()

def broadcast(message):
    for client in clients:
        client.send(message)


def get_user_info_from_client(client):
    user_id = client.recv(1024).decode('ascii')
    print(f"Received user ID: {user_id}")

    existing_conn = create_connection()
    if existing_conn:
        existing_conn.close()

    conn = create_connection()
    preset_data_str = client.recv(1024).decode('ascii')
    try:
        preset_data = json.loads(preset_data_str)
        position = preset_data.get('position', {'x': 0, 'y': 0})
    except json.JSONDecodeError:
        preset_data = None
        position = {'x': 0, 'y': 0}

    conn.close()
    return {'user_id': user_id, 'preset_data': preset_data, 'position': position}


def handle(client):
    user_info = get_user_info_from_client(client)
    print(f"User {user_info['user_id']} joined. Character Preset: {user_info['preset_data']}")
    broadcast(json.dumps(user_info).encode('ascii'))
    
    with user_info_lock:
        user_info_list.append(user_info)
        friend.set_connected_users(user_info_list)
        print(friend.get_connected_users())

    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            received_data = json.loads(message)
            position = received_data.get('position', {'x': 0, 'y': 0})
            friend.set_friend_picture_pos(position['x'], position['y'])
            #received_data['position'] = friend.get_friend_picture_pos()
            broadcast(message)
            #broadcast(json.dumps(received_data).encode('ascii'))

        except Exception as e:
            print(f"Error handling client: {e}")
            break

    with user_info_lock:
        user_info_list.remove(user_info)
        friend.set_connected_users(user_info_list)
        print(friend.get_connected_users())
    clients.remove(client)
    client.close()

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def get_user_info_list():
    with user_info_lock:
        return user_info_list

receive()
