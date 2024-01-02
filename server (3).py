# import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  #list of connected clients



shift = 5

def encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            # Harf ise sadece harfleri kaydır
            if char.isupper():
                encrypted_message += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                encrypted_message += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            # Harf değilse olduğu gibi bırak
            encrypted_message += char
    return encrypted_message

# Mesajları şifreleyen fonksiyon
def encrypt_message(username, message, shift):
    encrypted_msg = encrypt(message, shift)
    final_msg = username + '~' + encrypted_msg
    return final_msg







#function to listen for messsages from a client
def listen_messages(client, username):
    
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            #final_msg = username + '~' + message
            #send_messages_to_all(final_msg)


            encrypted_message = encrypt_message("SERVER", message, shift)
            send_messages_to_all(encrypted_message)

        else:
            print(f"Message from client {username} is empty.")

#function to send message to a single client
def send_message(client, message):

    client.sendall(message.encode())

def send_messages_to_all(message):
    
    for user in active_clients:
        send_message(user[1], message)    #user 1 bc we get the 2nd thing in array which is client

# function to handle client
def client_handler(client):
    
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} joined the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty.")

    threading.Thread(target = listen_messages, args = (client, username, )).start()

def main():

    #SOCK_STREAM = TCP
    #SOCK_DGRAM = UDP

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target = client_handler, args = (client, )).start()

if __name__ == '__main__':
    main()