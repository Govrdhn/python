# Chat server for multi-client-group-chat with Multi-threading

import socket
import threading

# HOST = "138.68.140.83"
HOST = "localhost"
PORT = 1313

clientsList = []
clientConnThreads = []


def handleChat(sender: socket.socket, senderUsername: str):
    while True:
        try:
            recieved_message = sender.recv(1024).decode()
            if recieved_message == "":
                break
            for client in clientsList:
                if client != sender:
                    try:
                        client.send(f"{senderUsername}: {recieved_message}".encode())
                    except Exception as e:
                        clientsList.remove(client)
        except Exception as e:
            print(e)
            break


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server is listening on port {PORT}.")


while True:
    try:
        conn, addr = server.accept()
        username = conn.recv(1024).decode()
        print(f"{username} connected!")
        clientsList.append(conn)
        thread = threading.Thread(name=addr, target=handleChat, args=[conn, username])
        clientConnThreads.append(thread)
        thread.start()
    except Exception as e:
        print(e)
        break

for connThread in clientConnThreads:
    connThread.join()

server.close()
