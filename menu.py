import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional

from main import Server, Client, Board

FPS = 60
WINDOW_SIZE = (540, 540)

class Menu:
    def __init__(self):
        self.clock: Optional['pygame.time.Clock'] = None
        self.main_menu: Optional['pygame_menu.Menu'] = None
        self.surface: Optional['pygame.Surface'] = None

    def main_background(self):
        self.surface.fill((9, 148, 15))

    def start_click(self):
        username = self.username_server_text.get_value()
        if not username: return
        Server('', 55843, username, self.surface)

    def join_click(self):
        # ip_address = self.ip_address_text.get_value().strip()
        ip_address = "127.0.0.1"
        if not ip_address: return
        username = self.username_client_text.get_value()
        if not username: return
        Client(ip_address, 55843, username)

    def run(self):
        self.surface = create_example_window('DOMINOS - Socket', WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        main_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        main_theme.background_color = (9, 148, 15)
        main_theme.title_background_color = (9, 148, 15)

        self.play_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=main_theme,
            title='',
            width=WINDOW_SIZE[0]
        )

        self.start_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=main_theme,
            title='   Start Server',
            width=WINDOW_SIZE[0]
        )

        # Tạo font chữ sigmarOne
        font_path = "./assets/fonts/SigmarOne-Regular.ttf"
        font = pygame.font.Font(font_path, 46)
        text_surface = font.render("to", True, (9, 148, 15))
        self.surface.blit(text_surface, (100, 100))

        # Màu sắc label
        font_size_welcome_to = 36
        font_size = 56
        font_name_welcome_to = pygame_menu.font.get_font(font_path, font_size_welcome_to)
        font_name_domino = pygame_menu.font.get_font(font_path, font_size)
        font_color = (210, 107, 3)
        selected_color = (255, 0, 0)
        readonly_color = (0, 255, 0)
        readonly_selected_color = (0, 0, 255)
        background_color = (9, 148, 15)

        selected_color_server = (255, 255, 255)
        self.username_server_text = self.start_server_menu.add.text_input(title='Username: ')
        server_text = self.username_server_text
        btn_start_server = self.start_server_menu.add.button('Start', self.start_click)
        btn_return_server = self.start_server_menu.add.button('Return to main menu', pygame_menu.events.RESET)

        server_text.set_font(font_name_welcome_to, font_size_welcome_to, font_color, selected_color_server, readonly_color, readonly_selected_color, background_color)
        btn_start_server.set_font(font_name_welcome_to, font_size_welcome_to, font_color, selected_color_server, readonly_color, readonly_selected_color, background_color)
        btn_return_server.set_font(font_name_welcome_to, font_size_welcome_to, font_color, selected_color_server, readonly_color, readonly_selected_color, background_color)

        self.join_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=main_theme,
            title='   Join Server',
            width=WINDOW_SIZE[0]
        )


        selected_color_start_server = (255, 255, 255)
        font_name_server = pygame_menu.font.get_font(font_path, 40)

        # self.ip_address_text = self.join_server_menu.add.text_input(title='IP address: ')
        self.username_client_text = self.join_server_menu.add.text_input(title='Username: ')
        client_text = self.username_client_text
        btn_joint_click = self.join_server_menu.add.button('Join', self.join_click)
        btn_return_menu_client = self.join_server_menu.add.button('Return to main menu', pygame_menu.events.RESET)



        btn_start_server = self.play_menu.add.button('Start server', self.start_server_menu)
        btn_join_server = self.play_menu.add.button('Join server', self.join_server_menu)
        btn_return_menu = self.play_menu.add.button('Return to main menu', pygame_menu.events.BACK)


        btn_start_server.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)
        btn_join_server.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)
        btn_return_menu.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)
        client_text.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)
        btn_joint_click.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)
        btn_return_menu_client.set_font(font_name_server, font_size_welcome_to, font_color, selected_color_start_server, readonly_color, readonly_selected_color, background_color)

        self.main_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=main_theme,
            title='',
            width=WINDOW_SIZE[0]
        )


        label_welcome = self.main_menu.add.label("Welcome")
        label_to = self.main_menu.add.label("to")
        label_domino = self.main_menu.add.label("Domino")

        #Khoảng cách label
        label_welcome.set_margin(-110,10)
        label_to.set_margin(-100,0)
        label_domino.set_margin(100,20)



        label_welcome.set_font(font_name_welcome_to, font_size_welcome_to, font_color, selected_color, readonly_color, readonly_selected_color, background_color)
        label_to.set_font(font_name_welcome_to, font_size_welcome_to, font_color, selected_color, readonly_color, readonly_selected_color, background_color)
        label_domino.set_font(font_name_domino, font_size, font_color, selected_color, readonly_color, readonly_selected_color, background_color)

        font_name_play = pygame_menu.font.FONT_FIRACODE_BOLD
        font_size_play = 30
        font_color_play = (255,255,255)
        selected_color = (255, 255, 255)
        readonly_color = (0, 255, 0)
        readonly_selected_color = (0, 0, 255)
        background_color = (9, 148, 15)

        btn_play = self.main_menu.add.button(title='Play', action=self.play_menu)
        btn_quit = self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

        btn_play.set_font(font_name_play, font_size_play, font_color_play, selected_color, readonly_color, readonly_selected_color, background_color)
        btn_quit.set_font(font_name_play, font_size_play, font_color_play, selected_color, readonly_color, readonly_selected_color, background_color)

        self.main_background()
        
        while True:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if self.main_menu.is_enabled():
                self.main_menu.mainloop(self.surface, self.main_background, fps_limit=FPS)

            pygame.display.update()


