import socket
import threading
import json
import time
from model import retrieve_user_id, retrieve_preset, create_connection
import friend

class MyClient:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.user_id = None
        self.preset_data = None
        self.client = None
        self.connected = False

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 55555))
            self.connected = True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return

        self.user_id = retrieve_user_id(create_connection())

        self.client.send(self.user_id.encode('ascii'))

        while self.connected:
            self.send_user_data()
            time.sleep(3)

    def send_user_data(self):
        try:
            self.preset_data = retrieve_preset(create_connection(), self.user_id)
            x = friend.get_character_pos()['x']
            y = friend.get_character_pos()['y']
            size = friend.get_character_pos()['size']

            preset_info = {'user_id': self.user_id,
                           'clothe': self.preset_data['clothe'],
                           'hair': self.preset_data['hair'],
                           'expression': self.preset_data['expression'],
                           'position': {'x': x, 'y': y, 'size': size}}

            self.client.send(json.dumps(preset_info).encode('ascii'))
            #print(f'\n\n sending data from {self.user_id}\n\n')
        except Exception as e:
            print(f"Error sending user data: {e}")

    def receive_messages(self):
        #print(f'\n\n status: {self.connected}\n\n')
        #print("\n\nReceive messages function started.\n\n")
        self.connected = True
        #print(f'\n\n status: {self.connected}\n\n')
        while self.connected:
            #print("\n\n trying to receive now\n\n")
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.user_id.encode('ascii'))
                else:
                    received_preset = json.loads(message)
                    if received_preset.get('disconnect'):
                        friend.set_friend_preset({'clothe': 1, 'hair': 1, 'expression': 1})
                        #print("User disconnected. Resetting friend's preset.")
                    else:
                        received_preset = received_preset
                        if received_preset['user_id'] != self.user_id:
                            friend.receive_friend_preset(received_preset)
                            #print(f"\n\nreceiving from {received_preset['user_id']}\n\n")

            except Exception as e:
                #print(f"Error receiving messages: {e}")
                self.client.close()
                self.connected = False
                break
            #time.sleep(3)

    def start(self):
        sending_thread = threading.Thread(target=self.connect_to_server)
        sending_thread.start()

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
