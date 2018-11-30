from socket import *

serverName = 'localhost'
serverPort = 5000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Type \"Join\" to join the chat room: ")
if message == "Join":
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    userName = input("What is your user name? ")
    #lines 11 and 12 require multithreading. Clients cannot receive a message
    #until they send one.
    clientSocket.sendto(userName.encode(), (serverName, serverPort))
    welcomeMessage, serverAddress = clientSocket.recvfrom(2048)
    modifiedWelcomeMessage = welcomeMessage.decode()
    print(modifiedWelcomeMessage + "!")
    message = input(userName + ": ")
    while message != "Quit": 
        #thread 1
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        #end thread 1
        #thread 2
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
        message = input(userName + ": ")
        #end thread 2
    clientSocket.close()
