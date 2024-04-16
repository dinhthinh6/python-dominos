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
        self.surface.fill((0, 0, 0))

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

        self.play_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=pygame_menu.themes.THEME_BLUE,
            title='Play Menu',
            width=WINDOW_SIZE[0]
        )

        self.start_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=pygame_menu.themes.THEME_BLUE,
            title='Start Server',
            width=WINDOW_SIZE[0]
        )
        self.username_server_text = self.start_server_menu.add.text_input(title='Username: ')
        self.start_server_menu.add.button('Start', self.start_click)
        self.start_server_menu.add.button('Return to main menu', pygame_menu.events.RESET)
        

        self.join_server_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=pygame_menu.themes.THEME_BLUE,
            title='Join Server',
            width=WINDOW_SIZE[0]
        )
        # self.ip_address_text = self.join_server_menu.add.text_input(title='IP address: ')
        self.username_client_text = self.join_server_menu.add.text_input(title='Username: ')
        self.join_server_menu.add.button('Join', self.join_click)
        self.join_server_menu.add.button('Return to main menu', pygame_menu.events.RESET)

        self.play_menu.add.button('Start server', self.start_server_menu)
        self.play_menu.add.button('Join server', self.join_server_menu)
        self.play_menu.add.button('Return to main menu', pygame_menu.events.BACK)
        
        main_theme = pygame_menu.themes.THEME_BLUE.copy()

        self.main_menu = pygame_menu.Menu(
            height=WINDOW_SIZE[1],
            theme=main_theme,
            title='Main Menu',
            width=WINDOW_SIZE[0]
        )

        self.main_menu.add.button(title='Play', action=self.play_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

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


