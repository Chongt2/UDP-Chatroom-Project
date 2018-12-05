from socket import *
import datetime

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
ipArray=[]
userArray=[]
print("The server is ready to receive.")
while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message, clientAddress = serverSocket.recvfrom(2048)
    print(clientAddress)
    decodedMessage = message.decode()
    if decodedMessage.lower().find("join") >= 0:
        ipArray.append(clientAddress)
        userName, clientAddress = serverSocket.recvfrom(2048)
        decodedUserName = userName.decode()
        welcomeMessage = "Welcome to the chat room " + decodedUserName + "!"
        userArray.append(decodedUserName)
        if len(userArray) == 1:
            serverSocket.sendto(welcomeMessage.encode(), clientAddress)
        else:
            for x in range(0, len(userArray)):
                print("send to " + userArray[x])
                serverSocket.sendto(welcomeMessage.encode(), ipArray[x])
    elif decodedMessage.lower().find("quit") >= 0:
        for x in range(0, len(userArray)):
            if clientAddress == ipArray[x]:
                goodbyeMessage = userArray[x] + "has left the chat room."
                for y in range(0, len(userArray)):
                    serverSocket.sendto(goodbyeMessage.encode(), ipArray[y])
    else:
        print("OOPS")
        for x in range(0, len(userArray)):
            if clientAddress == ipArray[x]:
                modifiedMessage = userArray[x] + ": " + decodedMessage
        print("message to be sent back: ")
        print(modifiedMessage)
        if len(userArray) == 1:
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
            for x in range(0, len(userArray)):
                if clientAddress != ipArray[x]:
                    print("send to " + userArray[x])
                    serverSocket.sendto(modifiedMessage.encode(), ipArray[x])
