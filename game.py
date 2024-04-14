import contextlib
with contextlib.redirect_stdout(None):
    import pygame
from client import Network
import random
import os
from src.Model import Player, Domino
from PIL import Image

pygame.font.init()
pygame.mixer.init()
W, H = 1400, 720

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TURN_FONT = pygame.font.SysFont("comicsans", 30)

# Dynamic Variables
selected = None
hand = []
players = []
board = ""
current_turn = 0
start = ""
is_dragging = False
rotated = 1
box_help = [False, 0,0]
error_box = False
error = False
insert_start = True
# Load the sound file
sound = pygame.mixer.Sound("./assets/sound/bg.wav")
sound.play()
# Set the initial sound state
is_sound_on = True

# Load the button images
button_image_on = pygame.image.load("./assets/ic_volume.png")
button_image_off = pygame.image.load("./assets/ic_volume_off.png")

# Scale the button images to the desired size
button_size = (60, 60)
button_image_on = pygame.transform.scale(button_image_on, button_size)
button_image_off = pygame.transform.scale(button_image_off, button_size)

# Set the initial button image
button_image = button_image_on if is_sound_on else button_image_off

# Define the button position
button_position = (W - button_size[0] - 50, 50)  # Right-aligned position)

# Define the colors
WHITE = (255, 255, 255)
BROWN = (210, 107, 3)
BUTTON_COLOR = BROWN
BUTTON_BORDER_COLOR = WHITE
BUTTON_TEXT_COLOR = WHITE
# Define the font
font = pygame.font.Font(None, 32)

# Define the button dimensions
button_width, button_height = 150, 50
button_corner_radius = 10

# Define the button position
button_x = W - button_width - 40
button_y = H - button_height - 40

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

# def is_mouse_link_domino_left_up(mouse_position, domino):
#     if mouse_position[0] > (domino.position[0] ) \
#         and mouse_position[0] < (domino.position[0] + players[current_id].selected.width)\
#         and mouse_position[1] > (domino.position[1] - players[current_id].selected.height)\
#         and mouse_position[1] < (domino.position[1]) :
#         return True
#     else :
#         return False

# def is_mouse_link_domino_left_down(mouse_position, domino):
#     if mouse_position[0] > (domino.position[0]) \
#         and mouse_position[0] < (domino.position[0]+ players[current_id].selected.width)\
#         and mouse_position[1] > (domino.position[1] )\
#         and mouse_position[1] < (domino.position[1] + players[current_id].selected.height) :
#         return True
#     else :
#         return False
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


# def check_mouse_link_domino(mouse_position, domino):
#     if mouse_position[0] > (domino.position[0] ) \
#         and mouse_position[0] < (domino.position[0] + players[current_id].selected.width)\
#         and mouse_position[1] > (domino.position[1] - players[current_id].selected.height)\
#         and mouse_position[1] < (domino.position[1]) :
#         return "Left-Up"
#     elif mouse_position[0] > (domino.position[0] + players[current_id].selected.width) \
#         and mouse_position[0] < (domino.position[0] + players[current_id].selected.width * 2)\
#         and mouse_position[1] > (domino.position[1] - players[current_id].selected.height)\
#         and mouse_position[1] < (domino.position[1]) :
#         return "Right-Up"
#     elif mouse_position[0] > (domino.position[0]) \
#         and mouse_position[0] < (domino.position[0]+ players[current_id].selected.width)\
#         and mouse_position[1] > (domino.position[1] )\
#         and mouse_position[1] < (domino.position[1] + players[current_id].selected.height) :
#         return "Left-Down"
#     elif mouse_position[0] > (domino.position[0] + players[current_id].selected.width) \
#         and mouse_position[0] < (domino.position[0]+ players[current_id].selected.width * 2)\
#         and mouse_position[1] > (domino.position[1] )\
#         and mouse_position[1] < (domino.position[1] + players[current_id].selected.height) :
#         return "Right-Down"
    
def check_mouse_link_domino_horizontal(mouse_position, domino, selected):
    if mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + selected.width)\
        and mouse_position[1] > (domino.position[1] - selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link == 2:
        return "Left-Up"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + selected.width)\
        and mouse_position[1] > (domino.position[1] + domino.height)\
        and mouse_position[1] < (domino.position[1] + domino.height + selected.height)\
        and domino.link == 2 :
        return "Left-Down"
    elif mouse_position[0] > (domino.position[0] + selected.width) \
        and mouse_position[0] < (domino.position[0] + selected.width * 2)\
        and mouse_position[1] > (domino.position[1] - selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link == 1 :
        return "Right-Up"
    elif mouse_position[0] > (domino.position[0] + selected.width) \
        and mouse_position[0] < (domino.position[0] + selected.width * 2)\
        and mouse_position[1] > (domino.position[1] + domino.height)\
        and mouse_position[1] < (domino.position[1] + domino.height + selected.height)\
        and domino.link == 1 :
        return "Right-Down"
    elif mouse_position[0] > (domino.position[0] - selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + selected.height)\
        and domino.link == 2 :
        return "Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0] + domino.width + selected.width)\
        and mouse_position[1] > (domino.position[1] )\
        and mouse_position[1] < (domino.position[1] + selected.height )\
        and domino.link == 1 :
        return "Right"
    
def check_mouse_link_domino_vertical(mouse_position, domino, selected):
    if mouse_position[0] > (domino.position[0] - selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + selected.height)\
        and domino.link == 2:
        return "Up-Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0] + domino.width + selected.width)\
        and mouse_position[1] > (domino.position[1])\
        and mouse_position[1] < (domino.position[1] + selected.height)\
        and domino.link == 2 :
        return "Up-Right"
    elif mouse_position[0] > (domino.position[0] - selected.width) \
        and mouse_position[0] < (domino.position[0])\
        and mouse_position[1] > (domino.position[1] + selected.height )\
        and mouse_position[1] < (domino.position[1] + selected.height * 2)\
        and domino.link == 1 :
        return "Down-Left"
    elif mouse_position[0] > (domino.position[0] + domino.width) \
        and mouse_position[0] < (domino.position[0]+ domino.width + selected.width)\
        and mouse_position[1] > (domino.position[1] + selected.height )\
        and mouse_position[1] < (domino.position[1] + selected.height * 2)\
        and domino.link == 1 :
        return "Down-Right"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0] + selected.width)\
        and mouse_position[1] > (domino.position[1] - selected.height)\
        and mouse_position[1] < (domino.position[1])\
        and domino.link == 2 :
        return "Up"
    elif mouse_position[0] > (domino.position[0]) \
        and mouse_position[0] < (domino.position[0]+ selected.width)\
        and mouse_position[1] > (domino.position[1] +domino.height )\
        and mouse_position[1] < (domino.position[1] + domino.height + selected.height )\
        and domino.link == 1 :
        return "Down"

def toggle_sound():
    global is_sound_on, button_image
    is_sound_on = not is_sound_on  # Chuyển đổi trạng thái

    if is_sound_on:
        sound.play(-1) #lặp âm thanh
        button_image = button_image_on
    else:
        sound.stop()
        button_image = button_image_off
def redraw_window(players,current_id, board, is_dragging, box_help,error ,hand, selected, current_turn):

	# WIN.fill((255,255,255)) # fill screen white, to clear old frames
	# Tạo màu cho board
	WIN.fill((210, 107, 3))

	# Tạo hình chữ nhật ở giữa màn hình
	rect_width = W  # Chiều rộng của hình chữ nhật bằng với chiều rộng của cửa sổ đồ họa
	rect_height = 400
	rect_x = 0  # Vị trí x để hình chữ nhật nằm ở giữa màn hình theo chiều ngang
	rect_y = (H - rect_height) // 2  # Vị trí y để hình chữ nhật nằm giữa màn hình theo chiều dọc
	pygame.draw.rect(WIN, (9, 148, 15), (rect_x, rect_y, rect_width, rect_height))

	# Tạo viền bọc domino (oppent's)
	rect_width = 760
	rect_height = 140
	rect_x = (W - rect_width) // 2  # Vị trí x để hình chữ nhật nằm giữa màn hình theo chiều ngang
	rect_y = (H - rect_height) // 20 - 24  # Vị trí y để hình chữ nhật nằm ở phía trên theo chiều dọc
	rect_radius = 10

	# Vẽ hình chữ nhật nhỏ hơn lên trên với màu trắng
	border_width = 2
	pygame.draw.rect(WIN, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_width,border_radius=rect_radius)

	# Tạo viền bọc domino (you)
	rect_width = 760
	rect_height = 140
	rect_x = (W - rect_width) // 2  # Vị trí x để hình chữ nhật nằm giữa màn hình theo chiều ngang
	rect_y = (H - rect_height) - 5  # Vị trí y để hình chữ nhật nằm ở phía trên theo chiều dọc
	rect_radius = 10

	# Vẽ hình chữ nhật nhỏ hơn lên trên với màu trắng
	border_width = 2
	pygame.draw.rect(WIN, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height), border_width,border_radius=rect_radius)

	# Vẽ button volume
	WIN.blit(button_image, button_position)

	# Vẽ viền button pass
	pygame.draw.rect(WIN, BUTTON_BORDER_COLOR, (button_x, button_y, button_width, button_height), 0,
					 button_corner_radius)
	pygame.draw.rect(WIN, BUTTON_COLOR, (button_x + 2, button_y + 2, button_width - 4, button_height - 4), 0,
					 button_corner_radius)

	# Vẽ text button pass
	button_text = "Pass"
	text_surface = font.render(button_text, True, BUTTON_TEXT_COLOR)
	text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
	WIN.blit(text_surface, text_rect)


	#  if box_help[0] and error  == False:
    #     # Vẽ hình vuông với viền
    #     square_rect = pygame.Rect(box_help[1] ,box_help[2] , players[current_id].selected.width, players[current_id].selected.height)
    #     pygame.draw.rect(screen, square_color, square_rect)
    #     # pygame.draw.rect(screen, square_border_color, square_rect, 2)
    # if box_help[0] and error  == True:
    #     square_rect = pygame.Rect(box_help[1] ,box_help[2] , players[current_id].selected.width, players[current_id].selected.height)
    #     pygame.draw.rect(screen, error _color, square_rect)

	if(box_help[0] == True) and error ==  False :
		box = pygame.Rect(box_help[1] ,box_help[2] , selected.width, selected.height)
		pygame.draw.rect(WIN, (106, 212, 221), box)

	if box_help[0] == True and error == True:
		box = pygame.Rect(box_help[1] ,box_help[2] , selected.width, selected.height)
		pygame.draw.rect(WIN, (250, 112, 112), box)

	# #Draw Board
	for i, domino in enumerate(board):
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

		WIN.blit(resized_image, rect)

	#Draw player hand
	for i, domino in enumerate(hand):
		domino_image = domino.get_image()
		image = pygame.image.load(domino_image)
		position_x = (W - len(hand) * domino.width * 2) // 2 + domino.width * i * 2
		position_y = H - domino.height

		# Move the hand
		position_y -= 20
		position_x += 25


		domino.set_position(position_x, position_y)
		hand[i].set_position(position_x, position_y)
		rect = pygame.Rect(position_x, position_y , domino.width, domino.height)
		resized_image = pygame.transform.scale(image, (domino.width, domino.height))
		WIN.blit(resized_image, rect)

	#Draw other player hand
	for i in players:
		if players[i] != players[current_id]:
			for j, domino in enumerate(players[i].hand):
				domino_image = f"assets\\Domino.png"
				image = pygame.image.load(domino_image)
				position_x = (W - len(players[i].hand) * domino.width * 2) // 2 + domino.width * j * 2
				position_y = 0

				# Move the hand
				position_y += 20
				position_x += 25

				domino.set_position(position_x, position_y)
				rect = pygame.Rect(position_x, position_y , domino.width, domino.height)
				resized_image = pygame.transform.scale(image, (domino.width, domino.height))
				WIN.blit(resized_image, rect)

	#Draw selected player
	if(selected != None):
		# if(selected.dot1 < selected.dot2):
		# 	if(selected.is_horizontal == False):
		# 		pass
		# 	else:
		# 		selected.set_image(pygame.transform.rotate(selected.get_image(), -90))

		# print(type(players[current_id].selected.width), type( players[current_id].selected.height))
		mouse_position = pygame.mouse.get_pos()
		image = selected.get_image_pg()
		# image = pygame.image.load(domino_image)
		rect = pygame.Rect(mouse_position[0] - selected.width//2 , mouse_position[1] - selected.height//2, selected.width, selected.height)
		resized_image = pygame.transform.scale(image, (selected.width, selected.height))
		WIN.blit(resized_image, rect)

	if current_id == current_turn:	
		text = TURN_FONT.render("Turn: Your Turn" , 1,(255,255,255))
		WIN.blit(text,(10,10))
	else:
		text = TURN_FONT.render("Turn: Opponent's" , 1, (255,255,255))
		WIN.blit(text,(10,10))
	# if current_id == current_turn:
	# 	text = TURN_FONT.render("Turn: Your Turn" , 1,(0,0,0))
	# 	WIN.blit(text,(10,10))
	# else:
	# 	text = TURN_FONT.render("Turn: Opponent's Turn" , 1, (0,0,0))
	# 	WIN.blit(text,(10,10))

	# if is_dragging:
	# 	mouse_position = pygame.mouse.get_pos()
	# 	domino_image = players[current_id].selected.get_image()
	# 	image = pygame.image.load(domino_image)
	# 	print(domino_image)
	# 	rect = pygame.Rect(mouse_position[0] - players[current_id].selected.width//2 , mouse_position[1] - players[current_id].selected.height//2, players[current_id].selected.width, players[current_id].selected.height)
	# 	resized_image = pygame.transform.scale(image, (players[current_id].selected.width, players[current_id].selected.height))
	# 	WIN.blit(resized_image, rect)


def main(name):
	"""
	function for running the game,
	includes the main loop of the game
	:param players: a list of dicts represting a player
	:return: None
	"""
	global players,current_turn ,board, is_dragging, box_help,error, hand, selected, rotated, insert_start

	# start by connecting to the network
	server = Network()
	current_id = server.connect(name)
	players, current_turn,  board, start = server.send("get")
	hand = players[current_id].hand
	for domino in  hand:
		domino_image = pygame.image.load(domino.get_image())
		domino.set_image_pg(domino_image)

	# setup the clock, limit to 30fps
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(60) # 30 fps max
		player = players[current_id]
		# send data to server and recieve back all players information\
		data = "get"
		for event in pygame.event.get():
			# if user hits red x button close window
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEMOTION:
				mouse_position = pygame.mouse.get_pos()
				# print(selected)
				if is_dragging and selected.is_horizontal == True:
					if(len(board) > 0):
						if(len(board) == 1):
							domino = board[0]
							if domino.is_horizontal == True:
								if is_mouse_link_domino_left(mouse_position, domino):
									box_help[0] = True
									left_domino = True
									insert_start = True
									valid = check_valid_domino(domino, selected, left_domino)
									if(valid == True):
										error  = False
									else:
										error  = True
									box_help[1] = domino.position[0] - selected.width
									box_help[2] = domino.position[1]

								elif is_mouse_link_domino_right(mouse_position, domino):
									box_help[0] = True
									left_domino = False
									insert_start = True
									valid = check_valid_domino(domino, selected, left_domino)
									if(valid == True):
										error  = False
									else:
										error  = True
									box_help[1] = domino.position[0] + selected.width
									box_help[2] = domino.position[1]
								else:
									box_help[0] = False 
							elif domino.is_horizontal == False:
								check_mouse_link_domino_vertical(mouse_position, domino, selected)
								check_valid_domino_board_vertical(domino, selected)
						else:     
							domino_start = board[0]
							domino_end = board[len(board)-1]

							if(domino_start.is_horizontal):
								value_start_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_start, selected)
								if value_start_horizontal in ["Left", "Right"] :
									if value_start_horizontal =="Left":
										box_help[1] = domino_start.position[0] - selected.width
										box_help[2] = domino_start.position[1]
										left_domino = True
										up_domino = None
									elif value_start_horizontal =="Right":
										box_help[1] = domino_start.position[0] + domino_start.width
										box_help[2] = domino_start.position[1] 
										left_domino = False
										up_domino = None 
									box_help[0] = True
									valid = check_valid_domino_board_horizontal(domino_start, selected, left_domino, up_domino)
									insert_start = True
									if(valid == True):
										error  = False
									else:
										error  = True
									break     
								else:
									box_help[0] = False                        
								
							elif(domino_start.is_horizontal == False):
								value_start_vertical = check_mouse_link_domino_vertical(mouse_position, domino_start, selected)
								if value_start_vertical not in ["Up", "Down", None]:
									if value_start_vertical == "Up-Left":
										box_help[1] = domino_start.position[0] - selected.width
										box_help[2] = domino_start.position[1]
										left_domino = True
										up_domino = True
									elif value_start_vertical == "Up-Right":
										box_help[1] = domino_start.position[0] + domino_start.width
										box_help[2] = domino_start.position[1]
										left_domino = False
										up_domino = True
									elif value_start_vertical == "Down-Left":
										box_help[1] = domino_start.position[0] - selected.width
										box_help[2] = domino_start.position[1] + selected.height
										left_domino = True
										up_domino = False
									elif value_start_vertical == "Down-Right":
										box_help[1] = domino_start.position[0] + domino_start.width
										box_help[2] = domino_start.position[1] + selected.height
										left_domino = False
										up_domino = False

									
									box_help[0] = True
									valid = check_valid_domino_board_vertical(domino_start, selected, left_domino, up_domino)
									insert_start = True
									if(valid == True):
										error  = False
									else:
										error  = True
									break  
								else:
									box_help[0] = False 
										
							if(domino_end.is_horizontal):
								value_end_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_end, selected)
								if value_end_horizontal in ["Left", "Right"]:

									if value_end_horizontal =="Left":
										box_help[1] = domino_end.position[0] - selected.width
										box_help[2] = domino_end.position[1]
										left_domino = True
										up_domino = None
									elif value_end_horizontal =="Right":
										box_help[1] = domino_end.position[0] + domino_end.width
										box_help[2] = domino_end.position[1] 
										left_domino = False
										up_domino = None 
									
									box_help[0] = True  
									valid = check_valid_domino_board_horizontal(domino_end, selected, left_domino, up_domino)
									insert_start = False
									if(valid == True):
										error  = False
									else:
										error  = True
									break  
								else:
									box_help[0] = False                             
								
							elif(domino_end.is_horizontal == False):
								value_end_vertical = check_mouse_link_domino_vertical(mouse_position, domino_end, selected)
								if value_end_vertical not in ["Up", "Down", None]:
									if value_end_vertical == "Up-Left":
										box_help[1] = domino_end.position[0] - selected.width
										box_help[2] = domino_end.position[1]
										left_domino = True
										up_domino = True
									elif value_end_vertical == "Up-Right":
										box_help[1] = domino_end.position[0] + domino_end.width
										box_help[2] = domino_end.position[1]
										left_domino = False
										up_domino = True
									elif value_end_vertical == "Down-Left":
										box_help[1] = domino_end.position[0] - selected.width
										box_help[2] = domino_end.position[1] + selected.height
										left_domino = True
										up_domino = False
									elif value_end_vertical == "Down-Right":
										box_help[1] = domino_end.position[0] + domino_end.width
										box_help[2] = domino_end.position[1] + selected.height
										left_domino = False
										up_domino = False

									
									box_help[0] = True
									valid = check_valid_domino_board_vertical(domino_end, selected, left_domino, up_domino)
									insert_start = False
									if(valid == True):
										error  = False
									else:
										error  = True
									break
								else:
									box_help[0] = False 
							
				elif is_dragging and selected.is_horizontal == False:
					if(len(board) > 0):
						if(len(board) == 1):
							domino = board[0]
							if domino.is_horizontal == True:
								if is_mouse_link_domino_left(mouse_position, domino):
									box_help[0] = True
									left_domino = True
									insert_start = True
									valid = check_valid_domino(domino, selected, left_domino)
									if(valid == True):
										error  = False
									else:
										error  = True
									box_help[1] = domino.position[0] - selected.width
									box_help[2] = domino.position[1]

								elif is_mouse_link_domino_right(mouse_position, domino):
									box_help[0] = True
									left_domino = False
									insert_start = True
									valid = check_valid_domino(domino, selected, left_domino)
									if(valid == True):
										error  = False
									else:
										error  = True
									box_help[1] = domino.position[0] + domino.width
									box_help[2] = domino.position[1]
								else:
									box_help[0] = False 
							elif domino.is_horizontal == False:
								check_mouse_link_domino_vertical(mouse_position, domino, selected)
								check_valid_domino_board_vertical(domino, selected,)
						else:     
							domino_start = board[0]
							domino_end = board[len(board)-1]

							if(domino_start.is_horizontal):
								value_start_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_start, selected)
								if value_start_horizontal not in ["Left", "Right", None]:
									if value_start_horizontal == "Left-Up":
										box_help[1] = domino_start.position[0]
										box_help[2] = domino_start.position[1] - selected.height
										left_domino = True
										up_domino = True
									elif value_start_horizontal == "Left-Down":
										box_help[1] = domino_start.position[0]
										box_help[2] = domino_start.position[1] + domino_start.height
										left_domino = True
										up_domino = False
									elif value_start_horizontal == "Right-Up":
										box_help[1] = domino_start.position[0] + selected.width
										box_help[2] = domino_start.position[1] - selected.height
										left_domino = False
										up_domino = True
									elif value_start_horizontal == "Right-Down":
										box_help[1] = domino_start.position[0] + selected.width
										box_help[2] = domino_start.position[1] + domino_start.height
										left_domino = False
										up_domino = False
									
									box_help[0] = True
									valid = check_valid_domino_board_horizontal(domino_start, selected, left_domino, up_domino)
									insert_start = True
									if(valid == True):
										error  = False
									else:
										error  = True
									break
								else:
									box_help[0] = False                                 
								
							elif(domino_start.is_horizontal == False):
								value_start_vertical = check_mouse_link_domino_vertical(mouse_position, domino_start, selected)
								if value_start_vertical in ["Up", "Down"]:
									if value_start_vertical =="Up":
										box_help[1] = domino_start.position[0] 
										box_help[2] = domino_start.position[1] - domino_start.height
										left_domino = None
										up_domino = True
									elif value_start_vertical =="Down":
										box_help[1] = domino_start.position[0]
										box_help[2] = domino_start.position[1] + domino_start.height
										left_domino = None
										up_domino = False 
									
									box_help[0] = True
									valid = check_valid_domino_board_vertical(domino_start, selected, left_domino, up_domino)
									insert_start = True
									if(valid == True):
										error  = False
									else:
										error  = True
									break   
								else:
									box_help[0] = False

							if(domino_end.is_horizontal):
								value_end_horizontal = check_mouse_link_domino_horizontal(mouse_position, domino_end, selected)
								# print(domino_end.get_dot_counts(), value_end_horizontal)
								if value_end_horizontal not in ["Left", "Right", None]:
									if value_end_horizontal == "Left-Up":
										box_help[1] = domino_end.position[0]
										box_help[2] = domino_end.position[1] - selected.height
										left_domino = True
										up_domino = True
									elif value_end_horizontal == "Left-Down":
										box_help[1] = domino_end.position[0]
										box_help[2] = domino_end.position[1] + domino_end.height
										left_domino = True
										up_domino = False
									elif value_end_horizontal == "Right-Up":
										box_help[1] = domino_end.position[0] + selected.width
										box_help[2] = domino_end.position[1] - selected.height
										left_domino = False
										up_domino = True
									elif value_end_horizontal == "Right-Down":
										box_help[1] = domino_end.position[0] + selected.width
										box_help[2] = domino_end.position[1] + domino_end.height
										left_domino = False
										up_domino = False
									# if value_end_horizontal =="Left":
									#     box_help[1] = domino_end.position[0] - player1.selected.width
									#     box_help[2] = domino_end.position[1]
									#     left_domino = True
									#     up_domino = None
									# elif value_end_horizontal =="Right":
									#     box_help[1] = domino_end.position[0] + domino_end.width
									#     box_help[2] = domino_end.position[1] 
									#     left_domino = False
									#     up_domino = None
									
									box_help[0] = True
									valid = check_valid_domino_board_horizontal(domino_end, selected, left_domino, up_domino)
									insert_start = False
									if(valid == True):
										error  = False
									else:
										error  = True
									break   
								else:
									box_help[0] = False                          
								
							elif(domino_end.is_horizontal == False):
								value_end_vertical = check_mouse_link_domino_vertical(mouse_position, domino_end, selected)
								if value_end_vertical in ["Up", "Down"]:
									# if value_start_vertical == "Up-Left":
									#     box_help[1] = domino_end.position[0] - player1.selected.width
									#     box_help[2] = domino_end.position[1]
									#     left_domino = True
									#     up_domino = True
									# elif value_start_vertical == "Up-Right":
									#     box_help[1] = domino_end.position[0] + domino_end.width
									#     box_help[2] = domino_end.position[1]
									#     left_domino = False
									#     up_domino = True
									# elif value_start_vertical == "Down-Left":
									#     box_help[1] = domino_end.position[0] - player1.selected.width
									#     box_help[2] = domino_end.position[1] + player1.selected.height
									#     left_domino = True
									#     up_domino = False
									# elif value_start_vertical == "Down-Right":
									#     box_help[1] = domino_end.position[0] + domino_end.width
									#     box_help[2] = domino_end.position[1] + player1.selected.height
									#     left_domino = False
									#     up_domino = False
									if value_end_vertical =="Up":
										box_help[1] = domino_end.position[0] 
										box_help[2] = domino_end.position[1] - domino_end.height
										left_domino = None
										up_domino = True
									elif value_end_vertical =="Down":
										box_help[1] = domino_end.position[0]
										box_help[2] = domino_end.position[1] + selected.height
										left_domino = None
										up_domino = False  
									
									box_help[0] = True
									valid = check_valid_domino_board_vertical(domino_end, selected, left_domino, up_domino)
									insert_start = False
									if(valid == True):
										error  = False
									else:
										error  = True
									break    
								else:
									box_help[0] = False     
        
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_position = pygame.mouse.get_pos()
				# print(is_dragging, selected, current_turn, current_id)

				# Trạng thái tắt bật âm thanh
				if button_position[0] <= mouse_position[0] <= button_position[0] + button_size[0] and button_position[1] <= mouse_position[1] <= button_position[1] + button_size[1]:
							toggle_sound()

				# data = "put " + "start" + " " + str(players[current_id].hand[0]) + " " + str(current_turn)
				# print(is_dragging)
				# players, current_turn ,board  = server.send(data)
				if(is_dragging == False and selected == None and current_turn == current_id):
					for i, domino in enumerate(hand):
						# print(domino.position)
						if is_mouse_on_domino(mouse_position, domino.get_position()):
							selected = domino
							# print(selected)
							is_dragging = True  # Bắt đầu dragging
							rotated = 1
							data = "pick:" + str(domino) + "-" +  str(i)
							hand.pop(i)
							break
				elif (current_turn == current_id):
					if(start == False):
						# board.insert(0, [selected_domino, selected_domino_width, selected_domino_height, mouse_x, mouse_y])
						domino_x = mouse_position[0] - selected.width//2
						domino_y = mouse_position[1] - selected.height//2
						selected.set_position(domino_x,domino_y)
						is_dragging = False
						players[current_id].selected.dot1 = selected.dot1
						players[current_id].selected.dot2 = selected.dot2
						players[current_id].selected.is_horizontal = selected.is_horizontal
						players[current_id].selected.height = selected.height
						players[current_id].selected.width = selected.width
						players[current_id].selected.set_position(domino_x, domino_y)
						# print(players[current_id].selected.image)

						data = "putfirst:" + str(players[current_id].selected) + "-" + str(current_turn)
						selected = None
						# start = True
					elif(start == True and box_help[0] == True and insert_start == True and  error  == False):
						box_help[0] = False
						selected.set_position(box_help[1],box_help[2])  
						players[current_id].selected.dot1 = selected.dot1
						players[current_id].selected.dot2 = selected.dot2
						players[current_id].selected.is_horizontal = selected.is_horizontal
						players[current_id].selected.height = selected.height
						players[current_id].selected.width = selected.width
						players[current_id].selected.set_position(box_help[1],box_help[2])

						is_dragging = False
						selected = None
						data = "put:" + str(players[current_id].selected) + "-" + "start" + "-" + str(current_turn)

					elif(start == True and box_help[0] == True and insert_start == False and  error  ==  False):
						box_help[0] = False
						selected.set_position(box_help[1],box_help[2])  
						players[current_id].selected.dot1 = selected.dot1
						players[current_id].selected.dot2 = selected.dot2
						players[current_id].selected.is_horizontal = selected.is_horizontal
						players[current_id].selected.height = selected.height
						players[current_id].selected.width = selected.width
						players[current_id].selected.set_position(box_help[1],box_help[2])

						is_dragging = False
						selected = None
						data = "put:" + str(players[current_id].selected) + "-" + "end" + "-" + str(current_turn)

					# elif (show_box_help == True):
					# 	show_box_help = False
					# 	players[current_id].selected.set_position(box_help[1],box_help[2])  
					# 	link = update_link_domino(board[0] ,players[current_id].selected)
					# 	board[0].link.append(link[0])
					# 	players[current_id].selected.link.append(link[1])
					# 	# board.insert(0, [selected_domino, box_help[1], box_help[2], 96, square_size])
					# 	board.insert(0, players[current_id].selected)
					# 	is_dragging = False
					# 	players[current_id].selected = None

					
					# elif box_help[0] == True and insert_start == False and error  == False: 
					# 	box_help[0] = False
					# 	players[current_id].selected.set_position(box_help[1],box_help[2])
					# 	link = update_link_domino(board[len(board)-1] ,players[current_id].selected)
					# 	board[len(board)-1].link.append(link[0])
					# 	players[current_id].selected.link.append(link[1])
					# 	# board.append([selected_domino, box_help[1], box_help[2], 96, square_size])
					# 	board.append(players[current_id].selected)
					# 	is_dragging = False
					# 	players[current_id].selected = None

			if event.type == pygame.KEYDOWN:	
				if event.key == pygame.K_p:
					if(is_dragging == False and current_turn == current_id):
						data = "swap:" + str(current_turn)
						# data = "putfirst:" + str(players[current_id].selected) + "-" + str(current_turn)


				if event.key == pygame.K_r:
					if(is_dragging == True):
						selected.set_image_pg(pygame.transform.rotate(selected.get_image_pg(), -90))
						selected.rotated()
						selected.is_horizontal = not selected.is_horizontal
						if rotated == 3:
							rotated = 1
						if rotated == 1:
							selected.swap_dot()
						rotated += 1
						box_help[0] = False	

				if event.key == pygame.K_q:
					if is_dragging and selected.is_horizontal == True:
						# selected.set_image_pg(pygame.transform.rotate(selected.get_image_pg(), -90))
						# selected.rotated()
						# selected.is_horizontal = not selected.is_horizontal

						hand.append(players[current_id].selected)
						is_dragging = False
						selected = None
						box_help[0] = False  
						data = "drop"
						# is_dragging = False
						# selected_domino = None
					elif is_dragging:
						domino_image = pygame.image.load(players[current_id].selected.get_image())
						players[current_id].selected.set_image_pg(domino_image)
						hand.append(players[current_id].selected)
						is_dragging = False
						selected = None
						box_help[0] = False
						data = "drop"


		players, current_turn ,board , start = server.send(data)
		# print(players[current_id].selected)
		# redraw window then update the frame
		redraw_window(players,current_id , board, is_dragging, box_help, error,hand, selected, current_turn)
		pygame.display.update()


	server.disconnect()
	pygame.quit()
	quit()

while True:
	name = input("Please enter your name: ")
	if 0 < len(name) < 20:
		break
	else:
		print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")
		
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,30)

# setup pygame window
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Dominoss")

# start game
main(name)
