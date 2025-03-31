import pygame
from images import*
from constants import*
from sprites import Wall, Stair
from constants import*
from button_function import undo_move, reset_maze, show_options, show_world_map, quit_to_main, OptionsMenu
from audio_manager import AudioManager
from level_manager import load_level

class Game:
    def __init__(self, game_screen, audio_manager, level_number=1):
        self.game_screen = game_screen
        self.level_number = level_number
        self.backdrop = pygame.image.load("images/backdrop.png")
        self.floor = pygame.image.load("images/floor.jpg")
        self.title_img = pygame.image.load("images/mumlogo.png")

        # Load dữ liệu từ JSON
        self.maze, self.stairs_positions = load_level(self.level_number)

        # Debug: In ra dữ liệu vừa load từ file JSON
        print(f"Debug level {self.level_number}:")
        print("Maze:", self.maze)
        print("Stairs:", self.stairs_positions)


        # Nhóm quản lý tường và cầu thang
        self.walls = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()

        self.create_objects()  # Khởi tạo vật thể

        self.audio_manager = audio_manager
        self.audio_manager.play_background_music()

        # Khởi tạo các thành phần giao diện trong game
        self.options_menu = OptionsMenu(self.audio_manager)

        # Danh sách các nút bấm
        self.buttons = [
            {"rect": pygame.Rect(12, 135, 125, 35), "action": lambda: undo_move(self.audio_manager), "label": "UNDO MOVE"},
            {"rect": pygame.Rect(12, 180, 125, 35), "action": lambda: reset_maze(self.audio_manager), "label": "RESET MAZE"},
            {"rect": pygame.Rect(12, 230, 125, 35), "action": lambda: show_options(self.options_menu, self.audio_manager), "label": "OPTIONS"},
            {"rect": pygame.Rect(12, 270, 125, 35), "action": lambda: show_world_map(self.audio_manager), "label": "WORLD MAP"},
            {"rect": pygame.Rect(12, 435, 125, 35), "action": lambda: quit_to_main(self.audio_manager), "label": "QUIT TO MAIN"}
        ]

    def create_objects(self):
        """Tạo tường và cầu thang dựa trên maze"""
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                cell = self.maze[row][col] #Lấy dữ liệu của ô

                x = 215 + col * CELL_SIZE
                y = 80 + row * CELL_SIZE
            
                #Vẽ tường
                if "walls" in cell:
                    for wall_type in cell["walls"]:
                        if wall_type == "top":
                            #Vẽ tường ngang ở top
                            self.walls.add(Wall(x, y, "W_h"))
                        elif wall_type == "bottom":
                            # Vẽ tường ngang ở bottom
                            self.walls.add(Wall(x, y + CELL_SIZE, "W_h"))
                        elif wall_type == "left":
                            # Vẽ tường dọc ởở left
                            self.walls.add(Wall(x, y, "W_v"))
                        elif wall_type == "right":
                            # Vẽ tường dọc ở right
                            self.walls.add(Wall(x + CELL_SIZE, y, "W_v"))

        #Vẽ cầu thang
        for stair in self.stairs_positions:
            row = int(stair["row"])  # Lấy giá trị từ dictionary
            col = int(stair["col"]) 

            x = 215 + col * CELL_SIZE
            y = 80 + row * CELL_SIZE

            self.stairs.add(Stair(x, y, stair["type"])) #Tạo cầu thang
    
    def next_level(self):
        """Chuyển sang level tiếp theo"""
        self.level_number += 1 #Tăng level lên 1

        # Load dữ liệu mới từ JSON
        self.maze, self.stairs_positions = load_level(self.level_number)
        
        #Xóa các đối tượng cũ
        self.walls.empty()
        self.stairs.empty()

        #Cập nhật maze và cầu thang
        #self.maze = new_maze
        #self.stairs_positions = new_stairs

        #Tạo lại vật thể
        self.create_objects()

        #Cập nhật lại màn hình ngay sau khi load level
        self.draw_game()
    
    def draw_game(self):
        """Vẽ màn hình game lên screen"""
        self.game_screen.blit(self.backdrop, (0, 0))
        self.game_screen.blit(self.floor, (215, 80))
        self.game_screen.blit(self.title_img, (10, 10))

        #Vẽ tất cả sprite trong nhóm
        self.walls.draw(self.game_screen)
        self.stairs.draw(self.game_screen)

        self.options_menu.draw(self.game_screen)

    def handled_event(self, event):
        """Xử lý sự kiện trong game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"   #Quay lại màn hình menu khi nhấn ESC
            
        # Xử lý sự kiện cho menu tùy chọn
        if self.options_menu.active:
            if self.options_menu.handle_event(event):
                return "play"
        else:    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at: {mouse_pos}")

                # Xử lý sự kiện cho các nút bấm
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        print(f"Button clicked: {button['label']}")
                        if button["label"] == "QUIT TO MAIN":
                            return "menu"  # Quay lại menu chính
                        button["action"]()
                        break
        return "play"