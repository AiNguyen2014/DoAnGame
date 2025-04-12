import pygame
from constants import *
from sprites import Wall, Stair, Player, Mummy, Scorpion, Trap, Key
from button_function import undo_move, reset_maze, show_options, show_world_map, quit_to_main, OptionsMenu
from audio_manager import AudioManager
from images_manager import IMAGES
from level_manager import load_level

class Game:
    def __init__(self, game_screen, audio_manager, level_number=1):
        self.game_screen = game_screen
        self.level_number = level_number
        self.backdrop = IMAGES["backdrop"]
        self.floor = IMAGES["floor"]
        self.title_img = IMAGES["mumlogo"]

        # Load dữ liệu từ JSON
        self.maze, self.stairs_positions, self.player_start, self.mummies_data, self.scorpions_data, self.traps_data, self.keys_data = load_level(self.level_number)
        
        if self.maze is None:
            raise FileNotFoundError(f"Could not load level {self.level_number}")

        # Nhóm quản lý sprite
        self.walls = pygame.sprite.Group()
        self.stairs = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()

        # Khởi tạo người chơi
        player_x = 215 + self.player_start["col"] * CELL_SIZE
        player_y = 80 + self.player_start["row"] * CELL_SIZE
        self.player = Player(player_x, player_y)
        self.characters.add(self.player)

        # Khởi tạo xác ướp
        self.mummies = []
        for mummy_data in self.mummies_data:
            mummy_x = 215 + mummy_data["col"] * CELL_SIZE
            mummy_y = 80 + mummy_data["row"] * CELL_SIZE
            mummy = Mummy(mummy_x, mummy_y, color=mummy_data["color"])
            self.mummies.append(mummy)
            self.characters.add(mummy)

        # Khởi tạo bò cạp
        self.scorpions = []
        for scorpion_data in self.scorpions_data:
            scorpion_x = 215 + scorpion_data["col"] * CELL_SIZE
            scorpion_y = 80 + scorpion_data["row"] * CELL_SIZE
            scorpion = Scorpion(scorpion_x, scorpion_y, color=scorpion_data["color"])
            self.scorpions.append(scorpion)
            self.characters.add(scorpion)

        # Khởi tạo bẫy
        for trap_data in self.traps_data:
            trap_x = 215 + trap_data["col"] * CELL_SIZE
            trap_y = 80 + trap_data["row"] * CELL_SIZE
            self.traps.add(Trap(trap_x, trap_y))

        # Khởi tạo chìa khóa
        for key_data in self.keys_data:
            key_x = 215 + key_data["col"] * CELL_SIZE
            key_y = 80 + key_data["row"] * CELL_SIZE
            self.keys.add(Key(key_x, key_y))

        self.create_objects()  # Khởi tạo vật thể

        self.audio_manager = audio_manager
        self.audio_manager.play_background_music()

        # Khởi tạo giao diện
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
        self.walls.empty()
        self.stairs.empty()

        for row in range(len(self.maze)):
            for col in range(len(self.maze[row])):
                cell = self.maze[row][col]
                x = 215 + col * CELL_SIZE
                y = 80 + row * CELL_SIZE

                # Vẽ tường
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

        # Vẽ cầu thang
        for stair in self.stairs_positions:
            row = stair["row"]
            col = stair["col"]
            x = 215 + col * CELL_SIZE
            y = 80 + row * CELL_SIZE
            if 0 <= row < 7 and 0 <= col < 7:
                self.stairs.add(Stair(x, y, stair["type"]))

    def check_collisions(self):
        """Kiểm tra va chạm giữa các đối tượng"""
        # Player chạm Trap -> Thua
        if pygame.sprite.spritecollide(self.player, self.traps, False):
            print("Player hit a trap! Game Over!")
            return "menu"

        # Player chạm Key -> Nhặt key
        keys_hit = pygame.sprite.spritecollide(self.player, self.keys, True)
        if keys_hit:
            print("Player picked up a key!")

        # Player chạm Stair -> Chuyển level
        if pygame.sprite.spritecollide(self.player, self.stairs, False):
            print("Player reached the stairs! Moving to next level.")
            self.next_level()
            return "play"

        # Mummy và Scorpion chạm nhau -> Scorpion thua
        for mummy in self.mummies:
            for scorpion in self.scorpions[:]:
                if pygame.sprite.collide_rect(mummy, scorpion):
                    print("Mummy and Scorpion collided! Scorpion is defeated.")
                    self.scorpions.remove(scorpion)
                    self.characters.remove(scorpion)

        # Mummy chạm Mummy -> Một Mummy thua
        for i, mummy1 in enumerate(self.mummies[:]):
            for mummy2 in self.mummies[i + 1:]:
                if pygame.sprite.collide_rect(mummy1, mummy2):
                    print("Two Mummies collided! One is defeated.")
                    self.mummies.remove(mummy2)
                    self.characters.remove(mummy2)
                    break

        # Player chạm Mummy hoặc Scorpion -> Thua
        for character in self.characters:
            if character != self.player and pygame.sprite.collide_rect(self.player, character):
                print("Player collided with an enemy! Game Over!")
                return "menu"

        return "play"

    def next_level(self):
        """Chuyển sang level tiếp theo"""
        self.level_number += 1
        self.maze, self.stairs_positions, self.player_start, self.mummies_data, self.scorpions_data, self.traps_data, self.keys_data = load_level(self.level_number)

        if self.maze is None:
            print(f"Level {self.level_number} not found! Returning to menu.")
            self.level_number = 1
            self.maze, self.stairs_positions, self.player_start, self.mummies_data, self.scorpions_data, self.traps_data, self.keys_data = load_level(self.level_number)
            if self.maze is None:
                raise FileNotFoundError("Could not load any levels.")

        # Xóa các đối tượng cũ
        self.walls.empty()
        self.stairs.empty()
        self.characters.empty()
        self.traps.empty()
        self.keys.empty()
        self.mummies.clear()
        self.scorpions.clear()

        # Khởi tạo lại các đối tượng
        player_x = 215 + self.player_start["col"] * CELL_SIZE
        player_y = 80 + self.player_start["row"] * CELL_SIZE
        self.player = Player(player_x, player_y)
        self.characters.add(self.player)

        for mummy_data in self.mummies_data:
            mummy_x = 215 + mummy_data["col"] * CELL_SIZE
            mummy_y = 80 + mummy_data["row"] * CELL_SIZE
            mummy = Mummy(mummy_x, mummy_y, color=mummy_data["color"])
            self.mummies.append(mummy)
            self.characters.add(mummy)

        for scorpion_data in self.scorpions_data:
            scorpion_x = 215 + scorpion_data["col"] * CELL_SIZE
            scorpion_y = 80 + scorpion_data["row"] * CELL_SIZE
            scorpion = Scorpion(scorpion_x, scorpion_y, color=scorpion_data["color"])
            self.scorpions.append(scorpion)
            self.characters.add(scorpion)

        for trap_data in self.traps_data:
            trap_x = 215 + trap_data["col"] * CELL_SIZE
            trap_y = 80 + trap_data["row"] * CELL_SIZE
            self.traps.add(Trap(trap_x, trap_y))

        for key_data in self.keys_data:
            key_x = 215 + key_data["col"] * CELL_SIZE
            key_y = 80 + key_data["row"] * CELL_SIZE
            self.keys.add(Key(key_x, key_y))

        self.create_objects()
        self.draw_game()

    def draw_game(self):
        """Vẽ màn hình game"""
        self.game_screen.blit(self.backdrop, (0, 0))
        self.game_screen.blit(self.floor, (215, 80))
        self.game_screen.blit(self.title_img, (10, 10))

        # Vẽ tất cả sprite
        self.walls.draw(self.game_screen)
        self.traps.draw(self.game_screen)
        self.keys.draw(self.game_screen)
        self.characters.draw(self.game_screen)
        self.stairs.draw(self.game_screen)
        self.options_menu.draw(self.game_screen)

    def handled_event(self, event):
        """Xử lý sự kiện trong game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            elif event.key == pygame.K_UP:
                print("Pressed UP")  # Debug
                if self.player.move("up", self.maze, self.walls):
                    for mummy in self.mummies:
                        mummy.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    for scorpion in self.scorpions:
                        scorpion.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    return self.check_collisions()
            elif event.key == pygame.K_DOWN:
                print("Pressed DOWN")  # Debug
                if self.player.move("down", self.maze, self.walls):
                    for mummy in self.mummies:
                        mummy.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    for scorpion in self.scorpions:
                        scorpion.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    return self.check_collisions()
            elif event.key == pygame.K_LEFT:
                print("Pressed LEFT")  # Debug
                if self.player.move("left", self.maze, self.walls):
                    for mummy in self.mummies:
                        mummy.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    for scorpion in self.scorpions:
                        scorpion.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    return self.check_collisions()
            elif event.key == pygame.K_RIGHT:
                print("Pressed RIGHT")  # Debug
                if self.player.move("right", self.maze, self.walls):
                    for mummy in self.mummies:
                        mummy.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    for scorpion in self.scorpions:
                        scorpion.auto_move(self.player.row, self.player.col, self.maze, self.walls)
                    return self.check_collisions()

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