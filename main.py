import queue
import socket
import sys
import threading
import _pickle as pickle
import copy

import pygame
import pygame_menu
from src.Model import Player, Board

FPS = 60
WINDOW_SIZE = (540, 540)
W, H = 1400, 720


class Client:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.competitor_name = 'Player 1'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.host, self.port)
        self.sock.connect(self.addr)
        data = "Connected"
        self.sock.send(str.encode(data))
        self.board = Board()
        reply = self.sock.recv(2048*4)
        data_received = pickle.loads(reply)
        self.board = copy.deepcopy(data_received)
        hand = self.board.hand_player()

        # self.sock.send(f'Connected:::{self.username}'.encode('utf-8'), (self.host, self.port))

        self.gui = PlaySurface(self.sock, self.host, self.port, username,hand, self.competitor_name, False)
        # self.gui.game_gui_window.clicked = True

        threading.Thread(target=self.receive, daemon=True).start()
        self.gui.run()

    def receive(self):
        while True:
            try:
                reply = self.sock.recv(2048*4)
                try:
                    data_received = pickle.loads(reply)
                    if isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "put":
                        # Lấy danh sách dominoes từ dữ liệu nhận được
                        placed_dominoes = data_received[1]
                        self.board.placed_dominoes = placed_dominoes
                        self.gui.gui_player.board.placed_dominoes = copy.deepcopy(self.board.placed_dominoes)
                        self.gui.gui_player.switch_turn()
                        self.gui.gui_player.other_player -= 1

                    elif data_received == "swap":
                        self.gui.gui_player.switch_turn()

                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "over":
                        print(self.gui.gui_player.over)
                        self.gui.gui_player.check_continue_player()
                        if(self.gui.gui_player.over):
                            self.gui.over = True
                            self.gui.score = data_received[1]

                    elif data_received == "winner":
                        score = self.gui.gui_player.get_domino_score()
                        data_to_send = ("score", score)           
                        data = pickle.dumps(data_to_send)
                        self.sock.send(data)

                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "score":
                        self.gui.score = data_received[1] 
                    else:
                        print("Received data does not contain 'put' string")
                    
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)
                self.sock.close()
                break

class Server:
    def __init__(self, host, port, username, surface):
        self.host = socket.gethostbyname("localhost")
        self.port = port
        self.username = username
        self.competitor_name = 'Player 2'
        self.connected = False
        self.addr = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.conn = None
        self.board = Board()
        self.board.create()
        self.board.shuffle()
        hand = self.board.hand_player()
        print(f"[SERVER] Server Started with local ip {self.host}")
        loading = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=pygame_menu.themes.THEME_BLUE,
            title='Waiting for client',
            width=WINDOW_SIZE[0]
        )
        loading.add.label(
            title=f'IP Address:{socket.gethostbyname("localhost")}')
        threading.Thread(target=self.accepted_connect).start()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.connected:
                break
            if loading.is_enabled():
                loading.update(events)
                loading.draw(surface)
            pygame.display.update()
        loading.disable()
        self.gui = PlaySurface(self.conn, self.addr[0], self.addr[1], username,hand, self.competitor_name, True)
        threading.Thread(target=self.receive, daemon=True).start()
        self.gui.run()

    def accepted_connect(self):
        while True:
            try:
                self.conn, self.addr = self.sock.accept()
                # print(self.conn)
                # Nhận dữ liệu từ client (nếu cần)
                data = self.conn.recv(1024)
                data = data.decode("utf-8")
                # print(data)
                if data == 'Connected':
                    self.connected = True
                    data_to_send = (self.board)           
                    data = pickle.dumps(data_to_send)
                    self.conn.send(data)
                    # self.sock.sendto(f'Connected:::{self.username}'.encode('utf-8'), self.addr)
                    break
                else:
                    self.connected = False
            except Exception:
                break

    def receive(self):
        while True:
            try:
                reply = self.conn.recv(2048*4)
                # reply = self.sock.recv(2048*4)
                try:
                    data_received = pickle.loads(reply)
                    # print(data_received)
                    if isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "put":
                        # Lấy danh sách dominoes từ dữ liệu nhận được
                        placed_dominoes = data_received[1]
                        self.board.placed_dominoes = placed_dominoes
                        self.gui.gui_player.board.placed_dominoes = copy.deepcopy(self.board.placed_dominoes)
                        self.gui.gui_player.switch_turn()
                        self.gui.gui_player.other_player -= 1
                        # Xử lý dữ liệu dominoes ở đây
                        # print("Received placed dominoes:", placed_dominoes)

                    elif data_received == "swap":
                        self.gui.gui_player.switch_turn()
                    elif data_received == "winner":
                        score = self.gui.gui_player.get_domino_score()
                        data_to_send = ("score", score)                
                        data = pickle.dumps(data_to_send)
                        self.conn.send(data)
                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "score":
                        self.gui.score = data_received[1] 
                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "over":

                        print(self.gui.gui_player.over)
                        # self.gui.gui_player.check_continue_player()
                        self.gui.gui_player.check_continue_player()
                        if(self.gui.gui_player.over):
                            self.gui.over = True
                            self.gui.score = data_received[1]
                    else:
                        print("Received data does not contain 'put' string")
                    
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)
                self.sock.close()
                break

class PlaySurface:
    def __init__(self, connection, host, port, username, hand ,competitor_name=None, is_host=True):
        self.connection = connection
        self.gui_player = Player(connection, host, port, username, competitor_name, is_host)
        self.gui_player.hand = hand
        self.gui_player.create_image_pg()
        self.gui_player.other_player = 7
        self.end_game = False
        self.over = False
        self.win = False
        self.score = 0
        if(is_host == True):
            self.gui_player.turn = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.connection.close()
                    pygame.quit()
                    sys.exit()
                self.gui_player.event_loop(event)
            
            self.gui_player.play()
                
            if self.over and self.gui_player.over:
                self.gui_player.score = self.score  
                end_text = pygame.font.SysFont(None, 36).render("Game Over! Press 'R' to play again. Your score: " + str(self.score), True, (255, 255, 255))
                end_text_rect = end_text.get_rect(center=(W // 2, H // 2))
                self.gui_player.display_surface.blit(end_text, end_text_rect)

            if(len(self.gui_player.hand) == 0 and self.gui_player.selected == None):
                self.gui_player.score = self.score
                end_text = pygame.font.SysFont(None, 36).render("You Win! Press 'Enter' to play again. Your score: " + str(self.score) , True, (244,67,54))
                end_text_rect = end_text.get_rect(center=(W // 2, H // 2))
                self.gui_player.display_surface.blit(end_text, end_text_rect)

            if(self.gui_player.other_player == 0):
                self.gui_player.score = self.score
                end_text = pygame.font.SysFont(None, 36).render("You Lose! Press 'Enter' to play again." , True, (211,67,54))
                end_text_rect = end_text.get_rect(center=(W// 2, H // 2))
                self.gui_player.display_surface.blit(end_text, end_text_rect)

            pygame.display.update()

    def close(self):
        self.connection.close()
        pygame.quit()
        sys.exit()
