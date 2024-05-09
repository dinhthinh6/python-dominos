import pygame
import random
import copy
pygame.font.init()
import _pickle as pickle
import time
import pygame_gui



W, H = 1490, 720
TURN_FONT = pygame.font.SysFont("", 30)
WHITE = (255, 255, 255)
BROWN = (210, 107, 3)
GRAY = (127, 127, 127)
GREEN = (0, 128, 0)
PASS_FONT = pygame.font.Font(None, 32)
text_font = pygame.font.Font(None, 24)

manager = pygame_gui.UIManager((W, H), 'src/theme.json')
clock = pygame.time.Clock()
user_text = ''
# Font chữ
font = pygame.font.Font(None, 24)

color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False

class Player:
    def __init__(self, connection, host, port, username=None, competitor_name=None, is_host=True):
        self.connection = connection
        self.host = host
        self.port = port
        self.username = username
        self.is_host = is_host
        self.hand = []  # Danh sách domino trong tay
        self.selected = None
        self.display_surface = pygame.display.set_mode((W,H))
        self.turn = None
        self.is_dragging = False
        self.error = False
        self.box_help = [False,0,0]
        self.insert_start = False
        self.board = Board(self.display_surface)
        self.other_player = 7
        self.other_player_hand = []
        self.rotated = 1
        self.left_domino = False
        self.up_domino = False
        self.over = False
        self.domino_score = 0
        self.score = 0
        self.turn_score = 0
        self.play_again = False
        self.playing = True
        self.first_play = False
        self.sound_init()
        self.button_pass_init()
        self.chat_box = ChatBox(self.display_surface)
        self.chatting = False
        self.status = ""

    def play(self):
        # self.check_continue_player()
        self.draw_screen()
        self.chat_box.draw_message()
        self.draw_domino()
        self.draw_other_player()
        self.board.draw_board()
        self.draw_end_game()
        self.draw_box_help()
        self.draw_domino_selected()
        self.draw_turn()
        self.draw_score()
        self.draw_turtorial()
        self.draw_button_pass()
        self.draw_sound()
        self.chat_box.draw_chat_box()


    def sound_init(self):
        self.sound = pygame.mixer.Sound("./assets/sound/bg.wav")
        self.sound.play()
        self.is_sound_on = True

        self.button_image_on = pygame.image.load("./assets/ic_volume.png")
        self.button_image_off = pygame.image.load("./assets/ic_volume_off.png")

        self.button_image_on = pygame.transform.scale(self.button_image_on, (60,60))
        self.button_image_off = pygame.transform.scale(self.button_image_off, (60,60))

        self.button_image = self.button_image_on if self.is_sound_on else self.button_image_off

    def toggle_sound(self):
        self.is_sound_on = not self.is_sound_on  # Chuyển đổi trạng thái

        if self.is_sound_on:
            self.sound.play(-1) #lặp âm thanh
            self.button_image = self.button_image_on
        else:
            self.sound.stop()
            self.button_image = self.button_image_off

    def button_pass_init(self):
        self.button_pass_color = (0, 128, 0)
        self.button_pass_width = 150
        self.button_pass_height = 50
        self.button_pass_x = W - self.button_pass_width - 40
        self.button_pass_y = H - self.button_pass_height - 40
        self.button_pass_text = "PASS"
        
    def draw_button_pass(self):
        
        pygame.draw.rect(self.display_surface, WHITE, (self.button_pass_x, self.button_pass_y, self.button_pass_width, self.button_pass_height),
                          0, 10)
        pygame.draw.rect(self.display_surface, self.button_pass_color, (self.button_pass_x + 2, self.button_pass_y + 2, self.button_pass_width - 4, self.button_pass_height - 4), 
                         0, 10)
        
        text_surface = PASS_FONT.render(self.button_pass_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.button_pass_x + self.button_pass_width // 2, self.button_pass_y + self.button_pass_height // 2))
        self.display_surface.blit(text_surface, text_rect)

    def draw_sound(self):
        self.button_position = (W - 60 - 50, 50)  # Right-aligned position)
        self.display_surface.blit(self.button_image, self.button_position)

    def draw_end_game(self):
        if self.playing:
            return
        self.play_again = True
        message = ''
        color = ''
        if self.status == "Win":
            message = f"You Win! Press 'Enter' to play again. Your score: {self.turn_score}"
            color = (244, 67, 54)
        elif self.status == "Lose":
            message = "You Lose! Press 'Enter' to play again."
            color = (211, 67, 54)
        elif self.status == "Draw":
            message = f"Game Over! Press 'Enter' to play again. Your score: {self.turn_score}"
            color = (255, 255, 255)

        end_text = pygame.font.SysFont(None, 36).render(message, True, color)
        end_text_rect = end_text.get_rect(center=(W // 2, H // 4))

        border_rect = pygame.Rect(end_text_rect.x - 10, end_text_rect.y - 10,
                              end_text_rect.w + 15, end_text_rect.h + 15)
        pygame.draw.rect(self.display_surface, (0, 0, 0), border_rect, 0, 10)  

        self.display_surface.blit(end_text, end_text_rect)

    def get_domino_score(self):
        domino_score = 0
        for i, domino in enumerate(self.hand):
            domino_score += domino.dot1 + domino.dot2
        return domino_score

    def draw_score(self):
        text = TURN_FONT.render("Score: " + str(self.score) , 1,(255,255,255))
        self.display_surface.blit(text,(10, 60))
    
    def check_continue_player(self):
        if len(self.board.placed_dominoes) == 1:
            frist_domino = self.board.placed_dominoes[0]
            for i, domino in enumerate(self.hand):
                if domino.check_continue_game_first_domino(frist_domino):
                    self.over = False
                    return 
                self.over = True
                
            if(self.selected != None and self.selected.check_continue_game_first_domino(frist_domino)):
                self.over = False

            domino_score = 0
            for i, domino in enumerate(self.hand):
                domino_score += domino.dot1 + domino.dot2

            if self.is_host==False and self.over and self.play_again == False:
                data_to_send = ("over", domino_score, self.get_player_hand())           
                data = pickle.dumps(data_to_send)
                self.connection.send(data) 
        elif len(self.board.placed_dominoes) > 1:
            domino_start = self.board.placed_dominoes[0]
            domino_end = self.board.placed_dominoes[len(self.board.placed_dominoes)-1]

            for i, domino in enumerate(self.hand):
                if domino.check_continue_game(domino_start, domino_end):
                    self.over = False
                    return 
                self.over = True
                
            if(self.selected != None and self.selected.check_continue_game(domino_start, domino_end)):
                self.over = False

            domino_score = 0
            for i, domino in enumerate(self.hand):
                domino_score += domino.dot1 + domino.dot2

            if self.is_host==False and self.over and self.play_again == False:
                data_to_send = ("over", domino_score, self.get_player_hand())           
                data = pickle.dumps(data_to_send)
                self.connection.send(data)  

    def draw_screen(self):
        self.display_surface.fill((210, 107, 3))

        rect_width = W # Chiều rộng của hình chữ nhật bằng với chiều rộng của cửa sổ đồ họa
        rect_height = 400
        rect_x = 0  # Vị trí x để hình chữ nhật nằm ở giữa màn hình theo chiều ngang
        rect_y = (H - rect_height) // 2  # Vị trí y để hình chữ nhật nằm giữa màn hình theo chiều dọc
        pygame.draw.rect(self.display_surface, (9, 148, 15), (rect_x, rect_y, rect_width, rect_height))

        # Tạo viền bọc domino (oppent's)
        rect_width = 760
        rect_height = 140
        rect_x = (W - rect_width) // 2  # Vị trí x để hình chữ nhật nằm giữa màn hình theo chiều ngang
        rect_y = (H - rect_height) // 20 - 24  # Vị trí y để hình chữ nhật nằm ở phía trên theo chiều dọc
        rect_radius = 10

        # Vẽ hình chữ nhật nhỏ hơn lên trên với màu trắng
        border_width = 2
        pygame.draw.rect(self.display_surface, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_width,border_radius=rect_radius)

        # Tạo viền bọc domino (you)
        rect_width = 760
        rect_height = 140
        rect_x = (W - rect_width) // 2  # Vị trí x để hình chữ nhật nằm giữa màn hình theo chiều ngang
        rect_y = (H - rect_height) - 5  # Vị trí y để hình chữ nhật nằm ở phía trên theo chiều dọc
        rect_radius = 10
        # Vẽ hình chữ nhật nhỏ hơn lên trên với màu trắng
        border_width = 2
        pygame.draw.rect(self.display_surface, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_width,border_radius=rect_radius)
    
    def draw_domino(self):
        for i, domino in enumerate(self.hand):
            image = domino.get_image_pg()
            if(image == domino.get_image()):
                image = pygame.image.load(image)
            # image = pygame.image.load(domino_image)
            position_x = (W - len(self.hand) * domino.width * 2) // 2 + domino.width * i * 2
            position_y = H - domino.height

            # Move the hand
            position_y -= 20
            position_x += 25

            domino.set_position(position_x, position_y)
            self.hand[i].set_position(position_x, position_y)
            rect = pygame.Rect(position_x, position_y , domino.width, domino.height)
            resized_image = pygame.transform.scale(image, (domino.width, domino.height))
            self.display_surface.blit(resized_image, rect)

    def draw_other_player(self):
        domino_width = 48
        domino_height = 96
        if self.playing == False:
            for i, domino in  enumerate(self.other_player_hand):
                domino_image = domino.get_image()
                image = pygame.image.load(domino_image)
                position_x = (W - self.other_player * domino_width * 2) // 2 + domino_width * i * 2
                position_y = 0

                # Move the hand
                position_y += 20
                position_x += 25

                rect = pygame.Rect(position_x, position_y , domino_width, domino_height)
                resized_image = pygame.transform.scale(image, (domino_width, domino_height))
                self.display_surface.blit(resized_image, rect)
        else:
            for j in range (self.other_player):
                domino_image = f"assets/Domino.png"
                image = pygame.image.load(domino_image)
                position_x = (W - self.other_player * domino_width * 2) // 2 + domino_width * j * 2
                position_y = 0

                # Move the hand
                position_y += 20
                position_x += 25

                rect = pygame.Rect(position_x, position_y , domino_width, domino_height)
                resized_image = pygame.transform.scale(image, (domino_width, domino_height))
                self.display_surface.blit(resized_image, rect)

    def draw_domino_selected(self):
        if(self.selected != None):
            mouse_position = pygame.mouse.get_pos()
            domino_image = self.selected.get_image()
            image = pygame.image.load(domino_image)
            if(self.selected.dot1 < self.selected.dot2):
                if(self.selected.is_horizontal == False):
                    pass
                else:
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
            else:
                if(self.selected.is_horizontal == False):
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
                else:
                    image = pygame.transform.rotate(image, -90)

            rect = pygame.Rect(mouse_position[0] - self.selected.width//2 , mouse_position[1] - self.selected.height//2, self.selected.width, self.selected.height)
            resized_image = pygame.transform.scale(image, (self.selected.width, self.selected.height))
            self.display_surface.blit(resized_image, rect)

            # try:
            #     image = self.selected.get_image_pg()
            #     # image = pygame.image.load(domino_image)
            #     rect = pygame.Rect(mouse_position[0] - self.selected.width//2 , mouse_position[1] - self.selected.height//2, self.selected.width, self.selected.height)
            #     resized_image = pygame.transform.scale(image, (self.selected.width, self.selected.height))
            #     self.display_surface.blit(resized_image, rect)
            # except pygame.error as e:
            #     print("Error loading image:", e)

    def draw_turn(self):
        if self.turn == True:	
            text = TURN_FONT.render("Turn: Your Turn" , 1,(255,255,255))
            self.display_surface.blit(text,(10,10))
        else:
            text = TURN_FONT.render("Turn: Opponent's" , 1, (255,255,255))
            self.display_surface.blit(text,(10,10))

    def draw_turtorial(self):
        text_r = TURN_FONT.render("Press R to Rotate Domino" , 1,(255,255,255))
        self.display_surface.blit(text_r,(10,600))
        text_q = TURN_FONT.render("Press Q to Give Domino To Hand" , 1,(255,255,255))
        self.display_surface.blit(text_q,(10,650))

    def draw_box_help(self):
        if self.selected != None:
            self.selected.set_position(self.box_help[1], self.box_help[2])
            for i, domino in enumerate(self.board.placed_dominoes):
                if(self.selected.is_overlapping(domino)):
                    self.box_help[0] = False
                    break

            # if self.box_help[2] < self.board.y  or self.box_help[2] + self.selected.height > self.board.y + self.board.height:
            #     self.box_help[0] = False
            #     return
            
            if self.selected.position[1] < self.board.y  or self.selected.position[1] + self.selected.height > self.board.y + self.board.height or self.selected.position[0] + self.selected.width > self.board.x + self.board.width:
                self.box_help[0] = False
                return

        if(self.box_help[0] == True) and self.error ==  False :
            box = pygame.Rect(self.box_help[1] ,self.box_help[2] , self.selected.width, self.selected.height)
            pygame.draw.rect(self.display_surface, (106, 212, 221), box)

        if self.box_help[0] == True and self.error == True:
            box = pygame.Rect(self.box_help[1] , self.box_help[2] , self.selected.width, self.selected.height)
            pygame.draw.rect(self.display_surface, (250, 112, 112), box)

    def event_loop(self, event):
        # print(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()

            if self.selected == None:
                if self.button_position[0] <= mouse_position[0] <= self.button_position[0] + 60 and self.button_position[1] <= mouse_position[1] <= self.button_position[1] + 60:
                    self.toggle_sound()
                
                if self.button_pass_x <= mouse_position[0] <= self.button_pass_x + self.button_pass_width and self.button_pass_y <= mouse_position[1] <= self.button_pass_y + self.button_pass_height:
                    if(self.turn == True):
                        self.turn = False
                        data = "swap"
                        data = pickle.dumps(data)
                        self.connection.send(data)
                # if self.chat_box.x + 5 <= mouse_position[0] <= self.chat_box.x + self.chat_box.width - 10 and self.chat_box.y + 400 - 50 <= mouse_position[1] <= self.chat_box.y + 40:
                #     self.chatting = True
                #     self.chat_box.active = True

        # self.text_input_surface = (self.x + 5, self.y + 400 - 50), (self.width - 10, 40)


            if self.playing == False:
                return

            if self.selected != None:
                self.selected.set_position(self.box_help[1], self.box_help[2])
                for i, domino in enumerate(self.board.placed_dominoes):
                    if(self.selected.is_overlapping(domino)):
                        self.box_help[0] = False
                        break

                if self.selected.position[1] < self.board.y  or self.selected.position[1] + self.selected.height > self.board.y + self.board.height or self.selected.position[0] + self.selected.width > self.board.x + self.board.width:
                    self.box_help[0] = False


            if(self.is_dragging == False and self.selected == None and self.turn == True):
                for i, domino in enumerate(self.hand):  
                    domino_position = domino.position
                    if self.is_mouse_on_domino(mouse_position, domino_position):
                        self.selected = domino
                        self.is_dragging = True  # Bắt đầu dragging
                        self.rotated = 1
                        # data = "pick:" + str(domino) + "-" +  str(i)
                        self.hand.pop(i)
                        break

            elif (self.turn == True):
                if(self.first_play == True and len(self.hand) == 6):
                    domino_x = mouse_position[0] - self.selected.width//2
                    domino_y = mouse_position[1] - self.selected.height//2
                    if self.board.y > domino_y:
                        return
                    elif self.board.y + self.board.height < domino_y + self.selected.height:
                        return
                    elif self.board.x + self.board.width < domino_x + self.selected.width:
                        return

                    self.selected.set_position(domino_x,domino_y)
                    self.is_dragging = False
                    self.selected.set_image_pg(self.selected.get_image()) 
                    self.board.add_first_domino(self.selected)
                    self.selected = None
                    self.turn = False

                    data_to_send = ("put", self.board.placed_dominoes)           
                    data = pickle.dumps(data_to_send)
                    self.connection.send(data)

                elif(self.box_help[0] == True and self.insert_start == True and  self.error  == False):
                    self.box_help[0] = False
                    self.selected.set_position(self.box_help[1], self.box_help[2])  
                    self.selected.set_image_pg(self.selected.get_image()) 
                    self.board.add_domino(self.selected, "start")
                    self.turn = False
                    self.is_dragging = False
                    self.selected = None
                   
                    data_to_send = ("put", self.board.placed_dominoes)           
                    data = pickle.dumps(data_to_send)
                    self.connection.send(data)

                    # if len(self.hand) == 0:
                    #     self.playing = False    
                    #     self.status = "Win"
                    #     self.first_play = False
                    #     data_to_send = ("winner")           
                    #     data = pickle.dumps(data_to_send)
                    #     self.connection.send(data)


                elif(self.box_help[0] == True and self.insert_start == False and  self.error  ==  False):
                    self.box_help[0] = False
                    self.selected.set_position(self.box_help[1], self.box_help[2])
                    self.selected.set_image_pg(self.selected.get_image()) 
                    self.board.add_domino(self.selected, "end")
                    self.turn = False
                    self.is_dragging = False
                    self.selected = None

                    data_to_send = ("put", self.board.placed_dominoes)           
                    data = pickle.dumps(data_to_send)
                    self.connection.send(data)

                    # if len(self.hand) == 0:    
                    #     self.playing = False    
                    #     self.status = "Win"
                    #     self.first_play = False
                    #     data_to_send = ("winner")           
                    #     data = pickle.dumps(data_to_send)
                    #     self.connection.send(data)

        if event.type == pygame.KEYDOWN:
            if self.chatting == True:
                pass
                # if event.key == pygame.K_RETURN:
                #     if self.chat_box.text == '':
                #         self.chat_box.active = False
                #         self.chatting = False
                #     else:
                #         self.chat_box.messages.append(self.username + ':' + self.chat_box.text)
                #         self.chatting = False
                #         self.chat_box.active = False
                #         data_to_send = ("chat", self.username, self.chat_box.text)
                #         data = pickle.dumps(data_to_send)
                #         self.connection.send(data)
                #         self.chat_box.text = ''

                # elif event.key == pygame.K_BACKSPACE:
                #     self.chat_box.text = self.chat_box.text[:-1]
                # else:
                #     self.chat_box.text += event.unicode
            else:
                # if event.key == pygame.K_g:
                #     for i,domino in enumerate(self.hand):
                #         print(str(domino))                if event.key == pygame.K_RETURN and self.play_again == True:


                if event.key == pygame.K_RETURN and self.play_again == True:
                    self.hand = []
                    self.other_player = 0
                    self.board.play_again()
                    self.over = False
                    self.play_again = False
                    self.other_player_hand = []
                    if (self.is_host == True):
                        self.playing = True
                        self.board.create()
                        self.board.shuffle()
                        self.hand = self.board.hand_player()
                        # self.create_image_pg()
                        self.other_player = 7
                        data = ("play-again", self.board.domino_list)
                        if (self.first_play == True):
                            self.turn = True
                        else:
                            self.turn = False
                        data = pickle.dumps(data)
                        self.connection.send(data)

                if event.key == pygame.K_p:
                    if (self.is_dragging == False and self.turn == True):
                        self.turn = False
                        data = "swap"
                        data = pickle.dumps(data)
                        self.connection.send(data)

                if event.key == pygame.K_r:
                    if (self.is_dragging == True):
                        # self.selected.set_image_pg(pygame.transform.rotate(self.selected.get_image_pg(), -90))
                        self.selected.rotated()
                        self.selected.is_horizontal = not self.selected.is_horizontal
                        if self.rotated == 3:
                            self.rotated = 1
                        if self.rotated == 1:
                            self.selected.swap_dot()
                        self.rotated += 1
                        self.box_help[0] = False

                if event.key == pygame.K_q:
                    if self.is_dragging and self.selected.is_horizontal == True:
                        # self.selected.set_image_pg(pygame.transform.rotate(self.selected.get_image_pg(), -90))
                        self.selected.rotated()
                        self.selected.is_horizontal = not self.selected.is_horizontal

                        self.hand.append(self.selected)
                        self.is_dragging = False
                        self.selected = None
                        self.box_help[0] = False
                        data = "drop"
                        # is_dragging = False
                        # selected_domino = None
                    elif self.is_dragging:
                        # domino_image = pygame.image.load(self.selected.get_image())
                        # self.selected.set_image_pg(domino_image)
                        self.hand.append(self.selected)
                        self.is_dragging = False
                        self.selected = None
                        self.box_help[0] = False
                        data = "drop"
        
        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()

            if self.selected == None:
                if self.button_pass_x <= mouse_position[0] <= self.button_pass_x + self.button_pass_width and self.button_pass_y <= mouse_position[1] <= self.button_pass_y + self.button_pass_height:
                    self.button_pass_color = GRAY
                else:
                    self.button_pass_color = GREEN

            if self.selected != None:
                self.selected.set_position(self.box_help[1], self.box_help[2])
                for i, domino in enumerate(self.board.placed_dominoes):
                    if(self.selected.is_overlapping(domino)):
                        self.box_help[0] = False
                        break
                    
                # if self.board.y > self.box_help[2]:
                #     self.box_help[0] = False
                # elif self.board.y + self.board.height > self.box_help[2]:
                #     self.box_help[0] == False


            if self.is_dragging and self.selected.is_horizontal == True:
                #Co 1 domino o tren ban
                if(len(self.board.placed_dominoes) > 0 and len(self.board.placed_dominoes) == 1):
                    domino = self.board.placed_dominoes[0]
                    # value_horizontal = self.selected.check_mouse_link_domino_horizontal(mouse_position, domino)
                    if domino.is_horizontal:
                        value_horizontal = self.selected.check_mouse_link_first_domino_horizontal(mouse_position, domino)
                        if value_horizontal in ["Left", "Right"] :
                            if value_horizontal =="Left":
                                self.box_help[1] = domino.position[0] - self.selected.width
                                self.box_help[2] = domino.position[1]
                                self.left_domino = True
                                self.up_domino = None
                            elif value_horizontal =="Right":
                                self.box_help[1] = domino.position[0] + domino.width
                                self.box_help[2] = domino.position[1] 
                                self.left_domino = False
                                self.up_domino = None 
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_horizontal(domino, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return   
                        else:
                            self.box_help[0] = False
                    elif domino.is_horizontal == False:
                        value_vertical = self.selected.check_mouse_link_first_domino_vertical(mouse_position, self.board.placed_dominoes[0])
                        if value_vertical not in ["Up", "Down", None]:
                            if value_vertical == "Up-Left":
                                self.box_help[1] = domino.position[0] - self.selected.width
                                self.box_help[2] = domino.position[1]
                                self.left_domino = True
                                self.up_domino = True
                            elif value_vertical == "Up-Right":
                                self.box_help[1] = domino.position[0] + domino.width
                                self.box_help[2] = domino.position[1]
                                self.left_domino = False
                                self.up_domino = True
                            elif value_vertical == "Down-Left":
                                self.box_help[1] = domino.position[0] - self.selected.width
                                self.box_help[2] = domino.position[1] + self.selected.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_vertical == "Down-Right":
                                self.box_help[1] = domino.position[0] + domino.width
                                self.box_help[2] = domino.position[1] + self.selected.height
                                self.left_domino = False
                                self.up_domino = False
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(domino, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False 

                elif len(self.board.placed_dominoes) > 0:
                    domino_start = self.board.placed_dominoes[0]
                    domino_end = self.board.placed_dominoes[len(self.board.placed_dominoes)-1]
                    if(domino_start.is_horizontal):
                        value_start_horizontal = self.selected.check_mouse_link_domino_horizontal(mouse_position, domino_start)
                        if value_start_horizontal in ["Left", "Right"] :
                            if value_start_horizontal =="Left":
                                self.box_help[1] = domino_start.position[0] - self.selected.width
                                self.box_help[2] = domino_start.position[1]
                                self.left_domino = True
                                self.up_domino = None
                            elif value_start_horizontal =="Right":
                                self.box_help[1] = domino_start.position[0] + domino_start.width
                                self.box_help[2] = domino_start.position[1] 
                                self.left_domino = False
                                self.up_domino = None 
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_horizontal(domino_start, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return   
                        else:
                            self.box_help[0] = False
                    elif(domino_start.is_horizontal == False):
                        value_start_vertical = self.selected.check_mouse_link_domino_vertical(mouse_position, domino_start)
                        if value_start_vertical not in ["Up", "Down", None]:
                            if value_start_vertical == "Up-Left":
                                self.box_help[1] = domino_start.position[0] - self.selected.width
                                self.box_help[2] = domino_start.position[1]
                                self.left_domino = True
                                self.up_domino = True
                            elif value_start_vertical == "Up-Right":
                                self.box_help[1] = domino_start.position[0] + domino_start.width
                                self.box_help[2] = domino_start.position[1]
                                self.left_domino = False
                                self.up_domino = True
                            elif value_start_vertical == "Down-Left":
                                self.box_help[1] = domino_start.position[0] - self.selected.width
                                self.box_help[2] = domino_start.position[1] + self.selected.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_start_vertical == "Down-Right":
                                self.box_help[1] = domino_start.position[0] + domino_start.width
                                self.box_help[2] = domino_start.position[1] + self.selected.height
                                self.left_domino = False
                                self.up_domino = False
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(domino_start, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False  
                    if(domino_end.is_horizontal):
                        value_end_horizontal = self.selected.check_mouse_link_domino_horizontal(mouse_position, domino_end)
                        if value_end_horizontal in ["Left", "Right"]:

                            if value_end_horizontal =="Left":
                                self.box_help[1] = domino_end.position[0] - self.selected.width
                                self.box_help[2] = domino_end.position[1]
                                self.left_domino = True
                                self.up_domino = None
                            elif value_end_horizontal =="Right":
                                self.box_help[1] = domino_end.position[0] + domino_end.width
                                self.box_help[2] = domino_end.position[1] 
                                self.left_domino = False
                                self.up_domino = None 
                            
                            self.box_help[0] = True  
                            valid = self.selected.check_valid_domino_board_horizontal(domino_end, self.left_domino, self.up_domino)
                            self.insert_start = False
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False                                        
                    elif(domino_end.is_horizontal == False):
                        value_end_vertical = self.selected.check_mouse_link_domino_vertical(mouse_position, domino_end)
                        if value_end_vertical not in ["Up", "Down", None]:
                            if value_end_vertical == "Up-Left":
                                self.box_help[1] = domino_end.position[0] - self.selected.width
                                self.box_help[2] = domino_end.position[1]
                                self.left_domino = True
                                self.up_domino = True
                            elif value_end_vertical == "Up-Right":
                                self.box_help[1] = domino_end.position[0] + domino_end.width
                                self.box_help[2] = domino_end.position[1]
                                self.left_domino = False
                                self.up_domino = True
                            elif value_end_vertical == "Down-Left":
                                self.box_help[1] = domino_end.position[0] - self.selected.width
                                self.box_help[2] = domino_end.position[1] + self.selected.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_end_vertical == "Down-Right":
                                self.box_help[1] = domino_end.position[0] + domino_end.width
                                self.box_help[2] = domino_end.position[1] + self.selected.height
                                self.left_domino = False
                                self.up_domino = False
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(domino_end, self.left_domino, self.up_domino)
                            self.insert_start = False
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False                   
            elif self.is_dragging and self.selected.is_horizontal == False:
                if(len(self.board.placed_dominoes) > 0 and len(self.board.placed_dominoes) == 1):
                    first_domino = self.board.placed_dominoes[0]
                    # value_vertical = self.selected.check_mouse_link_first_domino_vertical(mouse_position, first_domino)
                    if(first_domino.is_horizontal):
                        value_start_horizontal = self.selected.check_mouse_link_first_domino_horizontal(mouse_position, first_domino)
                        if value_start_horizontal not in ["Left", "Right", None]:
                            if value_start_horizontal == "Left-Up":
                                self.box_help[1] = first_domino.position[0]
                                self.box_help[2] = first_domino.position[1] - self.selected.height
                                self.left_domino = True
                                self.up_domino = True
                            elif value_start_horizontal == "Left-Down":
                                self.box_help[1] = first_domino.position[0]
                                self.box_help[2] = first_domino.position[1] + first_domino.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_start_horizontal == "Right-Up":
                                self.box_help[1] = first_domino.position[0] + self.selected.width
                                self.box_help[2] = first_domino.position[1] - self.selected.height
                                self.left_domino = False
                                self.up_domino = True
                            elif value_start_horizontal == "Right-Down":
                                self.box_help[1] = first_domino.position[0] + self.selected.width
                                self.box_help[2] = first_domino.position[1] + first_domino.height
                                self.left_domino = False
                                self.up_domino = False
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_horizontal(first_domino, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False                                 
                        
                    elif(first_domino.is_horizontal == False):
                        value_start_vertical = self.selected.check_mouse_link_first_domino_vertical(mouse_position, first_domino)
                        if value_start_vertical in ["Up", "Down"]:
                            if value_start_vertical =="Up":
                                self.box_help[1] = first_domino.position[0] 
                                self.box_help[2] = first_domino.position[1] - first_domino.height
                                self.left_domino = None
                                self.up_domino = True
                            elif value_start_vertical =="Down":
                                self.box_help[1] = first_domino.position[0]
                                self.box_help[2] = first_domino.position[1] + first_domino.height
                                self.left_domino = None
                                self.up_domino = False 
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(first_domino, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False

                elif len(self.board.placed_dominoes) > 0:
                    domino_start = self.board.placed_dominoes[0]
                    domino_end = self.board.placed_dominoes[len(self.board.placed_dominoes)-1]

                    if(domino_start.is_horizontal):
                        value_start_horizontal = self.selected.check_mouse_link_domino_horizontal(mouse_position, domino_start)
                        if value_start_horizontal not in ["Left", "Right", None]:
                            if value_start_horizontal == "Left-Up":
                                self.box_help[1] = domino_start.position[0]
                                self.box_help[2] = domino_start.position[1] - self.selected.height
                                self.left_domino = True
                                self.up_domino = True
                            elif value_start_horizontal == "Left-Down":
                                self.box_help[1] = domino_start.position[0]
                                self.box_help[2] = domino_start.position[1] + domino_start.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_start_horizontal == "Right-Up":
                                self.box_help[1] = domino_start.position[0] + self.selected.width
                                self.box_help[2] = domino_start.position[1] - self.selected.height
                                self.left_domino = False
                                self.up_domino = True
                            elif value_start_horizontal == "Right-Down":
                                self.box_help[1] = domino_start.position[0] + self.selected.width
                                self.box_help[2] = domino_start.position[1] + domino_start.height
                                self.left_domino = False
                                self.up_domino = False
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_horizontal(domino_start, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False                                 
                        
                    elif(domino_start.is_horizontal == False):
                        value_start_vertical = self.selected.check_mouse_link_domino_vertical(mouse_position, domino_start)
                        if value_start_vertical in ["Up", "Down"]:
                            if value_start_vertical =="Up":
                                self.box_help[1] = domino_start.position[0] 
                                self.box_help[2] = domino_start.position[1] - domino_start.height
                                self.left_domino = None
                                self.up_domino = True
                            elif value_start_vertical =="Down":
                                self.box_help[1] = domino_start.position[0]
                                self.box_help[2] = domino_start.position[1] + domino_start.height
                                self.left_domino = None
                                self.up_domino = False 
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(domino_start, self.left_domino, self.up_domino)
                            self.insert_start = True
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False

                    if(domino_end.is_horizontal):
                        value_end_horizontal = self.selected.check_mouse_link_domino_horizontal(mouse_position, domino_end)
                        if value_end_horizontal not in ["Left", "Right", None]:
                            if value_end_horizontal == "Left-Up":
                                self.box_help[1] = domino_end.position[0]
                                self.box_help[2] = domino_end.position[1] - self.selected.height
                                self.left_domino = True
                                self.up_domino = True
                            elif value_end_horizontal == "Left-Down":
                                self.box_help[1] = domino_end.position[0]
                                self.box_help[2] = domino_end.position[1] + domino_end.height
                                self.left_domino = True
                                self.up_domino = False
                            elif value_end_horizontal == "Right-Up":
                                self.box_help[1] = domino_end.position[0] + self.selected.width
                                self.box_help[2] = domino_end.position[1] - self.selected.height
                                self.left_domino = False
                                self.up_domino = True
                            elif value_end_horizontal == "Right-Down":
                                self.box_help[1] = domino_end.position[0] + self.selected.width
                                self.box_help[2] = domino_end.position[1] + domino_end.height
                                self.left_domino = False
                                self.up_domino = False
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_horizontal(domino_end, self.left_domino, self.up_domino)
                            self.insert_start = False
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False                          
                        
                    elif(domino_end.is_horizontal == False):
                        value_end_vertical = self.selected.check_mouse_link_domino_vertical(mouse_position, domino_end)
                        if value_end_vertical in ["Up", "Down"]:
                            if value_end_vertical =="Up":
                                self.box_help[1] = domino_end.position[0] 
                                self.box_help[2] = domino_end.position[1] - domino_end.height
                                self.left_domino = None
                                self.up_domino = True
                            elif value_end_vertical =="Down":
                                self.box_help[1] = domino_end.position[0]
                                self.box_help[2] = domino_end.position[1] + self.selected.height
                                self.left_domino = None
                                self.up_domino = False  
                            
                            self.box_help[0] = True
                            valid = self.selected.check_valid_domino_board_vertical(domino_end, self.left_domino, self.up_domino)
                            self.insert_start = False
                            if(valid == True):
                                self.error  = False
                            else:
                                self.error  = True
                            return
                        else:
                            self.box_help[0] = False  

        if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#main_text_entry'):
            # self.chat_box.messages.append(self.username + ':' + event.text)
            if event.text != '':
                self.chat_box.box_message.append_html_text(f"<p>{self.username}:{event.text}</p>")
                # self.chatting = False
                # self.chat_box.active = False
                data_to_send = ("chat", self.username, event.text)
                data = pickle.dumps(data_to_send)
                self.connection.send(data)
                self.chat_box.text_input.clear()

        if self.selected != None:
            return
        manager.process_events(event)

    def is_mouse_on_domino(self, mouse_position, domino_position):
        if mouse_position[0] > domino_position[0]\
            and mouse_position[0] < (domino_position[0] + 48)\
            and mouse_position[1] > domino_position[1]\
            and mouse_position[1] < (domino_position[1] + 96) :
            return True
        else :
            return False


    def get_player_hand(self):
        hand_player = []
        for domino in self.hand:
            hand_player.append(domino)
            
        for domino in hand_player:
            domino.set_image_pg(domino.get_image())
                
        return hand_player

    def switch_turn(self):
        self.turn = True

    def create_image_pg(self):
        for domino in self.hand:
            domino_image = pygame.image.load(domino.get_image())
            domino.set_image_pg(domino_image)

    def motion_horizontal_domino_fisrt(self, domino):
        self.box_help[0] = True
        valid = self.selected.check_valid_domino(domino, self.left_domino)
        if(valid == True):
            self.error  = False
        else:
            self.error  = True
        self.box_help[2] = domino.position[1]

class Board:
    def __init__(self, surface = None):
        self.domino_list = []
        self.placed_dominoes = []  # Danh sách domino đã đặt
        self.surface = surface
        self.width = W - 200
        self.height = 400
        self.x = 0
        self.y = (H - self.height)//2
    
    def __str__(self):
        return f"{self.domino_list.__str__}"

    def add_first_domino(self, domino):
        self.placed_dominoes.append(domino)

    def create(self):
        for i in range(7):
            for j in range(i, 7):
                image_path = f"assets/Domino{i}{j}.png"
                domino_new = Domino(i,j,image_path)
                self.domino_list.append(domino_new)

    def play_again(self):
        self.domino_list = []
        self.placed_dominoes = []

    def shuffle(self):
        random.shuffle(self.domino_list)

    def hand_player(self):
        hand = []
        for i in range(7):
            hand.append(self.domino_list.pop())
        return hand

    def add_domino(self, domino, position):
        if(position == "start"):
            link = self.update_link_domino(self.placed_dominoes[0] ,domino)
            self.placed_dominoes[0].link = link[0]
            domino.link = link[1]
            self.placed_dominoes.insert(0, domino)
            
        elif(position == "end"):
            link = self.update_link_domino(self.placed_dominoes[len(self.placed_dominoes)-1] ,domino)
            self.placed_dominoes[len(self.placed_dominoes)-1].link  = link[0]
            domino.link = link[1]
            self.placed_dominoes.append(domino)

    def update_link_domino(self, domino_board, domino):
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

    def draw_board(self):
        for i, domino in enumerate(self.placed_dominoes):
            domino_image = domino.get_image()
            image = pygame.image.load(domino_image)

            if(domino.dot1 < domino.dot2):
                if(domino.is_horizontal == False):
                    pass
                else:
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
            else:
                if(domino.is_horizontal == False):
                    image = pygame.transform.rotate(image, -90)
                    image = pygame.transform.rotate(image, -90)
                else:
                    image = pygame.transform.rotate(image, -90)

            rect = pygame.Rect(domino.position[0], domino.position[1], domino.width, domino.height)
            resized_image = pygame.transform.scale(image, (domino.width, domino.height))

            self.surface.blit(resized_image, rect)

class ChatBox:
    def __init__(self, surface = None):
        self.messages = []
        self.surface = surface
        self.width = 200
        self.height = 400
        self.x = W - 210
        self.y = (H - 400) // 2
        self.active = False
        self.text = ''
        self.txt_surface =  text_font.render(self.text, True, WHITE)
        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pygame.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))

        self.text_input_surface = (self.x + 5, self.y + 400 - 50), (self.width - 10, 40)
        self.text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(self.text_input_surface), manager=manager,
                                               object_id= '#main_text_entry')


        self.box_message = pygame_gui.elements.UITextBox("", relative_rect=pygame.Rect((self.x + 5,self.y + 5), (self.width - 10,self.height - 60)),manager=manager, object_id='#box_message', allow_split_dashes =False)


    def draw_chat_box(self):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Kích thước khung chat
        chat_box_width = 200
        chat_box_height = 400
        chat_box_x = (W - chat_box_width - 10)
        chat_box_y = (H - chat_box_height) // 2

        text_surface = font.render(user_text,True,(255,255,255))
        input_box_width = chat_box_width - 20
        input_box_height = 40
        input_box_x = chat_box_x + 10
        input_box_y = chat_box_y + chat_box_height - input_box_height - 20

        # self.surface.blit(text_surface,(input_box_x + 5,input_box_y + 10))
        # self.surface.blit(self.txt_surface,(input_box_x + 5,input_box_y + 10))

        # self.txt_surface = text_font.render(self.text, True, WHITE)
        # if time.time() % 1 > 0.5 and self.active:

        #     # bounding rectangle of the text
        #     text_rect = self.txt_surface.get_rect(topleft = (input_box_x + 5, input_box_y + 10))

        #     # set cursor position
        #     self.cursor.midleft = text_rect.midright

        #     pygame.draw.rect(self.surface, WHITE, self.cursor)
        

        # Vẽ khung chat
        pygame.draw.rect(self.surface, BLACK, (chat_box_x, chat_box_y, chat_box_width, chat_box_height), 2)

        # input_rect = pygame.draw.rect(self.surface, BLACK, (input_box_x, input_box_y, input_box_width, input_box_height), 2)
        # input_rect.w = max(100, text_surface.get_width() + 10)
        UI_REFRESH_RATE = clock.tick(60)/1000

        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(self.surface)
        pygame.display.flip()

    def draw_message(self):
        chat_box_width = 200
        chat_box_height = 400
        chat_box_x = (W - chat_box_width - 10)
        chat_box_y = (H - chat_box_height) // 2

        self.formatted_messages = []
        for message in self.messages:
            if len(message) > 20:
                parts = [message[i:i + 20] for i in range(0, len(message), 20)]
                self.formatted_messages.extend(parts)
            else:
                self.formatted_messages.append(message)

        for i, message in enumerate(self.formatted_messages):
            message_surface = font.render(message, True, WHITE)
            message_rect = message_surface.get_rect()
            message_rect.topleft = (chat_box_x + 10, chat_box_y + 10 + i * 20)
            self.surface.blit(message_surface, message_rect.topleft)


class Domino:
    def __init__(self, dot1, dot2,  image , position = [0, 0], link = 0, is_horizontal = False ,width = 48, height = 96 ):
        self.dot1 = dot1
        self.dot2 = dot2
        self.width = width
        self.height = height
        self.image = image
        self.image_pg = image
        self.position = position
        self.is_horizontal = is_horizontal
        self.link = link

    # def __str__(self):
    #     return f"{self.dot1}-{self.dot2}-{self.image}-{self.position[0]}-{self.position[1]}-{self.link}-{self.is_horizontal}-{self.width}-{self.height}"

    def __str__(self):
        return f"{self.image}-{self.image_pg}"

    def get_link(self):
        return self.link

    def set_position(self, x, y):
        self.position = [x,y]

    def get_position(self):
        return self.position
    
    def rotated(self):
        z = self.width
        self.width = self.height
        self.height = z

    def swap_dot(self):
        d = self.dot1
        self.dot1 = self.dot2
        self.dot2 = d
        

    def get_dot_counts(self):
        return self.dot1, self.dot2

    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image
    
    def set_image_pg(self, image_pg):
        self.image_pg = image_pg

    def get_image_pg(self):
        return self.image_pg
    
    def is_mouse_link_domino_left(self, mouse_position):
        if mouse_position[0] > (self.position[0] - self.width ) \
            and mouse_position[0] < (self.position[0])\
            and mouse_position[1] > (self.position[1] )\
            and mouse_position[1] < (self.position[1] + self.height) :
            return True
        else :
            return False

    def is_mouse_link_domino_right(self, mouse_position):
        if mouse_position[0] > (self.position[0] +  self.width) \
            and mouse_position[0] < (self.position[0] +  self.width +  self.width)\
            and mouse_position[1] > self.position[1]\
            and mouse_position[1] < (self.position[1] + self.height) :
            return True
        else :
            return False
        
    def check_valid_domino(self, domino_board, left, up=None):
        if(left and up==False):
            if(self.dot1 == domino_board.dot1):
                return True
        elif(left == False and up == False):
            if(self.dot1 == domino_board.dot2):
                return True
        elif(left == False and up):
            if(self.dot2 == domino_board.dot2):
                return True
        elif(left):
            if(self.dot2 == domino_board.dot1):
                return True
        elif left == False:
            if(self.dot1 == domino_board.dot2):
                return True
        return False
    
    def check_mouse_link_first_domino_horizontal(self, mouse_position, domino):
        if mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1]):
            return "Left-Up"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] + domino.height)\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height):
            return "Left-Down"
        elif mouse_position[0] > (domino.position[0] + self.width) \
            and mouse_position[0] < (domino.position[0] + self.width * 2)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1]):
            return "Right-Up"
        elif mouse_position[0] > (domino.position[0] + self.width) \
            and mouse_position[0] < (domino.position[0] + self.width * 2)\
            and mouse_position[1] > (domino.position[1] + domino.height)\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height):
            return "Right-Down"
        elif mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height):
            return "Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0] + domino.width + self.width)\
            and mouse_position[1] > (domino.position[1] )\
            and mouse_position[1] < (domino.position[1] + self.height ):
            return "Right"
        
    def check_mouse_link_first_domino_vertical(self, mouse_position, domino):
        if mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height):
            return "Up-Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0] + domino.width + self.width)\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height):
            return "Up-Right"
        elif mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1] + self.height )\
            and mouse_position[1] < (domino.position[1] + self.height * 2):
            return "Down-Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0]+ domino.width + self.width)\
            and mouse_position[1] > (domino.position[1] + self.height )\
            and mouse_position[1] < (domino.position[1] + self.height * 2):
            return "Down-Right"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1]):
            return "Up"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0]+ self.width)\
            and mouse_position[1] > (domino.position[1] +domino.height )\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height ):
            return "Down"
    
    def check_mouse_link_domino_horizontal(self, mouse_position, domino):
        if mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1])\
            and domino.link == 2:
            return "Left-Up"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] + domino.height)\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height)\
            and domino.link == 2 :
            return "Left-Down"
        elif mouse_position[0] > (domino.position[0] + self.width) \
            and mouse_position[0] < (domino.position[0] + self.width * 2)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1])\
            and domino.link == 1 :
            return "Right-Up"
        elif mouse_position[0] > (domino.position[0] + self.width) \
            and mouse_position[0] < (domino.position[0] + self.width * 2)\
            and mouse_position[1] > (domino.position[1] + domino.height)\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height)\
            and domino.link == 1 :
            return "Right-Down"
        elif mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height)\
            and domino.link == 2 :
            return "Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0] + domino.width + self.width)\
            and mouse_position[1] > (domino.position[1] )\
            and mouse_position[1] < (domino.position[1] + self.height )\
            and domino.link == 1 :
            return "Right"
        
    def check_mouse_link_domino_vertical(self, mouse_position, domino):
        if mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height)\
            and domino.link == 2:
            return "Up-Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0] + domino.width + self.width)\
            and mouse_position[1] > (domino.position[1])\
            and mouse_position[1] < (domino.position[1] + self.height)\
            and domino.link == 2 :
            return "Up-Right"
        elif mouse_position[0] > (domino.position[0] - self.width) \
            and mouse_position[0] < (domino.position[0])\
            and mouse_position[1] > (domino.position[1] + self.height )\
            and mouse_position[1] < (domino.position[1] + self.height * 2)\
            and domino.link == 1 :
            return "Down-Left"
        elif mouse_position[0] > (domino.position[0] + domino.width) \
            and mouse_position[0] < (domino.position[0]+ domino.width + self.width)\
            and mouse_position[1] > (domino.position[1] + self.height )\
            and mouse_position[1] < (domino.position[1] + self.height * 2)\
            and domino.link == 1 :
            return "Down-Right"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0] + self.width)\
            and mouse_position[1] > (domino.position[1] - self.height)\
            and mouse_position[1] < (domino.position[1])\
            and domino.link == 2 :
            return "Up"
        elif mouse_position[0] > (domino.position[0]) \
            and mouse_position[0] < (domino.position[0]+ self.width)\
            and mouse_position[1] > (domino.position[1] +domino.height )\
            and mouse_position[1] < (domino.position[1] + domino.height + self.height )\
            and domino.link == 1 :
            return "Down"
        
    def check_valid_domino_board_horizontal(self, domino_board , left, up = None):
        if(left):
            if(up == False and self.dot1 == domino_board.dot1):
                return True  
            elif(up == True and self.dot2 == domino_board.dot1):
                return True
            elif(up == None and self.dot2 == domino_board.dot1):
                return True
            
        elif(left == False):
            if(up and self.dot2 == domino_board.dot2):
                return True
            elif(up == False and self.dot1 == domino_board.dot2):
                return True
            elif(up == None and self.dot1 == domino_board.dot2):
                return True
        return False

    def check_valid_domino_board_vertical(self, domino_board, left = None, up = None):
        if(up):
            if(left == False and self.dot1 == domino_board.dot1):
                return True
            elif(left==True and self.dot2 == domino_board.dot1):
                return True
            elif(left == None and self.dot2 == domino_board.dot1):
                return True
        elif(up == False):
            if(left == True and self.dot2 == domino_board.dot2):
                return True
            elif(left == False and self.dot1 == domino_board.dot2):
                return True
            elif(left == None and self.dot1 == domino_board.dot2):
                return True
        return False
    
    def check_continue_game_first_domino(self, first_domino):
        if (first_domino.dot1 == self.dot1)\
            or (first_domino.dot1 == self.dot2)\
            or first_domino.dot2 == self.dot1\
            or first_domino.dot2 == self.dot2:
            return True
        return False
           

    def check_continue_game(self, domino_start, domino_end):
        if domino_start.link == 1:
            if self.dot1 == domino_start.dot2 or self.dot2 == domino_start.dot2:
                return True
        elif domino_start.link == 2:
            if self.dot1 == domino_start.dot1 or self.dot2 == domino_start.dot1:
                return True
        if domino_end.link == 1:
            if self.dot1 == domino_end.dot2 or self.dot2 == domino_end.dot2:
                return True
        elif domino_end.link == 2:
            if self.dot1 == domino_end.dot1 or self.dot2 == domino_end.dot1:
                return True
        return False
    
    def is_overlapping(self, domino):
    # Kiểm tra xem hai domino có chồng lên nhau không
        if (self.position[0] + self.width > domino.position[0] and
                self.position[0] < domino.position[0] + domino.width and
                self.position[1] + self.height > domino.position[1] and
                self.position[1] < domino.position[1] + domino.height):
            return True
        return False


