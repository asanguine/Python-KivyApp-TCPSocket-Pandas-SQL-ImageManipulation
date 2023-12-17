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

client.send(user_id.encode('ascii'))
preset_info = {'clothe': preset_data['clothe'], 'hair': preset_data['hair'], 'expression': preset_data['expression']}
client.send(json.dumps(preset_info).encode('ascii'))

received_preset = None

def receive():
    global received_preset
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                # Assuming the message contains the received preset as a JSON string
                received_preset = json.loads(message)
                print(f"Received preset: {received_preset}")
        except:
            print("An error occurred!")
            client.close()
            break



def write():
    while True:
        #message = '{}: {}'.format(nickname, input(''))
        message = ''
        client.send(message.encode('ascii'))
        #pass



# Start two threads for receiving and writing messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()



