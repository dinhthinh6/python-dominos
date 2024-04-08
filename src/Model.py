class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  # Danh sách domino trong tay
        self.selected = None

    def draw_domino(self, screen, x, y):
    # Vẽ domino của người chơi trên màn hình (chưa thực hiện)
       pass

    def place_domino(self, board, domino):
    # Xử lý đặt domino lên bảng (chưa thực hiện)
        pass

    def switch_turn(self):
        pass  # Chuyển đổi lượt chơi (logic đơn giản)
class Board:
    def __init__(self):
        self.placed_dominoes = []  # Danh sách domino đã đặt

    def add_domino(self, domino, position):
        # Xử lý thêm domino vào danh sách đã đặt và kiểm tra vị trí (chưa thực hiện)
        pass

    def draw_board(self, screen):
        # Vẽ bảng domino trên màn hình (chưa thực hiện)
        pass
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