import socket
import threading
import json, time, os
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

        while True:
            preset_info = {'user_id': self.user_id,
                           'clothe': self.preset_data['clothe'],
                           'hair': self.preset_data['hair'],
                           'expression': self.preset_data['expression']}
            self.client.send(json.dumps(preset_info).encode('ascii'))
            time.sleep(3)

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.user_id.encode('ascii'))
                else:
                    received_preset = json.loads(message)
                    #print(f"Received preset: {received_preset}")
                    if received_preset['user_id'] != self.user_id:
                        with open('friend.json', 'w') as friend_file:
                            json.dump(received_preset, friend_file)
                            friend_file.write('\n')

            except:
                print("no message received!")
                os.remove('friend.json')
                self.client.close()
                break

    def start(self):
        sending_thread = threading.Thread(target=self.connect_to_server)
        sending_thread.start()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
