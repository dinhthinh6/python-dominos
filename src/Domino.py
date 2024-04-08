class Domino:
    def __init__(self, dot1, dot2, image):
        self.dot1 = dot1
        self.dot2 = dot2
        self.width = 48
        self.height = 96
        self.image = image
        self.position = []
        self.is_horizontal = False
        self.link = []


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