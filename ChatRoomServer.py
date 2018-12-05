from socket import *
import datetime

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
activeIpArray = []
activeUserArray = []

def clientJoin(clientAddress):
    activeIpArray.append(clientAddress)
    userName, clientAddress = serverSocket.recvfrom(2048)
    decodedUserName = userName.decode()
    welcomeMessage = "Welcome to the chat room " + decodedUserName + "!"
    activeUserArray.append(decodedUserName)
    if len(activeUserArray) == 1:
        serverSocket.sendto(welcomeMessage.encode(), clientAddress)
    else:
        for x in range(0, len(activeUserArray)):
            print("send to " + activeUserArray[x])
            serverSocket.sendto(welcomeMessage.encode(), activeIpArray[x])
                
                
def clientQuit(clientAddress):  
    for x in range(0, len(activeIpArray)):
        if(activeIpArray[x]==clientAddress):
            goodbyeMessage = activeUserArray[x] + " has left the chat room."
            del activeUserArray[x]
            break
#     remove clientAddress from active users
    activeIpArray.remove(clientAddress)
#     send goodbye message to all active users
    for x in range(0, len(activeIpArray)):
        serverSocket.sendto(goodbyeMessage.encode(), activeIpArray[x])
        
def clientSend(clientAddress):
    for x in range(0, len(activeUserArray)):
            if clientAddress == activeIpArray[x]:
                modifiedMessage = activeUserArray[x] + ": " + decodedMessage
    print("Received: " + modifiedMessage)
    if len(activeUserArray) == 1:
            serverSocket.sendto("There is no one else in this chatroom".encode(), clientAddress)
    else:
        print("Send to: ", end = "")
        for x in range(0, len(activeIpArray)):
            if(activeIpArray[x]!=clientAddress):
                serverSocket.sendto(modifiedMessage.encode(), activeIpArray[x])
                if(x<len(activeIpArray)-1):
                    print(activeUserArray[x], end =", ")
                else:
                    print(activeUserArray[x])
        
    
print("The server is ready to receive.")
while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()
    
#   if message cotains join add user to the active user list
    if (decodedMessage.lower().find("join") >= 0 and (clientAddress not in activeIpArray)):
        print("Join")
        clientJoin(clientAddress)
        print(activeIpArray)
        print(activeUserArray)
        
#   if message is quit delete client from the active user array, delete client from the username array      
    elif decodedMessage.lower().find("quit") >= 0:
        print("Quit")
        clientQuit(clientAddress)
        if(len(activeUserArray)>0):
            print(activeIpArray)
            print(activeUserArray)
        else:
            print("No active users")
        
#   if message does not have join or quit, send the message every other client
    else:
        print("Normal")
        clientSend(clientAddress)
        print(activeIpArray)
        print(activeUserArray)       
        