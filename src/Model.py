import pygame
import random
pygame.font.init()
import _pickle as pickle


W, H = 1400, 720
TURN_FONT = pygame.font.SysFont("comicsans", 30)

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
        self.rotated = 1
        self.left_domino = False
        self.up_domino = False
        self.over = False
        self.domino_score = 0
        self.score = 0
        self.play_again = False
        self.first_play = False

    def play(self):
        # self.check_continue_player()
        self.draw_screen()
        self.draw_domino()
        self.draw_other_player()
        self.board.draw_board()
        self.draw_box_help()
        self.draw_domino_selected()
        self.draw_turn()
        self.draw_score()

    def get_domino_score(self):
        domino_score = 0
        for i, domino in enumerate(self.hand):
            domino_score += domino.dot1 + domino.dot2
        return domino_score

    def draw_score(self):
        text = TURN_FONT.render("Score: " + str(self.score) , 1,(255,255,255))
        self.display_surface.blit(text,(20, 60))
    
    def check_continue_player(self):
        if len(self.board.placed_dominoes) > 1:
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
                data_to_send = ("over", domino_score)           
                data = pickle.dumps(data_to_send)
                self.connection.send(data)

        # if(self.over == True):
        #     data_to_send = ("over")           
        #     data = pickle.dumps(data_to_send)
        #     self.connection.send(data)    

    def draw_screen(self):
        self.display_surface.fill((210, 107, 3))

        rect_width = W  # Chiều rộng của hình chữ nhật bằng với chiều rộng của cửa sổ đồ họa
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
        for j in range (self.other_player):
            domino_image = f"assets\\Domino.png"
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
            image = self.selected.get_image_pg()
            # image = pygame.image.load(domino_image)
            rect = pygame.Rect(mouse_position[0] - self.selected.width//2 , mouse_position[1] - self.selected.height//2, self.selected.width, self.selected.height)
            resized_image = pygame.transform.scale(image, (self.selected.width, self.selected.height))
            self.display_surface.blit(resized_image, rect)

    def draw_turn(self):
        if self.turn == True:	
            text = TURN_FONT.render("Turn: Your Turn" , 1,(255,255,255))
            self.display_surface.blit(text,(10,10))
        else:
            text = TURN_FONT.render("Turn: Opponent's" , 1, (255,255,255))
            self.display_surface.blit(text,(10,10))

    def draw_box_help(self):
        if self.selected != None:
            self.selected.set_position(self.box_help[1], self.box_help[2])
            for i, domino in enumerate(self.board.placed_dominoes):
                if(self.selected.is_overlapping(domino)):
                    self.box_help[0] = False
                    break

        if self.board.y > self.box_help[2]:
            self.box_help[0] = False
        elif self.board.y + self.board.height > self.box_help[2]:
            self.box_help[0] == False

        if(self.box_help[0] == True) and self.error ==  False :
            box = pygame.Rect(self.box_help[1] ,self.box_help[2] , self.selected.width, self.selected.height)
            pygame.draw.rect(self.display_surface, (106, 212, 221), box)

        if self.box_help[0] == True and self.error == True:
            box = pygame.Rect(self.box_help[1] , self.box_help[2] , self.selected.width, self.selected.height)
            pygame.draw.rect(self.display_surface, (250, 112, 112), box)

    def event_loop(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.selected != None:
                self.selected.set_position(self.box_help[1], self.box_help[2])
                for i, domino in enumerate(self.board.placed_dominoes):
                    if(self.selected.is_overlapping(domino)):
                        self.box_help[0] = False
                        break
                    
            if self.board.y > self.box_help[2]:
                self.box_help[0] = False
            elif self.board.y + self.board.height > self.box_help[2]:
                self.box_help[0] == False

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
                if(self.is_host == True and len(self.hand) == 6 and self.selected.is_horizontal):
                    domino_x = mouse_position[0] - self.selected.width//2
                    domino_y = mouse_position[1] - self.selected.height//2
                    if self.board.y > domino_y:
                        return
                    elif self.board.y + self.board.height < domino_y:
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

                    if len(self.hand) == 0:    
                        data_to_send = ("winner")           
                        data = pickle.dumps(data_to_send)
                        self.connection.send(data)


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

                    if len(self.hand) == 0:    
                        data_to_send = ("winner")           
                        data = pickle.dumps(data_to_send)
                        self.connection.send(data)

        if event.type == pygame.KEYDOWN:	
            if event.key == pygame.K_RETURN and self.play_again == True:
                self.hand = []
                self.other_player = 0
                self.board.play_again()
                self.over = False
                self.play_again = False
                if(self.is_host == True):
                    self.board.create()
                    self.board.shuffle()
                    self.hand = self.board.hand_player()
                    self.create_image_pg()
                    self.other_player = 7
                    data = ("play-again", self.board.domino_list)
                    self.turn = True
                    data = pickle.dumps(data)
                    self.connection.send(data)

            if event.key == pygame.K_p:
                if(self.is_dragging == False and self.turn == True):
                    self.turn = False
                    data = "swap"
                    data = pickle.dumps(data)
                    self.connection.send(data)

            if event.key == pygame.K_r:
                if(self.is_dragging == True):
                    self.selected.set_image_pg(pygame.transform.rotate(self.selected.get_image_pg(), -90))
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
                    self.selected.set_image_pg(pygame.transform.rotate(self.selected.get_image_pg(), -90))
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
            if self.is_dragging and self.selected.is_horizontal == True:
                #Co 1 domino o tren ban
                if(len(self.board.placed_dominoes) > 0 and len(self.board.placed_dominoes) == 1):
                    domino = self.board.placed_dominoes[0]
                    if domino.is_horizontal == True:
                        if domino.is_mouse_link_domino_left(mouse_position):
                            self.left_domino = True
                            self.box_help[1] = domino.position[0] - self.selected.width
                            self.insert_start = True
                            self.motion_horizontal_domino_fisrt(domino)
                        if domino.is_mouse_link_domino_right(mouse_position):
                            self.left_domino = False
                            self.box_help[1] = domino.position[0] + self.selected.width
                            self.insert_start = False
                            self.motion_horizontal_domino_fisrt(domino)
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
                    pass
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
                        # print(domino_end.get_dot_counts(), value_end_horizontal)
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

    def is_mouse_on_domino(self, mouse_position, domino_position):
        if mouse_position[0] > domino_position[0]\
            and mouse_position[0] < (domino_position[0] + 48)\
            and mouse_position[1] > domino_position[1]\
            and mouse_position[1] < (domino_position[1] + 96) :
            return True
        else :
            return False

    def place_domino(self, board, domino):
    # Xử lý đặt domino lên bảng (chưa thực hiện)
        pass

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
        self.width = W
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
                image_path = f"assets\\Domino{i}{j}.png"
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

    def __str__(self):
        return f"{self.dot1}-{self.dot2}-{self.image}-{self.position[0]}-{self.position[1]}-{self.link}-{self.is_horizontal}-{self.width}-{self.height}"

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