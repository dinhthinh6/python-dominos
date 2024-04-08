import socket
from _thread import *
import random
import math
from src.Model import Domino, Player, Board
import _pickle as pickle
import time


# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5555

ROUND_TIME = 60 * 5

MASS_LOSS_TIME = 7

MAX_PLAYER = 2

W, H = 1600, 830

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen(2)  # listen for connections

print(f"[SERVER] Server Started with local ip {SERVER_IP}")

players = {}
connections = 0
_id = 0
start = False

board = []
dominoList = []
current_turn = 0
turn_start = False

for i in range(7):
    for j in range(i, 7):
        image_path = f"assets\\Domino{i}{j}.png"
        domino_new = Domino(i,j,image_path)
        dominoList.append(domino_new)

random.shuffle(dominoList)

def getFirstHand(player):
    for i in range(7):
        player.hand.append(dominoList.pop())

def changeTurn(turn):
    turn = int(turn)
    next_turn = 0
    for i in players:
        if turn == i:
            next_turn = turn + 1
            break
    if(next_turn == len(players)):
        next_turn = 0
    return next_turn
    

def update_link_domino(domino_board, domino):
    domino_x, domino_y =  domino.position[0], domino.position[1]
    domino_board_x, domino_board_y = domino_board.position[0], domino_board.position[1]

    if(domino_board.is_horizontal == True):
        if(domino.is_horizontal == True):
            if domino_x < domino_board_x:
                return 1, 2
            elif domino_x > domino_board_x:
                return 2, 1
        elif(domino.is_horizontal == False):
            if domino_x == domino_board_x and  domino_y < domino_board_y:
                return 1, 2
            elif domino_x == domino_board_x and domino_y > domino_board_y:
                return 1, 1
            elif domino_x > domino_board_x and domino_y < domino_board_y:
                return 2, 2
            elif domino_x > domino_board_x and domino_y > domino_board_y:
                return 2, 1
               
    elif (domino_board.is_horizontal == False):
        if(domino.is_horizontal == True):
            if domino_x < domino_board_x and domino_y == domino_board_y:
                return 1, 2
            elif domino_x < domino_board_x and domino_y > domino_board_y:
                return 2, 2
            
            elif domino_x > domino_board_x and domino_y == domino_board_y:
                return 1, 1
            elif domino_x > domino_board_x and domino_y > domino_board_y:
                return 2, 1
            
        elif(domino.is_horizontal == False):
            if domino_x == domino_board_x and domino_y < domino_board_y:
                return 1, 2
            elif domino_x == domino_board_x and domino_y > domino_board_y:
                return 2, 1

def updateBoard(position, domino):
    if(position == "start"):
        link = update_link_domino(board[0] ,domino)
        board[0].link = link[0]
        domino.link = link[1]
        board.insert(0, domino)
        
    elif(position == "end"):
        link = update_link_domino(board[len(board)-1] ,domino)
        board[len(board)-1].link  = link[0]
        domino.link = link[1]
        board.append(domino)

def threaded_client(conn, _id):
    global connections, players, board, start, current_turn, turn_start
	
    current_id = _id
    # recieve a name from the client
    data = conn.recv(16)
    name = data.decode("utf-8")
    conn.send(str.encode(str(current_id)))
    print("[LOG]", name, "connected to the server.")
    
    players[current_id] = Player(name)
    getFirstHand(players[current_id])

    while True: 
        try:
            data = conn.recv(1204)
            if not data:
                break
            data = data.decode("utf-8")
            if data.split(":")[0] == "put":
                split_data = data.split(":")
                domino_data = str(split_data[1])
                domino_data = domino_data.split("-")
                is_horizontal = True
                if(domino_data[6] == "False"):
                    is_horizontal = False
                domino = Domino(int(domino_data[0]), int(domino_data[1]), domino_data[2], [int(domino_data[3]), int(domino_data[4])], domino_data[5], is_horizontal, int(domino_data[7]), int(domino_data[8]))
                position = domino_data[9]
                turn = domino_data[10]
                current_turn = changeTurn(turn)
                updateBoard(position, domino)
                send_data = pickle.dumps((players, current_turn ,board, start))

            elif data.split(":")[0] == "pick":
                split_data = data.split(":")
                domino_data = str(split_data[1])
                domino_data = domino_data.split("-")
                is_horizontal = True
                if(domino_data[6] == "False"):
                    is_horizontal = False
                domino = Domino(int(domino_data[0]), int(domino_data[1]), domino_data[2], [int(domino_data[3]), int(domino_data[4])], domino_data[5], is_horizontal, int(domino_data[7]), int(domino_data[8]))
                index = int(domino_data[9])
                del players[current_id].hand[index]
                players[current_id].selected = domino
                # print(players[current_id].selected)
                send_data = pickle.dumps((players, current_turn ,board, start))

                # print(players[current_id].hand[index])
                # for i in range(len(players[current_id].hand)):
                #     print(players[current_id].hand[i])

                send_data = pickle.dumps((players, current_turn ,board, start))
            elif data.split(":")[0] == "putfirst":
                start = True
                split_data = data.split(":")
                domino_data = str(split_data[1])
                domino_data = domino_data.split("-")
                is_horizontal = True

                if(domino_data[6] == "False"):
                    is_horizontal = False
                domino = Domino(int(domino_data[0]), int(domino_data[1]), domino_data[2], [int(domino_data[3]), int(domino_data[4])], domino_data[5], is_horizontal, int(domino_data[7]), int(domino_data[8]))
                board.append(domino)
                turn = domino_data[9]
                current_turn = changeTurn(turn)
                send_data = pickle.dumps((players, current_turn ,board, start))
            
            elif data == "drop":
                players[current_id].hand.append(players[current_id].selected)
                players[current_id].selected = None
                send_data = pickle.dumps((players, current_turn ,board, start))

            elif data.split(":")[0] =="swap":
                split_data = data.split(":")
                turn = split_data[1]
                current_turn = changeTurn(turn)
                send_data = pickle.dumps((players, current_turn ,board, start))

            else:
                send_data = pickle.dumps((players, current_turn ,board, start))
            conn.send(send_data)
        except Exception as e:
            print(e)
            break  
    time.sleep(0.001)
        
	# When user disconnects	
    print("[DISCONNECT] Client Id:", current_id, "disconnected")

    connections -= 1 
    del players[current_id]  # remove client information from players list
    conn.close()  # close connection


print("[GAME] Setting up level")
print("[SERVER] Waiting for connections")

while True:
    host, addr = S.accept()
    print("[CONNECTION] Connected to:", addr)
     
	# start game when a client on the server computer connects
    if addr[0] == SERVER_IP and not(turn_start):
        turn_start = True
        current_turn = _id
        print("[STARTED] Game Started")
    connections += 1
    start_new_thread(threaded_client,(host,_id))
    _id += 1
     

# when program ends
print("[SERVER] Server offline")
