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
WINDOW_SIZE = (580, 580)
W, H = 1490, 720


class Client:
    def __init__(self, host, port, username, socket, oppenent):
        self.host = host
        self.port = port
        self.username = username
        self.oppenent_name = oppenent
        self.sock = socket
        self.addr = (self.host, self.port)
        data = "get-board"
        data = pickle.dumps(data)
        self.sock.send(data)
        # self.board = Board()
        reply = self.sock.recv(2048)
        data_received = pickle.loads(reply)
        self.board = data_received
        hand = self.board.hand_player()
        self.gui = PlaySurface(self.sock, self.host, self.port, username, hand, self.oppenent_name, False)

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
                        self.gui.gui_player.board.placed_dominoes = self.board.placed_dominoes
                        self.gui.gui_player.switch_turn()
                        self.gui.gui_player.check_continue_player()
                        self.gui.gui_player.other_player -= 1

                    elif data_received == "swap":
                        self.gui.gui_player.switch_turn()
                        self.gui.gui_player.check_continue_player()
                    elif data_received[0] == 'chat':
                        message = f"<p>{data_received[1]}:{data_received[2]}</p>"
                        self.gui.gui_player.chat_box.box_message.append_html_text(message)
                    # elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "over":
                    #     print(self.gui.gui_player.over)
                    #     self.gui.gui_player.check_continue_player()
                    #     if(self.gui.gui_player.over):
                    #         self.gui.over = True
                    #         self.gui.score = data_received[1]
                    #         self.gui.gui_player.score += self.gui.score

                    elif isinstance(data_received, tuple) and len(data_received) == 4 and data_received[0] == "game_over":
                        # if(self.gui.gui_player.over):
                        # self.gui.over = True
                        score = data_received[1]
                        self.gui.gui_player.status = "Draw"
                        self.gui.gui_player.turn_score = score
                        self.gui.gui_player.score += score
                        self.gui.gui_player.playing = False
                        self.gui.gui_player.first_play = data_received[2]
                        self.gui.gui_player.other_player_hand = data_received[3]

                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "play-again":
                        # self.gui.over = False
                        self.gui.gui_player.playing = True
                        if(self.gui.gui_player.first_play == True):
                            self.gui.gui_player.turn = True
                        else:
                            self.gui.gui_player.turn = False

                        self.gui.gui_player.over = False
                        self.gui.gui_player.play_again = False
                        self.gui.gui_player.board.placed_dominoes = []
                        self.gui.gui_player.board.domino_list = data_received[1]
                        self.gui.gui_player.hand = copy.deepcopy(self.gui.gui_player.board.hand_player())
                        # self.gui.gui_player.create_image_pg()
                        self.gui.gui_player.other_player = 7
                        self.gui.gui_player.other_player_hand = []

                        data_to_send = ("start-game", self.gui.gui_player.board.domino_list)           
                        data = pickle.dumps(data_to_send)
                        self.sock.send(data)
                        # other_score = data_received[1]
                        # print(other_score)
                    elif data_received == "winner":
                        self.gui.gui_player.status = "Lose"
                        self.gui.gui_player.playing = False
                        self.gui.gui_player.play_again = True
                        score = self.gui.gui_player.get_domino_score()
                        data_to_send = ("score", score, self.gui.gui_player.get_player_hand())           
                        data = pickle.dumps(data_to_send)
                        self.sock.send(data)

                    elif isinstance(data_received, tuple) and len(data_received) == 3 and data_received[0] == "score":
                        your_score = data_received[1]
                        self.gui.gui_player.turn_score = your_score
                        self.gui.gui_player.score += your_score
                        self.gui.gui_player.other_player_hand = data_received[2]
                    
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)
                self.sock.close()
                break

        print("QUIT")
        self.gui.quit = True

class Server:
    def __init__(self, host, port, username, surface):
        print(socket.gethostname())
        self.host = host
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
            title=f'IP Address:{self.get_ip_address()}')
        threading.Thread(target=self.accepted_connect).start()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    break
            if self.connected:
                break
            if loading.is_enabled():
                loading.update(events)
                loading.draw(surface)
            pygame.display.update()

        if self.connected:
            loading.disable()
            self.gui = PlaySurface(self.conn, self.addr[0], self.addr[1], username, hand, self.competitor_name, True)
            threading.Thread(target=self.receive, daemon=True).start()
            self.gui.run()

        if not self.connected:
            self.close()

    def accepted_connect(self):
        while not self.connected:
            try:
                self.conn, self.addr = self.sock.accept()
                print(self.conn)
                # Nhận dữ liệu từ client (nếu cần)
                data = self.conn.recv(1024)
                data = data.decode("utf-8")
                print(data)
                if data == 'Connected':
                    self.connected = True
                    # data_to_send = (self.board)
                    data_to_send = ("Connected",self.username)           
                    data = pickle.dumps(data_to_send)
                    self.conn.send(data)
                    break
                else:
                    self.connected = False
            except Exception:
                break

    def receive(self):
        while self.connected:
            try:
                reply = self.conn.recv(2048*4)
                try:
                    data_received = pickle.loads(reply)
                    if not data_received:
                        break
                    if data_received == "get-board":
                        data_to_send = (self.board)
                        data = pickle.dumps(data_to_send)
                        self.conn.send(data)
                        
                    if isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "put":
                        # Lấy danh sách dominoes từ dữ liệu nhận được
                        placed_dominoes = data_received[1]
                        self.board.placed_dominoes = placed_dominoes
                        self.gui.gui_player.board.placed_dominoes = self.board.placed_dominoes
                        self.gui.gui_player.switch_turn()
                        self.gui.gui_player.other_player -= 1

                    elif data_received == "swap":
                        self.gui.gui_player.switch_turn()

                    elif data_received[0] == 'chat':
                        message = f"<p>{data_received[1]}:{data_received[2]}</p>"
                        self.gui.gui_player.chat_box.box_message.append_html_text(message)

                    elif data_received == "winner":
                        self.gui.gui_player.status = "Lose"
                        self.gui.gui_player.playing = False
                        self.gui.gui_player.play_again = True
                        score = self.gui.gui_player.get_domino_score()
                        data_to_send = ("score", score, self.gui.gui_player.get_player_hand())                
                        data = pickle.dumps(data_to_send)
                        self.conn.send(data)
                        
                    elif isinstance(data_received, tuple) and len(data_received) == 3 and data_received[0] == "score":
                        your_score = data_received[1]
                        self.gui.gui_player.turn_score = your_score
                        self.gui.gui_player.score += your_score
                        self.gui.gui_player.other_player_hand = data_received[2]

                    elif isinstance(data_received, tuple) and len(data_received) == 3 and data_received[0] == "over":
                        print(self.gui.gui_player.over)
                        self.gui.gui_player.check_continue_player()
                        if(self.gui.gui_player.over):
                            # self.gui.over = True
                            your_score = data_received[1]
                            self.gui.gui_player.turn_score = your_score
                            self.gui.gui_player.other_player_hand = data_received[2]
                            self.gui.gui_player.score += your_score
                            oppenent_score = self.gui.gui_player.get_domino_score()
                            self.gui.gui_player.playing = False
                            self.gui.gui_player.status = "Draw"

                            #Ít điểm hơn thì chuyển lượt cho người đó đi trước khi bắt đầu game sau
                            if(oppenent_score <= your_score):
                                client_first_turn = True
                                self.gui.gui_player.first_play = False
                                data_to_send = ("game_over", oppenent_score, client_first_turn, self.gui.gui_player.get_player_hand())                
                                data = pickle.dumps(data_to_send)
                                self.conn.send(data)
                            else:
                                client_first_turn = False
                                self.gui.gui_player.first_play = True
                                data_to_send = ("game_over", oppenent_score, client_first_turn, self.gui.gui_player.get_player_hand())                
                                data = pickle.dumps(data_to_send)
                                self.conn.send(data)
                                
                    elif isinstance(data_received, tuple) and len(data_received) == 2 and data_received[0] == "start-game":
                        self.gui.gui_player.board.domino_list = data_received[1]

                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)
                self.connected = False
                break
        
        if not self.connected:
            print("QUIT")
            self.gui.quit = True
            self.conn.close()

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
        finally:
            s.close()
        return ip_address
    
    def close(self):
        self.sock.close()
        pygame.quit()
        sys.exit()

class PlaySurface:
    def __init__(self, connection, host, port, username, hand ,competitor_name=None, is_host=True):
        self.connection = connection
        self.gui_player = Player(connection, host, port, username, competitor_name, is_host)
        self.gui_player.hand = hand
        # self.gui_player.create_image_pg()
        self.gui_player.other_player = 7
        self.quit = False
        if(is_host == True):
            self.gui_player.turn = True
            self.gui_player.first_play = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.connection.close()
                    pygame.quit()
                    sys.exit()
                self.gui_player.event_loop(event)

            self.gui_player.play()
            
            # if(len(self.gui_player.hand) == 0 and self.gui_player.selected == None and self.gui_player.other_player > 0):
            #     self.gui_player.play_again = True
            #     # self.gui_player.score = self.score
            #     end_text = pygame.font.SysFont(None, 36).render("You Win! Press 'Enter' to play again. Your score: " + str(self.score) , True, (244,67,54))
            #     end_text_rect = end_text.get_rect(center=(W // 2, H // 2))
            #     self.gui_player.display_surface.blit(end_text, end_text_rect)
            #     self.gui_player.play_again = True

            # elif (self.gui_player.other_player == 0 and len(self.gui_player.hand) >0):
            #     self.gui_player.play_again = True
            #     # self.gui_player.score = self.score
            #     end_text = pygame.font.SysFont(None, 36).render("You Lose! Press 'Enter' to play again." , True, (211,67,54))
            #     end_text_rect = end_text.get_rect(center=(W// 2, H // 2))
            #     self.gui_player.display_surface.blit(end_text, end_text_rect)
            #     self.gui_player.play_again = True

            # elif self.over and len(self.gui_player.hand) >0 :
            #     self.gui_player.play_again = True
            #     # self.gui_player.score = self.score  
            #     end_text = pygame.font.SysFont(None, 36).render("Game Over! Press 'Enter' to play again. Your score: " + str(self.score), True, (255, 255, 255))
            #     end_text_rect = end_text.get_rect(center=(W // 2, H // 2))
            #     self.gui_player.display_surface.blit(end_text, end_text_rect)
            #     self.gui_player.play_again = True   
            if self.quit == True:
                break
            pygame.display.update()
        
        if self.quit == True:
            self.close()

    def close(self):
        self.connection.close()
        pygame.quit()
        sys.exit()
