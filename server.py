
from socket import *
import threading
from time import *
import random

numOfPlayers=0
numOfPlayersAnswerd=0
correctAnswer="" #to allow thread server to access the correct answer, to check players' answers correctness

def addClinet (clientAddress:str, clientName:str, clientsList:list): 

    #: Number of entries
    # Create a dictionary for the student
    client = {
          "clientAddress": clientAddress ,
          "clientName": clientName,
          "score": 0 , #score in current round
          "wonRounds": 0 , # num of rounds that client has won
          "hasAnswerdQ": False , # has the client answerd the current question?
          "isPlaying": True, # to determine if client is not responding to game
          "mustQuit": True #if player does not respond in a round, disconnect them but keep records
          #quit is true just as initialization, if player answers, it will be set to false
        }
    clientsList.append(client)

def  isExisted (clientAddress : str , clientsList : list ) ->  bool: 
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
          return  True 
    return False 

def  getClientName (clientAddress : str , clientsList : list ) ->  str: 
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
            return client ["clientName"]
def getClient (clientAddress , clientsList : list ) ->  dict:
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
            return client 
       
def  getWonRounds (clientAddress : str , clientsList : list ) ->  int : 
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
        return client ["wonRounds"]
 
def  hasClientAnswerd (clientAddress : str , clientsList : list ) ->  bool: 
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
              return client["hasAnswerdQ"]

def  isClientPlaying (clientAddress : str , clientsList : list ) ->  bool: 
    for client in clientsList : 
       if client["clientAddress"] ==  clientAddress : 
             return client["isPlaying"]

def sendToPlayers (message:str, clientsList:list)->None: 
    for client in clientsList:
        if client["isPlaying"]==True:
            serverSocket.sendto(message.encode(),client["clientAddress"])
            sleep(0.1)  # Small delay to prevent message collisions

def sendToPlayersExcept (clientAddressExcepted,message:str, clientsList:list)->None: 
    for client in clientsList:
        if client["clientAddress"]!=clientAddressExcepted and client["isPlaying"]==True:
            serverSocket.sendto(message.encode(),client["clientAddress"])
            sleep(0.1)  # Small delay to prevent message collisions

def sendToClient (clientAddress,message:str)->None: 
    serverSocket.sendto(message.encode(),clientAddress)
    sleep(0.1)  # Small delay to prevent message collisions

def getPlayersScore (clientsList:list)->str:
    result="Current Scores:\n"
    for client in clientsList:
        if client["isPlaying"]:
            result+=f"* {client["clientName"]}: {client["score"]:.2f} points\n"

    return result

def listenToPort (serverSocket,serverPort, clientsList:list) ->None:
    global numOfPlayers
    global correctAnswer
    global numOfPlayersAnswerd

    print (f"\nThe server is listening to {serverPort} port, and ready to receive messages\n") 

    while True:
        try:
            serverSocket.settimeout(1)
            msg, clientAddress = serverSocket.recvfrom(2048)
            msg= msg.decode()

            """
            to check if reveived message is an answer, 
            it must start with "answer:", other wise: it is new client connecting
            """

            #client is trying to connect to server
            if  not isExisted(clientAddress,clientsList):
                #msg is client's info to connect
                clientInfo=msg

                # Split the message into components (serverIP, portNumber, clientName)
                parts = clientInfo.split(",")  # Assuming the client separates fields with commas
                if len(parts) == 3:  # Ensure the expected format
                    serverIP = parts[0].strip()
                    portNumber =int (parts[1].strip())
                    clientName = parts[2].strip()

                addClinet(clientAddress, clientName,clientsList)
                numOfPlayers+=1
                #send welcome message 
                msgToSend=f"\n{clientName} has joined the game\n  current number of players is {numOfPlayers}\n"
                sendToPlayers(msgToSend, clientsList)

                print(f"\n{clientName} joined the game from {clientAddress}\n")


            #to reach here, means player is existed

            #if player has joined before, but disconnected: -> reconnect again
            elif  not isClientPlaying(clientAddress, clientsList):
                client=getClient(clientAddress,clientsList)
                client["isPlaying"]=True
                client["mustQuit"]=True #just idenifier, if they respond to a question at least, it will be set to false


            #if player is playing, they are submitting answers, or want to exit
            elif msg.startswith("answer:"):

                client=getClient(clientAddress,clientsList)
                # Handle answer message
                playerAnswer = str(msg[len("answer:"):].strip())

                #if player wants to exit
                if playerAnswer.lower().startswith("exit"):
                    client["isPlaying"]=False
                    client["mustQuit"]=False #we disconnected them using isPlaying flag
                    numOfPlayers-=1
                    print(f"{client["clientName"]} with {clientAddress} exited the game\n")

                
                #if player wants to answer for the first time for the current Q
                elif not hasClientAnswerd(clientAddress,clientsList):
                    #to prevent player from answering twice for the same Q
                    client["hasAnswerdQ"]=True
                    client["mustQuit"]=False
                    if playerAnswer.lower() == correctAnswer.lower():#correct answer
                        numOfPlayersAnswerd+=1
                        client["score"]+= (1/numOfPlayersAnswerd)
                        print(f"received answer from {client["clientName"]}, {clientAddress}: {playerAnswer} - correct!")
                    else:#wrong answer
                        print(f"received answer from {client["clientName"]}, {clientAddress}: {playerAnswer} - Incorrect")


        except:
            pass

def clearAnswerFlag(clientsList:list)->None:
    for client in clientsList:
        if client["isPlaying"]==True:
            client["hasAnswerdQ"]=False

def clearScores (clientsList:list)->None:
    for client in clientsList:
        client["score"]=0

def set_mustQuit_flag (clientsList:list)->None:
    for client in clientsList:
        if client["isPlaying"]:
            client["mustQuit"]=True

def quitDisconnectedPlayers (clientsList:list)->None:
    global numOfPlayers
    for client in clientsList:
        if client["mustQuit"]==True:
            client["isPlaying"]= False
            client["mustQuit"]=False
            numOfPlayers-=1

def getWinner_in1Round (clientsList:list)->dict:
    max=-1
    winner={}
    for client in clientsList:
        if client["isPlaying"] and client["score"]>max:
            max=client["score"]
            winner=client
    return winner

# Dataset of 20 questions 
dataSet=[
    {"question": "What is the basic unit of life?", "answer": "The cell"},
    {"question": "What is the process by which plants make their own food?", "answer": "Photosynthesis"},
    {"question": "What is the main component of the human brain?", "answer": "Water"},
    {"question": "Which organ in the human body is responsible for pumping blood?", "answer": "The heart"},
    {"question": "What is the molecule that carries genetic information?", "answer": "DNA"},
    {"question": "What is the universal solvent essential for life?", "answer": "Water"},
    {"question": "What gas do humans exhale as a waste product of respiration?", "answer": "Carbon dioxide (CO2)"},
    {"question": "What is the main source of energy for life on Earth?", "answer": "The Sun"},
    {"question": "What organ in the human body filters waste from the blood?", "answer": "The kidneys"},
    {"question": "What is the chemical process by which cells release energy from food?", "answer": "Cellular respiration"},
    {"question": "What is the largest organ in the human body?", "answer": "The skin"},
    {"question": "What is the process by which organisms produce offspring?", "answer": "Reproduction"},
    {"question": "What is the primary function of red blood cells?", "answer": "To carry oxygen"},
    {"question": "Which system in the human body defends against diseases?", "answer": "The immune system"},
    {"question": "What is the term for a group of similar cells working together?", "answer": "A tissue"},
    {"question": "What type of organism can survive without oxygen?", "answer": "Anaerobic organisms"},
    {"question": "What is the natural environment where an organism lives called?", "answer": "Habitat"},
    {"question": "What is the term for organisms that can make their own food?", "answer": "Producers or autotrophs"},
    {"question": "What is the average temperature of the human body in Celsius?", "answer": "37°C"},
    {"question": "What are the building blocks of proteins?", "answer": "Amino acids"},
]

clientsList=[] 

#initiate the server
serverPort = 5689
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
thread = threading.Thread(target=listenToPort, args=(serverSocket,serverPort,clientsList))
# Start the thread
thread.start()

numOfRounds=3
numOfQuestions=3
for i in range (numOfRounds):# for rounds
    while numOfPlayers<2 :
        print("waiting for at least two clients to participate")
        sleep(2)
    msgToSend=f"Strting round #{i+1} after 60s! Get ready!\n"
    sendToPlayers(msgToSend,clientsList)
    print(f"\nStrting round #{i+1} after 60s")

    sleep (60)

    for j in range(numOfQuestions):
        #choose random Q to send to all players
        question_and_answer=dict (random.choice(dataSet))
        question=str (question_and_answer["question"]).strip()
        correctAnswer=str (question_and_answer["answer"]).strip()

        """
        Send a question to players as this form
        Question 1: the question...
        Enter your answer (or 'exit' to quit)
        """
        msgToSend= f"Quesion {j+1}: "+question+"\n  Enter your answer (or 'exit' to quit)"
        sendToPlayers(msgToSend,clientsList)
        print(f"\nQuesion {j+1}: "+question)
        sleep(80)#wait for players to submit answers
#correctAnswer="trash, to prevent user to get scored after time is up"#
        print ("\nTime is UP!\n")
        sendToPlayers(f"\nTime is UP! The correct answer was {correctAnswer}",clientsList)
        sendToPlayers ("\n"+getPlayersScore(clientsList),clientsList)
        sleep (10)

        #set flag to False, to allow players to answer for next comming question
        clearAnswerFlag(clientsList)
        numOfPlayersAnswerd=0
    
    #round num i is over

    # announce the winner of the round 
    client=getWinner_in1Round(clientsList)
    client["wonRounds"]+=1

    #quit players who haven't answerd at this round
    sendToPlayers("Game Over!",clientsList)
    quitDisconnectedPlayers(clientsList)
    msgToSend=f"The winner in this round is {client["clientName"]} (has won {client["wonRounds"]} rounds untill now)"
    sendToPlayers(msgToSend, clientsList)
    print(msgToSend)
    print(f"Round {i+1} ended")
    clearScores(clientsList)#to start from score 0 in next round
    set_mustQuit_flag(clientsList)
    

        
    






    