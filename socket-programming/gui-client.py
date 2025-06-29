# Chat client with GUI

import socket
import threading
import tkinter as tk

# HOST = "138.68.140.83"
HOST = "localhost"
PORT = 1313


def enterChat():
    def recieve():
        global isChatting
        global chat
        while isChatting:
            try:
                recieved_message = client.recv(1024).decode()
                chat = chat + "\n" + recieved_message
                showText()
                if recieved_message == "bye":
                    isChatting = False
            except Exception as e:
                print(e)
                isChatting = False

    def send():
        global isChatting
        global chat
        try:
            message = msgInput.get()
            msgInput.delete(0, tk.END)
            chat = chat + "\n" + "You: " + message
            showText()
            client.send(message.encode())
            if message == "bye":
                isChatting = False
        except Exception as e:
            print(e)
            print("hello")
            isChatting = False

    def showText():
        global chat
        chatContainer.configure(text=chat)

    def closeWindow():
        root.destroy()

    # Chat window components
    chatContainer = tk.Label(master=root, text=chat, width=100, height=15)
    msgInput = tk.Entry(master=root)
    exitBtn = tk.Button(root, text="Exit", command=closeWindow, background="red")
    sendBtn = tk.Button(root, text="Send", command=send, default=tk.ACTIVE)

    chatContainer.anchor(anchor="nw")
    chatContainer.grid(row=1, rowspan=9, column=0)
    msgInput.grid(row=10, column=0)
    msgInput.focus_set()
    sendBtn.grid(row=10, column=1)
    exitBtn.grid(row=1, column=1)
    root.bind("<Return>", lambda event=None: sendBtn.invoke())

    # Recieving messages from server
    recieverThread = threading.Thread(name="Reciever", target=recieve)
    recieverThread.start()


def login():
    username = usernameInput.get()
    client.send(username.encode())
    usernameLbl.destroy()
    usernameInput.destroy()
    loginBtn.destroy()
    enterChat()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

isChatting = True
chat = ""

root = tk.Tk()
root.geometry("900x600")

# Login page components
headerLbl = tk.Label(
    master=root, text="Chat Application", height=3, width=50, background="lightblue"
)
usernameLbl = tk.Label(master=root, text="Enter your Username:", width=100)
usernameInput = tk.Entry(master=root)
loginBtn = tk.Button(root, text="Login", command=login, default=tk.ACTIVE)

headerLbl.grid(row=0, columnspan=2)
usernameLbl.grid(row=1)
usernameInput.grid(row=2)
usernameInput.focus_set()
loginBtn.grid(row=3)

root.bind("<Return>", lambda event=None: loginBtn.invoke())

root.mainloop()
isChatting = False
client.close()
print("Exited!!!")
