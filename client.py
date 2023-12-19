import socket
import threading
import json
from model import retrieve_user_id, retrieve_preset, create_connection
import friend

class MyClient:
    def __init__(self, state_manager):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_id = None
        self.preset_data = None
        self.state_manager = state_manager

    def connect_to_server(self):
        self.client.connect(('127.0.0.1', 55555))
        self.user_id = retrieve_user_id(create_connection())
        self.preset_data = retrieve_preset(create_connection(), self.user_id)

        self.client.send(self.user_id.encode('ascii'))
        preset_info = {'clothe': self.preset_data['clothe'], 'hair': self.preset_data['hair'], 'expression': self.preset_data['expression']}
        self.client.send(json.dumps(preset_info).encode('ascii'))

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.user_id.encode('ascii'))
                else:
                    received_preset = json.loads(message)
                    print(f"Received preset: {received_preset}")
                    print("one minute")
                    user_info = []
                    user_info.append(received_preset)
                    friend.set_connected_users(user_info)
                    print(f'lets see... {user_info}')
                    #friend.set_connected_users(self.state_manager.get_connected_users())
                    print(friend.get_connected_users())
            except:
                print("An error occurred!")
                self.client.close()
                break

    def start(self):
        self.connect_to_server()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
