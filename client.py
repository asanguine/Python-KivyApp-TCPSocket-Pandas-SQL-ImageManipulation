# client.py
import socket
import threading
from model import retrieve_user_id, retrieve_preset, create_connection
import json

conn = create_connection()
user_id = retrieve_user_id(conn)
preset_data = retrieve_preset(conn, user_id)
nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Send user ID to the server
client.send(user_id.encode('ascii'))
preset_info = {'clothe': preset_data['clothe'], 'hair': preset_data['hair'], 'expression': preset_data['expression']}
client.send(json.dumps(preset_info).encode('ascii'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))
    
# Start two threads for receiving and writing messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
