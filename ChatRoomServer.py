from socket import *
import datetime

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
activeIpList = []
activeUserList = []
clientMuteList = []

class Client:
    blockList = []
    muteStatus = False
    def _init_(self, clientAddress, userName):
        self.clientAddress = clientAddress
        self.userName = userName

def clientJoin(clientAddress):
    activeIpList.append(clientAddress)
    clientMuteList.append(False)
    userName, clientAddress = serverSocket.recvfrom(2048)
    decodedUserName = userName.decode()
    welcomeMessage = "Welcome to the chat room " + decodedUserName + "!: "
    print(clientAddress)
    activeUserList.append(decodedUserName)
    if len(activeUserList) == 1:
        serverSocket.sendto(welcomeMessage.encode(), clientAddress)
    else:
        for x in range(0, len(activeUserList)):
            print("send to " + activeUserList[x])
            serverSocket.sendto(welcomeMessage.encode(), activeIpList[x])
                
def clientQuit(clientAddress):  
    for x in range(0, len(activeIpList)):
        if(activeIpList[x]==clientAddress):
            goodbyeMessage = activeUserList[x] + " has left the chat room.: " + clientAddress
            clientMuteList.pop(x)
            del activeUserList[x]
            break
    serverSocket.sendto("!quit".encode(), clientAddress)
#     remove clientAddress from active users
    activeIpList.remove(clientAddress)
#     send goodbye message to all active users
    for x in range(0, len(activeIpList)):
        serverSocket.sendto(goodbyeMessage.encode(), activeIpList[x])
        
def clientSend(clientAddress):
    for x in range(0, len(activeUserList)):
        if clientAddress == activeIpList[x]:
            modifiedMessage = activeUserList[x] + ": " + decodedMessage
    print("Received: " + modifiedMessage)
    if len(activeUserList) == 1:
            serverSocket.sendto("There is no one else in this chat room".encode(), clientAddress)
    else:
        print("Send to: ", end = "")
        for x in range(0, len(activeIpList)):
            print(clientMuteList)
            if(activeIpList[x]!=clientAddress and not clientMuteList[x]):
                serverSocket.sendto(modifiedMessage.encode(), activeIpList[x])
#                 if(x==len(activeIpList)-1):
                print(activeUserList[x], end =", ")
#                 else:
            else:
                print(activeUserList[x])
        
def clientMute(clientAddress):
    for x in range(0, len(activeIpList)):
        if(activeIpList[x] == clientAddress):
            clientMuteList[x] = True
    
def clientUnmute(clientAddress):
    for x in range(0, len(activeIpList)):
        if(activeIpList[x] == clientAddress):
            clientMuteList[x] = False
    
print("The server is ready to receive.")
while True:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message, clientAddress = serverSocket.recvfrom(2048)
    decodedMessage = message.decode()
    
#   if message cotains join add user to the active user list
    if (decodedMessage.lower().find("!join") > -1):
        print("Join")
        clientJoin(clientAddress)
        print(activeIpList)
        print(activeUserList)
        
#   if message is quit delete client from the active user List, delete client from the username List      
    elif (decodedMessage.lower().find("!quit") > -1):
        print("Quit")
        clientQuit(clientAddress)
        if(len(activeUserList)>0):
            print(activeIpList)
            print(activeUserList)
        else:
            print("No active users")
        
    elif (decodedMessage.lower().find("!mute") > -1 ):
        clientMute(clientAddress)
        print("Mute")
        print(activeIpList)
        print(activeUserList)  
        print(clientMuteList)     
        
        
    elif (decodedMessage.lower().find("!unmute") > -1):
        clientUnmute(clientAddress)
        print("Unmute")
        print(activeIpList)
        print(activeUserList)       
        print(clientMuteList)
        
#   if message does not have join or quit, send the message every other client
    else:
        print("Normal")
        clientSend(clientAddress)
        print(activeIpList)
        print(activeUserList)       
        