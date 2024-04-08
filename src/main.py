import pygame
import random
from Domino import Domino  # Giả sử bạn đã tạo các lớp này
from Player import Player
from PIL import Image


# Khởi tạo Pygame
pygame.init()
# Cài đặt màn hình
screen_width = 1400
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Domino")

dominoList = []
board = []
hand_player = []

player1 = Player("Thịnh")

domino_width = 48
domino_height = 96

for i in range(7):
    for j in range(i, 7):
        image_path = f"..\\assets\Domino{i}{j}.png"
        domino_image = pygame.image.load(image_path)
        domino_new = Domino( i,j,domino_image)
        dominoList.append(domino_new)

random.shuffle(dominoList)

for i in range (14):
    domino = dominoList.pop(0)
    hand_player.append(domino)

# player = Player("Thịnh", hand_player)
player1.hand = hand_player

box_x = 0
box_y = 0

# def is_mouse_on_domino(i, mouse_x, mouse_y):
#     domino_rect = pygame.Rect(i * 80, screen_height - domino_height, domino_width, domino_height)
    # return domino_rect.collidepoint(mouse_x, mouse_y)

def is_mouse_on_domino(mouse_position, domino_position):
    if mouse_position[0] > domino_position[0]\
        and mouse_position[0] < (domino_position[0] + 48)\
        and mouse_position[1] > domino_position[1]\
        and mouse_position[1] < (domino_position[1] + 96) :
        return True
    else :
        return False


def is_mouse_link_domino_left(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] - domino.width ) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + domino.height) :
        return True
    else :
        return False

def is_mouse_link_domino_left_up(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] ) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1]) :
        return True
    else :
        return False

def is_mouse_link_domino_left_down(mouse_position, domino):
    if mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0]+ player1.selected.width)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height) :
        return True
    else :
        return False
    # domino_rect = pygame.Rect(domino[1] - 96, domino[2], domino[3], domino[4])
    # return domino_rect.collidepoint(mouse_x, mouse_y)

def is_mouse_link_domino_right(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] +  domino.width) \
        and mouse_position[0] < (domino.position[0] +  domino.width +  domino.width)\
        and mouse_position[1] > domino.position[1]\
        and mouse_position[1] < (domino.position[1] + domino.height) :
        return True
    else :
        return False
    # domino_rect = pygame.Rect(domino[1] + 96 , domino[2], domino[3], domino[4])
    # return domino_rect.collidepoint(mouse_x, mouse_y)

def is_mouse_link_domino_right_up(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1]) :
        return True
    else :
        return False

def is_mouse_link_domino_right_down(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0]+ player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height) :
        return True
    else :
        return False


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

def check_valid_domino(domino_board, domino, left, up=None):
    if(left and up==False):
        if(domino.dot1 == domino_board.dot1):
            return True
    elif(left == False and up == False):
        if(domino.dot1 == domino_board.dot2):
            return True
    elif(left == False and up):
        if(domino.dot2 == domino_board.dot2):
            return True
    elif(left):
        if(domino.dot2 == domino_board.dot1):
            return True
    elif left == False:
        if(domino.dot1 == domino_board.dot2):
            return True
    return False

def check_valid_domino_board_horizontal(domino_board, domino, left, up = None):
    if(left):
        if(up == False and domino.dot1 == domino_board.dot1):
            return True  
        elif(up == True and domino.dot2 == domino_board.dot1):
            return True
        elif(up == None and domino.dot2 == domino_board.dot1):
            return True
        
    elif(left == False):
        if(up and domino.dot2 == domino_board.dot2):
            return True
        elif(up == False and domino.dot1 == domino_board.dot2):
            return True
        elif(up == None and domino.dot1 == domino_board.dot2):
            return True
    return False

def check_valid_domino_board_vertical(domino_board, domino, left = None, up = None):
    if(up):
        if(left == False and domino.dot1 == domino_board.dot1):
            return True
        elif(left==True and domino.dot2 == domino_board.dot1):
            return True
        elif(left == None and domino.dot2 == domino_board.dot1):
            return True
    elif(up == False):
        if(left == True and domino.dot2 == domino_board.dot2):
            return True
        elif(left == False and domino.dot1 == domino_board.dot2):
            return True
        elif(left == None and domino.dot1 == domino_board.dot2):
            return True
    return False


def check_mouse_link_domino(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] ) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1]) :
        return "Left-Up"
    elif mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1]) :
        return "Right-Up"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0]+ player1.selected.width)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height) :
        return "Left-Down"
    elif mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0]+ player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height) :
        return "Right-Down"
    
def check_mouse_link_domino_horizontal(mouse_position, domino):
    if mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link[0] == 2:
        return "Left-Up"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] + domino.height)\
        and mouse_position[1] < (domino.position[1] + domino.height + player1.selected.height)\
        and domino.link[0] == 2 :
        return "Left-Down"
    elif mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0] + + player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link[0] == 1 :
        return "Right-Up"
    elif mouse_position[0] > (domino.position[0] + player1.selected.width) \
        and mouse_position[0] < (domino.position[0] + + player1.selected.width * 2)\
        and mouse_position[1] > (domino.position[1] + domino.height)\
        and mouse_position[1] < (domino.position[1] + domino.height + player1.selected.height)\
        and domino.link[0] == 1 :
        return "Right-Down"
    elif mouse_position[0] > (domino.position[0] - player1.selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + player1.selected.height)\
        and domino.link[0] == 2 :
        return "Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0] + domino.width + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height )\
        and domino.link[0] == 1 :
        return "Right"
    
def check_mouse_link_domino_vertical(mouse_position, domino):
    if mouse_position[0] > (domino.position[0] - player1.selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + player1.selected.height)\
        and domino.link[0] == 2:
        return "Up-Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0] + domino.width + player1.selected.width)\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + player1.selected.height)\
        and domino.link[0] == 2 :
        return "Up-Right"
    elif mouse_position[0] > (domino.position[0] - player1.selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1] + + player1.selected.height )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height * 2)\
        and domino.link[0] == 1 :
        return "Down-Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0]+ domino.width +  player1.selected.width)\
        and mouse_position[1] > (domino.position[1] + player1.selected.height )\
        and mouse_position[1] < (domino.position[1] + player1.selected.height * 2)\
        and domino.link[0] == 1 :
        return "Down-Right"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + player1.selected.width)\
        and mouse_position[1] > (domino.position[1] - player1.selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link[0] == 2 :
        return "Up"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0]+ player1.selected.width)\
        and mouse_position[1] > (domino.position[1] +domino.height )\
        and mouse_position[1] < (domino.position[1] + domino.height + player1.selected.height )\
        and domino.link[0] == 1 :
        return "Down"

drop_domino = None
selected_domino = domino
selected_domino_width = domino_width
selected_domino_height = domino_height
rotated = 1
is_dragging = False 
game_over = False
show_square = False
error_sq = False
start_game = True
# Khởi tạo màu sắc

square_color = (106, 212, 221) # Xanh lam
error_sq_color = (250, 112, 112)
square_border_color = (255, 255, 255)  # Trắng
square_size = 47  # Kích thước hình vuông
left_domino = False
up_domino = None
start_domino = None

# Vòng lặp chính
while not game_over:
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if(is_dragging == False):
                for i, domino in enumerate(player1.hand):
                    if is_mouse_on_domino(mouse_position, domino.get_position()):
                        rotated = 1
                        player1.selected = domino
                        is_dragging = True  # Bắt đầu dragging
                        player1.hand.remove(domino)
                        break
            else:
                if(start_game == True):
                    # board.insert(0, [selected_domino, selected_domino_width, selected_domino_height, mouse_x, mouse_y])
                    domino_x = mouse_position[0] - player1.selected.width//2
                    domino_y = mouse_position[1] - player1.selected.height//2
                    player1.selected.set_position(domino_x,domino_y)
                    board.append(player1.selected)
                    is_dragging = False
                    start_game = False
                    player1.selected = None
                    
                    selected_domino_width = domino_width
                    selected_domino_height = domino_height

                elif (show_square == True and start_domino == True and error_sq == False):
                    show_square = False
                    player1.selected.set_position(box_x,box_y)  
                    link = update_link_domino(board[0] ,player1.selected)
                    board[0].link.append(link[0])
                    player1.selected.link.append(link[1])
                    # board.insert(0, [selected_domino, box_x, box_y, 96, square_size])
                    board.insert(0, player1.selected)
                    is_dragging = False
                    player1.selected = None

                    selected_domino_width = domino_width
                    selected_domino_height = domino_height
                
                elif show_square == True and start_domino == False and error_sq == False: 
                    show_square = False
                    player1.selected.set_position(box_x,box_y)
                    link = update_link_domino(board[len(board)-1] ,player1.selected)
                    board[len(board)-1].link.append(link[0])
                    player1.selected.link.append(link[1])
                    # board.append([selected_domino, box_x, box_y, 96, square_size])
                    board.append(player1.selected)
                    is_dragging = False
                    player1.selected = None

                    selected_domino_width = domino_width
                    selected_domino_height = domino_height

        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            if is_dragging and player1.selected.is_horizontal == True:
                if(len(board) > 0):
                    if(len(board) == 1):
                        domino = board[0]
                        if domino.is_horizontal == True:
                            if is_mouse_link_domino_left(mouse_position, domino):
                                show_square = True
                                left_domino = True
                                start_domino = True
                                valid = check_valid_domino(domino, player1.selected, left_domino)
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                box_x = domino.position[0] - player1.selected.width
                                box_y = domino.position[1]

                            elif is_mouse_link_domino_right(mouse_position, domino):
                                show_square = True
                                left_domino = False
                                start_domino = False
                                valid = check_valid_domino(domino, player1.selected, left_domino)
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True

                                box_x = domino.position[0] + domino.width
                                box_y = domino.position[1]
                            else:
                                show_square = False 
                        elif domino.is_horizontal == False:
                            check_mouse_link_domino_vertical(mouse_position, domino)
                            check_valid_domino_board_vertical(domino, player1.selected,)
                    else:     
                        domino_start = board[0]
                        domino_end = board[len(board)-1]

                        if(domino_start.is_horizontal):
                            value_start_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_start)
                            if value_start_horizontal in ["Left", "Right"] :
                                if value_start_horizontal =="Left":
                                    box_x = domino_start.position[0] - player1.selected.width
                                    box_y = domino_start.position[1]
                                    left_domino = True
                                    up_domino = None
                                elif value_start_horizontal =="Right":
                                    box_x = domino_start.position[0] + domino_start.width
                                    box_y = domino_start.position[1] 
                                    left_domino = False
                                    up_domino = None 
                                show_square = True
                                valid = check_valid_domino_board_horizontal(domino_start, player1.selected, left_domino, up_domino)
                                start_domino = True
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break     
                            else:
                                show_square = False                        
                               
                        elif(domino_start.is_horizontal == False):
                            value_start_vertical = check_mouse_link_domino_vertical(mouse_position, domino_start)
                            if value_start_vertical not in ["Up", "Down", None]:
                                if value_start_vertical == "Up-Left":
                                    box_x = domino_start.position[0] - player1.selected.width
                                    box_y = domino_start.position[1]
                                    left_domino = True
                                    up_domino = True
                                elif value_start_vertical == "Up-Right":
                                    box_x = domino_start.position[0] + domino_start.width
                                    box_y = domino_start.position[1]
                                    left_domino = False
                                    up_domino = True
                                elif value_start_vertical == "Down-Left":
                                    box_x = domino_start.position[0] - player1.selected.width
                                    box_y = domino_start.position[1] + player1.selected.height
                                    left_domino = True
                                    up_domino = False
                                elif value_start_vertical == "Down-Right":
                                    box_x = domino_start.position[0] + domino_start.width
                                    box_y = domino_start.position[1] + player1.selected.height
                                    left_domino = False
                                    up_domino = False
                                # elif value_start_vertical =="Up":
                                #     box_x = domino_start.position[0] 
                                #     box_y = domino_start.position[1] + domino_start.height
                                #     left_domino = None
                                #     up_domino = True
                                # elif value_start_vertical =="Down":
                                #     box_x = domino_start.position[0] + domino_start.width
                                #     box_y = domino_start.position[1] + player1.selected.height
                                #     left_domino = None
                                #     up_domino = False
                                
                                show_square = True
                                valid = check_valid_domino_board_vertical(domino_start, player1.selected, left_domino, up_domino)
                                start_domino = True
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break  
                            else:
                                show_square = False 
                                       
                        if(domino_end.is_horizontal):
                            value_end_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_end)
                            if value_end_horizontal in ["Left", "Right"]:
                                # if value_end_horizontal == "Left-Up":
                                #     box_x = domino_end.position[0]
                                #     box_y = domino_end.position[1] - player1.selected.height
                                #     left_domino = True
                                #     up_domino = True
                                # elif value_end_horizontal == "Left-Down":
                                #     box_x = domino_end.position[0]
                                #     box_y = domino_end.position[1] + domino.height
                                #     left_domino = True
                                #     up_domino = False
                                # elif value_end_horizontal == "Right-Up":
                                #     box_x = domino_end.position[0] + player1.selected.width
                                #     box_y = domino_end.position[1] - player1.selected.height
                                #     left_domino = False
                                #     up_domino = True
                                # elif value_end_horizontal == "Right-Down":
                                #     box_x = domino_end.position[0] + player1.selected.width
                                #     box_y = domino_end.position[1] + domino.height
                                #     left_domino = True
                                #     up_domino = False
                                if value_end_horizontal =="Left":
                                    box_x = domino_end.position[0] - player1.selected.width
                                    box_y = domino_end.position[1]
                                    left_domino = True
                                    up_domino = None
                                elif value_end_horizontal =="Right":
                                    box_x = domino_end.position[0] + domino_end.width
                                    box_y = domino_end.position[1] 
                                    left_domino = False
                                    up_domino = None 
                                
                                show_square = True  
                                valid = check_valid_domino_board_horizontal(domino_end, player1.selected, left_domino, up_domino)
                                start_domino = False
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break  
                            else:
                                show_square = False                             
                               
                        elif(domino_end.is_horizontal == False):
                            value_end_vertical = check_mouse_link_domino_vertical(mouse_position, domino_end)
                            if value_end_vertical not in ["Up", "Down", None]:
                                if value_end_vertical == "Up-Left":
                                    box_x = domino_end.position[0] - player1.selected.width
                                    box_y = domino_end.position[1]
                                    left_domino = True
                                    up_domino = True
                                elif value_end_vertical == "Up-Right":
                                    box_x = domino_end.position[0] + domino_end.width
                                    box_y = domino_end.position[1]
                                    left_domino = False
                                    up_domino = True
                                elif value_end_vertical == "Down-Left":
                                    box_x = domino_end.position[0] - player1.selected.width
                                    box_y = domino_end.position[1] + player1.selected.height
                                    left_domino = True
                                    up_domino = False
                                elif value_end_vertical == "Down-Right":
                                    box_x = domino_end.position[0] + domino_end.width
                                    box_y = domino_end.position[1] + player1.selected.height
                                    left_domino = False
                                    up_domino = False
                                # elif value_start_vertical =="Up":
                                #     box_x = domino_end.position[0] 
                                #     box_y = domino_end.position[1] + domino_end.height
                                #     left_domino = None
                                #     up_domino = True
                                # elif value_start_vertical =="Down":
                                #     box_x = domino_end.position[0] + domino_end.width
                                #     box_y = domino_end.position[1] + player1.selected.height
                                #     left_domino = None
                                #     up_domino = False  
                                
                                show_square = True
                                valid = check_valid_domino_board_vertical(domino_end, player1.selected, left_domino, up_domino)
                                start_domino = False
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break
                            else:
                                show_square = False 
                         
            elif is_dragging and player1.selected.is_horizontal == False:
                if(len(board) > 0):
                    if(len(board) == 1):
                        domino = board[0]
                        if domino.is_horizontal == True:
                            if is_mouse_link_domino_left(mouse_position, domino):
                                show_square = True
                                left_domino = True
                                start_domino = True
                                valid = check_valid_domino(domino, player1.selected, left_domino)
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                box_x = domino.position[0] - player1.selected.width
                                box_y = domino.position[1]

                            elif is_mouse_link_domino_right(mouse_position, domino):
                                show_square = True
                                left_domino = False
                                start_domino = False
                                valid = check_valid_domino(domino, player1.selected, left_domino)
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True

                                box_x = domino.position[0] + domino.width
                                box_y = domino.position[1]
                            else:
                                show_square = False 
                        elif domino.is_horizontal == False:
                            check_mouse_link_domino_vertical(mouse_position, domino)
                            check_valid_domino_board_vertical(domino, player1.selected,)
                    else:     
                        domino_start = board[0]
                        domino_end = board[len(board)-1]

                        if(domino_start.is_horizontal):
                            value_start_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_start)
                            if value_start_horizontal not in ["Left", "Right", None]:
                                if value_start_horizontal == "Left-Up":
                                    box_x = domino_start.position[0]
                                    box_y = domino_start.position[1] - player1.selected.height
                                    left_domino = True
                                    up_domino = True
                                elif value_start_horizontal == "Left-Down":
                                    box_x = domino_start.position[0]
                                    box_y = domino_start.position[1] + domino_start.height
                                    left_domino = True
                                    up_domino = False
                                elif value_start_horizontal == "Right-Up":
                                    box_x = domino_start.position[0] + player1.selected.width
                                    box_y = domino_start.position[1] - player1.selected.height
                                    left_domino = False
                                    up_domino = True
                                elif value_start_horizontal == "Right-Down":
                                    box_x = domino_start.position[0] + player1.selected.width
                                    box_y = domino_start.position[1] + domino_start.height
                                    left_domino = False
                                    up_domino = False
                                # if value_start_horizontal =="Left":
                                #     box_x = domino_start.position[0] - player1.selected.width
                                #     box_y = domino_start.position[1]
                                #     left_domino = True
                                #     up_domino = None
                                # elif value_start_horizontal =="Right":
                                #     box_x = domino_start.position[0] + domino_start.width
                                #     box_y = domino_start.position[1] 
                                #     left_domino = False
                                #     up_domino = None 
                                
                                show_square = True
                                valid = check_valid_domino_board_horizontal(domino_start, player1.selected, left_domino, up_domino)
                                start_domino = True
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break
                            else:
                                show_square = False                                 
                            
                        elif(domino_start.is_horizontal == False):
                            value_start_vertical = check_mouse_link_domino_vertical(mouse_position, domino_start)
                            print(value_start_vertical)
                            if value_start_vertical in ["Up", "Down"]:
                                # if value_start_vertical == "Up-Left":
                                #     box_x = domino_start.position[0] - player1.selected.width
                                #     box_y = domino_start.position[1]
                                #     left_domino = True
                                #     up_domino = True
                                # elif value_start_vertical == "Up-Right":
                                #     box_x = domino_start.position[0] + domino_start.width
                                #     box_y = domino_start.position[1]
                                #     left_domino = False
                                #     up_domino = True
                                # elif value_start_vertical == "Down-Left":
                                #     box_x = domino_start.position[0] - player1.selected.width
                                #     box_y = domino_start.position[1] + player1.selected.height
                                #     left_domino = True
                                #     up_domino = False
                                # elif value_start_vertical == "Down-Right":
                                #     box_x = domino_start.position[0] + domino_start.width
                                #     box_y = domino_start.position[1] + player1.selected.height
                                #     left_domino = False
                                #     up_domino = False
                                if value_start_vertical =="Up":
                                    box_x = domino_start.position[0] 
                                    box_y = domino_start.position[1] - domino_start.height
                                    left_domino = None
                                    up_domino = True
                                elif value_start_vertical =="Down":
                                    box_x = domino_start.position[0]
                                    box_y = domino_start.position[1] + domino_start.height
                                    left_domino = None
                                    up_domino = False 
                                
                                show_square = True
                                valid = check_valid_domino_board_vertical(domino_start, player1.selected, left_domino, up_domino)
                                start_domino = True
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break   
                            else:
                                show_square = False

                        if(domino_end.is_horizontal):
                            value_end_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_end)
                            print(domino_end.get_dot_counts(), value_end_horizontal)
                            if value_end_horizontal not in ["Left", "Right", None]:
                                if value_end_horizontal == "Left-Up":
                                    box_x = domino_end.position[0]
                                    box_y = domino_end.position[1] - player1.selected.height
                                    left_domino = True
                                    up_domino = True
                                elif value_end_horizontal == "Left-Down":
                                    box_x = domino_end.position[0]
                                    box_y = domino_end.position[1] + domino_end.height
                                    left_domino = True
                                    up_domino = False
                                elif value_end_horizontal == "Right-Up":
                                    box_x = domino_end.position[0] + player1.selected.width
                                    box_y = domino_end.position[1] - player1.selected.height
                                    left_domino = False
                                    up_domino = True
                                elif value_end_horizontal == "Right-Down":
                                    box_x = domino_end.position[0] + player1.selected.width
                                    box_y = domino_end.position[1] + domino_end.height
                                    left_domino = False
                                    up_domino = False
                                # if value_end_horizontal =="Left":
                                #     box_x = domino_end.position[0] - player1.selected.width
                                #     box_y = domino_end.position[1]
                                #     left_domino = True
                                #     up_domino = None
                                # elif value_end_horizontal =="Right":
                                #     box_x = domino_end.position[0] + domino_end.width
                                #     box_y = domino_end.position[1] 
                                #     left_domino = False
                                #     up_domino = None
                                
                                show_square = True
                                valid = check_valid_domino_board_horizontal(domino_end, player1.selected, left_domino, up_domino)
                                start_domino = False
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break   
                            else:
                                show_square = False                          
                            
                        elif(domino_end.is_horizontal == False):
                            value_end_vertical = check_mouse_link_domino_vertical(mouse_position, domino_end)
                            if value_end_vertical in ["Up", "Down"]:
                                # if value_start_vertical == "Up-Left":
                                #     box_x = domino_end.position[0] - player1.selected.width
                                #     box_y = domino_end.position[1]
                                #     left_domino = True
                                #     up_domino = True
                                # elif value_start_vertical == "Up-Right":
                                #     box_x = domino_end.position[0] + domino_end.width
                                #     box_y = domino_end.position[1]
                                #     left_domino = False
                                #     up_domino = True
                                # elif value_start_vertical == "Down-Left":
                                #     box_x = domino_end.position[0] - player1.selected.width
                                #     box_y = domino_end.position[1] + player1.selected.height
                                #     left_domino = True
                                #     up_domino = False
                                # elif value_start_vertical == "Down-Right":
                                #     box_x = domino_end.position[0] + domino_end.width
                                #     box_y = domino_end.position[1] + player1.selected.height
                                #     left_domino = False
                                #     up_domino = False
                                if value_end_vertical =="Up":
                                    box_x = domino_end.position[0] 
                                    box_y = domino_end.position[1] - domino_end.height
                                    left_domino = None
                                    up_domino = True
                                elif value_end_vertical =="Down":
                                    box_x = domino_end.position[0]
                                    box_y = domino_end.position[1] + player1.selected.height
                                    left_domino = None
                                    up_domino = False  
                                
                                show_square = True
                                valid = check_valid_domino_board_vertical(domino_end, player1.selected, left_domino, up_domino)
                                start_domino = False
                                if(valid == True):
                                    error_sq = False
                                else:
                                    error_sq = True
                                break    
                            else:
                                show_square = False                  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if is_dragging and player1.selected.is_horizontal == True:
                    player1.selected.set_image(pygame.transform.rotate(player1.selected.get_image(), -90))
                    player1.selected.rotated()
                    player1.selected.is_horizontal = not player1.selected.is_horizontal
                    hand_player.append(player1.selected)
                    is_dragging = False
                    player1.selected = None
                    show_square = False  
                    # is_dragging = False
                    # selected_domino = None
                elif is_dragging:
                    hand_player.append(player1.selected)
                    is_dragging = False
                    player1.selected = None
                    show_square = False  

            if event.key == pygame.K_r:
                if(is_dragging == True):
                    player1.selected.set_image(pygame.transform.rotate(player1.selected.get_image(), -90))
                    player1.selected.rotated()

                    p = selected_domino_height
                    selected_domino_height = selected_domino_width
                    selected_domino_width = p

                    player1.selected.is_horizontal = not player1.selected.is_horizontal
                    if rotated == 3:
                        rotated = 1
                    if rotated == 1:
                        player1.selected.swap_dot()
                    rotated += 1
                    show_square = False
                    
            if event.key == pygame.K_s:
                mouse_x, mouse_y = pygame.mouse.get_pos()

    #draw background
    screen.fill((0, 0, 0))

    if show_square and error_sq == False:
        # Vẽ hình vuông với viền
        square_rect = pygame.Rect(box_x ,box_y , player1.selected.width, player1.selected.height)
        pygame.draw.rect(screen, square_color, square_rect)
        # pygame.draw.rect(screen, square_border_color, square_rect, 2)
    if show_square and error_sq == True:
        square_rect = pygame.Rect(box_x ,box_y , player1.selected.width, player1.selected.height)
        pygame.draw.rect(screen, error_sq_color, square_rect)

    #draw domino
    for i, domino in enumerate(dominoList):
        image = domino.get_image()
        rect = pygame.Rect(i * 50, 0, 5, 10)
        resized_image = pygame.transform.scale(image, (domino.width, domino.height))
        screen.blit(resized_image, rect)

    #draw player hand
    for i, domino in enumerate(player1.hand):
        image = domino.get_image()
        position_x = i * 80
        position_y = screen_height - domino.height
        domino.set_position(position_x, position_y)
        rect = pygame.Rect(position_x, position_y , domino.width, domino.height)
        resized_image = pygame.transform.scale(image, (domino.width, domino.height))
        screen.blit(resized_image, rect)

    #draw domino board
    for i, domino in enumerate(board):
        image = domino.get_image()
        rect = pygame.Rect(domino.position[0], domino.position[1], domino.width, domino.height)
        resized_image = pygame.transform.scale(image, (domino.width, domino.height))
        screen.blit(resized_image, rect)

    #draw picked domino
    if is_dragging:
        image = player1.selected.get_image()
        rect = pygame.Rect(mouse_position[0] - player1.selected.width//2 , mouse_position[1] - player1.selected.height//2, player1.selected.width, player1.selected.height)
        resized_image = pygame.transform.scale(image, (player1.selected.width, player1.selected.height))
        screen.blit(resized_image, rect)

    pygame.display.flip()

# Kết thúc game
pygame.quit()