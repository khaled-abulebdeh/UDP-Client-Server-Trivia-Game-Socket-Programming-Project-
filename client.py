from socket import *
import threading
from time import *

def receiveMessages (clientSocket) ->None:
    
    while True:
        try:
            msgReceived, serverAddress =  clientSocket.recvfrom(2048)
            print(msgReceived.decode())
        except:
            pass
    

#serverPort = 5689
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(None)  # Ensure no timeout (blocking mode)
serverPort = 5689

#handle client message reciption using threads
thread = threading.Thread(target=receiveMessages,args=(clientSocket,))
# Start the thread
thread.start()


serverIP =input("Enter the server IP address:")
portNumber=int(input("Enter the server port number:"))
clientName= input("Enter your name:")


#connect client to server
msgToSend= serverIP+","+ str(portNumber)+ ","+clientName
clientSocket.sendto(msgToSend.encode(),(serverIP, portNumber))


#this loop is to submit answers to server
#the submission taks from as:
#answer: the answer
while True:
    msgToSend=input()
    clientSocket.sendto(("answer:"+msgToSend).encode(),(serverIP, portNumber))
    if (msgToSend.lower()=="exit"):
        print("You left the game..")
        break
    else:
        print("answer submitted: "+ msgToSend)

clientSocket.close()
