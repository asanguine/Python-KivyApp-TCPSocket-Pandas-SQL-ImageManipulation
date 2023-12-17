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
    except json.JSONDecodeError:
        preset_data = None

    conn.close()
    return {'user_id': user_id, 'preset_data': preset_data}

def handle(client):
    user_info = get_user_info_from_client(client)
    print(f"User {user_info['user_id']} joined. Character Preset: {user_info['preset_data']}")
    broadcast(json.dumps(user_info).encode('ascii'))
    
    with user_info_lock:
        user_info_list.append(user_info)
        friend.set_connected_users(user_info_list)

    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except Exception as e:
            print(f"Error handling client: {e}")
            break

    with user_info_lock:
        user_info_list.remove(user_info)
        friend.set_connected_users(user_info_list)
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


# if __name__ == '__main__':
#     # ... (other code)

#     friend.set_connected_users(user_info_list)
#     friend.print_users(user_info_list)
