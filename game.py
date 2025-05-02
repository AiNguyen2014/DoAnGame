import pygame
from constants import *
from sprites import Wall, Stair, Player, Mummy, Trap
from button_function import undo_move, reset_maze, show_options, show_world_map, quit_to_main, OptionsMenu
from audio_manager import AudioManager
from images_manager import IMAGES
from level_manager import LevelManager

class Game:
    def __init__(self, game_screen, audio_manager, level_manager, map_instance):
        self.game_screen = game_screen
        self.level_manager = level_manager
        self.map_instance = map_instance
        self.backdrop = IMAGES["backdrop"]
        self.floor = IMAGES["floor"]
        self.title_img = IMAGES["mumlogo"]
        self.snake_img = IMAGES["snake"] 
        self.snake_img = pygame.transform.scale(self.snake_img, (130, 80))
        self.game_over_img = IMAGES["game_over"]
        self.game_over_rect = self.game_over_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.walls = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        self.game_over = False
        self.move_history = []

        self.maze = None
        self.stairs_positions = None
        self.player_start = None
        self.mummies_data = []
        self.traps_data = []
        self.player = None
        self.mummies = []
        self.gate = {"isClosed": False}  # Giả sử không có cổng hoặc cổng mở

        self.audio_manager = audio_manager
        self.audio_manager.play_background_music()
        self.options_menu = OptionsMenu(self.audio_manager)

        self.buttons = [
            {"rect": pygame.Rect(12, 135, 125, 35), "action": lambda: undo_move(self.audio_manager), "label": "UNDO MOVE"},
            {"rect": pygame.Rect(12, 180, 125, 35), "action": lambda: reset_maze(self.audio_manager), "label": "RESET MAZE"},
            {"rect": pygame.Rect(12, 230, 125, 35), "action": lambda: show_options(self.options_menu, self.audio_manager), "label": "OPTIONS"},
            {"rect": pygame.Rect(12, 270, 125, 35), "action": lambda: show_world_map(self, self.audio_manager), "label": "WORLD MAP"},
            {"rect": pygame.Rect(12, 435, 125, 35), "action": lambda: quit_to_main(self.audio_manager), "label": "QUIT TO MAIN"}
        ]

        self.game_over_buttons = [
            {"rect": pygame.Rect(239, 300, 106, 16), "action": self.try_again, "label": "TRY AGAIN"},
            {"rect": pygame.Rect(230, 341, 106, 19), "action": self.undo_last_move, "label": "UNDO MOVE"},
            {"rect": pygame.Rect(406, 300, 119, 17), "action": self.show_world_map, "label": "WORLD MAP"}
        ]

        self.load_level()

    def try_again(self):
        self.load_level()

    def undo_last_move(self):
        if self.move_history:
            pass

    def show_world_map(self):
        self.map_instance.toggle("play")
        return "map"     

    def load_level(self):
        self.walls.empty()
        self.stairs.empty()
        self.characters.empty()
        self.traps.empty()
        self.keys.empty()
        self.mummies = []
        self.move_history.clear()
        self.game_over = False

        maze, stairs_positions, player_start, mummies_data, traps_data = self.level_manager.get_current_level_data()
        
        self.maze = maze
        self.stairs_positions = stairs_positions
        self.player_start = player_start
        self.mummies_data = mummies_data
        self.traps_data = traps_data

        if maze is None:
            print(f"Không thể tải cấp độ {self.level_manager.current_level + 1}!")
            return

        print(f"Debug level {self.level_manager.current_level + 1}:")
        print("Maze:", maze)
        print("Stairs:", stairs_positions)
        print("Player Start:", player_start)
        print("Mummies:", mummies_data)
        print("Traps:", traps_data)

        player_x = 215 + player_start["col"] * CELL_SIZE
        player_y = 80 + player_start["row"] * CELL_SIZE
        self.player = Player(player_x, player_y)
        self.characters.add(self.player)

        for mummy_data in mummies_data:
            mummy_x = 215 + mummy_data["col"] * CELL_SIZE
            mummy_y = 80 + mummy_data["row"] * CELL_SIZE
            color = mummy_data["color"].lower()
            if color not in ["white", "red"]:
                print(f"Warning: Invalid mummy color '{color}' in level {self.level_manager.current_level + 1}. Using 'white'.")
                color = "white"
            mummy = Mummy(mummy_x, mummy_y, color=color)
            self.mummies.append(mummy)
            self.characters.add(mummy)
        
        for trap_data in traps_data:
            trap_x = 215 + trap_data["col"] * CELL_SIZE
            trap_y = 80 + trap_data["row"] * CELL_SIZE
            self.traps.add(Trap(trap_x, trap_y))

        self.create_objects()
        
    def create_objects(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                cell = self.maze[row][col]
                x = 215 + col * CELL_SIZE
                y = 80 + row * CELL_SIZE

                if "walls" in cell:
                    for wall_type in cell["walls"]:
                        if wall_type == "top":
                            self.walls.add(Wall(x, y, "W_h"))
                        elif wall_type == "bottom":
                            self.walls.add(Wall(x, y + CELL_SIZE, "W_h"))
                        elif wall_type == "left":
                            self.walls.add(Wall(x, y, "W_v"))
                        elif wall_type == "right":
                            self.walls.add(Wall(x + CELL_SIZE, y, "W_v"))

        for stair in self.stairs_positions:
            row = stair["row"]
            col = stair["col"]
            x = 215 + col * CELL_SIZE
            y = 80 + row * CELL_SIZE
            # Chỉ tạo sprite Stair nếu ô đích nằm trong mê cung (để hiển thị hình ảnh)
            if 0 <= row < 7 and 0 <= col < 7:
                self.stairs.add(Stair(x, y, stair["type"]))

    def next_level(self):
        success = self.level_manager.next_level()
        if success:
            self.load_level()
            return "play"
        else:
            print("You've completed all levels!")
            return "menu"
        
    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.traps, False):
            print("Player hit a trap! Game Over!")
            return "menu"

        # Kiểm tra nếu người chơi đến ô đích (có thể nằm ngoài mê cung)
        for stair in self.stairs_positions:
            if self.player.row == stair["row"] and self.player.col == stair["col"]:
                print("Player reached the stairs! Moving to next level.")
                return self.next_level()

        return "play"

    def update(self):
        if self.player:
            self.player.update()
    
        for mummy in self.mummies:
            mummy.update()

        if self.player and not self.player.moving:
            for character in self.characters:
                if character != self.player and pygame.sprite.collide_rect(self.player, character):
                    self.game_over = True
                    break
                
            self.check_collisions()

    def draw_game(self):
        self.game_screen.blit(self.backdrop, (0, 0))
        self.game_screen.blit(self.floor, (215, 80))
        self.game_screen.blit(self.title_img, (10, 10))

        self.update()

        self.walls.draw(self.game_screen)
        self.traps.draw(self.game_screen)
        self.keys.draw(self.game_screen)
        self.characters.draw(self.game_screen)
        self.stairs.draw(self.game_screen)
        self.options_menu.draw(self.game_screen)

        if self.game_over:
            self.game_screen.blit(self.game_over_img, self.game_over_rect)
        
        self.options_menu.draw(self.game_screen)

    def handled_event(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.game_over_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        print(f"Game over button clicked: {button['label']}")
                        if button["label"] == "TRY AGAIN":
                            self.load_level()
                            self.game_over = False
                            return "play"
                        elif button["label"] == "UNDO MOVE":
                            self.undo_last_move()
                            self.game_over = False
                            return "play"
                        elif button["label"] == "WORLD MAP":
                            return "map"
            return "play"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_UP:
                print("Pressed UP")
                if self.player.move("up", self.maze, self.gate, self.stairs_positions):
                    for mummy in self.mummies:
                        mummy.auto_move(self.maze, self.gate, self.player.row, self.player.col)
                    return self.check_collisions()
                else:
                    print("Move UP blocked!")
            elif event.key == pygame.K_DOWN:
                print("Pressed DOWN")
                if self.player.move("down", self.maze, self.gate, self.stairs_positions):
                    for mummy in self.mummies:
                        mummy.auto_move(self.maze, self.gate, self.player.row, self.player.col)
                    return self.check_collisions()
                else:
                    print("Move DOWN blocked!")
            elif event.key == pygame.K_LEFT:
                print("Pressed LEFT")
                if self.player.move("left", self.maze, self.gate, self.stairs_positions):
                    for mummy in self.mummies:
                        mummy.auto_move(self.maze, self.gate, self.player.row, self.player.col)
                    return self.check_collisions()
                else:
                    print("Move LEFT blocked!")
            elif event.key == pygame.K_RIGHT:
                print("Pressed RIGHT")
                if self.player.move("right", self.maze, self.gate, self.stairs_positions):
                    for mummy in self.mummies:
                        mummy.auto_move(self.maze, self.gate, self.player.row, self.player.col)
                    return self.check_collisions()
                else:
                    print("Move RIGHT blocked!")

        if self.options_menu.active:
            if self.options_menu.handle_event(event):
                return "play"
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at: {mouse_pos}")
                for button in self.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        print(f"Button clicked: {button['label']}")
                        if button["label"] == "QUIT TO MAIN":
                            return "menu"
                        button["action"]()
                        break
        return "play"