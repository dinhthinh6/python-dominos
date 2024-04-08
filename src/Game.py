
class Game:
    def __init__(self, num_players, dominoes):
        self.players = []
        for i in range(num_players):
            self.players.append(Player(f"Player {i+1}"))
            self.board = Board(800, 600)  # Ví dụ kích thước bảng
            self.dominoes = dominoes  # Danh sách tất cả domino
            self.current_player = 0  # Chỉ số người chơi hiện tại

    def deal_dominoes(self):
        # Trộn domino ngẫu nhiên và chia bài cho người chơi (chưa thực hiện)
        pass

    def handle_mouse_click(self, event):
        # Xử lý sự kiện
        pass