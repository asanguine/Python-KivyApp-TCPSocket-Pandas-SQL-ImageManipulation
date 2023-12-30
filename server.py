import socket
import threading
import json
import friend

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
user_info_list = []
user_info_lock = threading.Lock()

def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            try:
                client.send(message)
                #print(f"\n() Broadcasting message to {client}a")
                print(f"\n Broadcasted message is: {message}   ()\n")
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                remove_client(client)

def remove_client(client):
    if client in clients:
        clients.remove(client)
        print("\n\n---- someone is gone ---")
        client.close()
        update_user_info_list()


def handle(client):
    try:
        user_id = client.recv(1024).decode('ascii')
        print(f"user joined: {user_id}")

        preset_data_str = client.recv(1024).decode('ascii')
        print(f"\n*********n\info of joined user:\n{preset_data_str}\n***********\n")
        try:
            preset_data = json.loads(preset_data_str)
            position = preset_data.get('position', {'x': 0, 'y': 0, 'size': 0.7})
        except json.JSONDecodeError:
            preset_data = None
            position = {'x': 0, 'y': 0, 'size': 0.7}

        user_info = {'user_id': user_id, 'preset_data': preset_data, 'position': position}

        print(f"\nReceived message from: {user_info['user_id']}\n")
        broadcast(json.dumps(user_info).encode('ascii'), exclude_client=client)

        with user_info_lock:
            user_info_list.append(user_info)
            friend.set_connected_users(user_info_list)
            print("\n\n---- someone has joined ---")
            print(len(friend.get_connected_users()))
            print("-------\n\n")

        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break
                received_data = json.loads(message)
                position = received_data.get('position', {'x': 0, 'y': 0, 'size': 0.7})
                friend.set_friend_picture_pos(position['x'], position['y'], position['size'])
                print(f"\n\nReceived data: {received_data}\n")#################
                print("\n\n---- connected users: ---")
                print(len(friend.get_connected_users()))
                print("-------\n\n")
                broadcast(message, exclude_client=client)

            except Exception as e:
                print(f"Error handling client: {e}")
                break

        disconnect_message = {'disconnect': True}
        broadcast(json.dumps(disconnect_message).encode('ascii'), exclude_client=client)


        with user_info_lock:
            user_info_list.remove(user_info)
            friend.set_connected_users(user_info_list)
            print("\n\n---- someone is gone ---")
            print(len(friend.get_connected_users()))
            print("-------\n\n")
        clients.remove(client)
        client.close()

    except Exception as e:
        print(f"Error handling client: {e}")


def update_user_info_list():
    with user_info_lock:
        friend.set_connected_users(user_info_list)


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
