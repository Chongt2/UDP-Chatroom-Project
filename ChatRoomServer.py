from socket import *
import datetime

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
activeIpArray = []
activeUserArray = []

def addClient(clientAddress):
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
                
                
def removeClient(clientAddress):  
#     form goodbye message  
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
        
            
    
print("The server is ready to receive.")
while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message, clientAddress = serverSocket.recvfrom(2048)
    print(clientAddress)
    decodedMessage = message.decode()
    
#   if message is join, add a new client to the active user array, register the username into the activeUserArray
    if decodedMessage.lower().find("join") >= 0:
        addClient(clientAddress)
        print("Join")
        
#   if message is quit delete client from the active user array, delete client from the username array      
    elif decodedMessage.lower().find("quit") >= 0:
        removeClient(clientAddress)
        print("Quit")
        
#   if message does not have join or quit, send the message every other client
    else:
        print("Normal")
        for x in range(0, len(activeUserArray)):
            if clientAddress == activeIpArray[x]:
                modifiedMessage = activeUserArray[x] + ": " + decodedMessage
        print("message to be sent back: ")
        print(decodedMessage)
        if len(activeUserArray) == 1:
            serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
            for x in range(0, len(activeUserArray)):
                if clientAddress != activeIpArray[x]:
                    print("send to " + activeUserArray[x])
                    serverSocket.sendto(modifiedMessage.encode(), activeIpArray[x])
