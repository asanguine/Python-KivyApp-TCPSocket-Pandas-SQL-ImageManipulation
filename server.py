# server.py
import socket
import threading
import json
from model import retrieve_user_id, retrieve_preset, create_connection

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

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

    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except Exception as e:
            print(f"Error handling client: {e}")
            break

    clients.remove(client)
    client.close()


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
