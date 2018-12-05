from socket import *
import threading
import time


def listener():
    #May need to set a parameter to  so that when the user wants to quit the thread can know when to send
    #a goodbye message
    while True:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
        time.sleep(0.300)

# def sender():
#     while True:
        
serverName = 'localhost'
serverPort = 5000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Type \"Join\" to join the chat room: ")
if message.lower().find("join") >= 0:
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    userName = input("What is your user name? ")
    #lines 11 and 12 require multithreading. Clients cannot receive a message
    #until they send one.
    clientSocket.sendto(userName.encode(), (serverName, serverPort))
    welcomeMessage, serverAddress = clientSocket.recvfrom(2048)
    modifiedWelcomeMessage = welcomeMessage.decode()
    print(modifiedWelcomeMessage)
    #After client joins the listener thread runs immediately.
    t1 = threading.Thread(target=listener)
    t1.start()
    #Without formatting the incoming message is received after the receiving clients user name
    #e.g.: If Chris sent "HI", Jon would see "Jon: Chris: HI
    #message = input(userName + ": ")
    message = input()
    while message.lower().find('quit') < 0: 
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        message = input()

    clientSocket.sendto(message.encode(), (serverName, serverPort))
    if not t1.isAlive():
        clientSocket.close()
