import time
from models import MazeMap, Point
from generators import ManualGenerator
from services import Renderer, InputHandler


class Game:
    """Основной игровой движок."""

    def __init__(self) -> None:
        """Инициализирует игру с начальными параметрами."""
        
        self.level = 1
        self.total_time = 0.0
        self.renderer = Renderer()
        self.input = InputHandler()

    def start(self) -> None:
        """Запускает основной цикл игры с меню."""
        
        while True:
            self.renderer.draw_menu(self.level)
            choice = self.input.get_key()
            if choice == '1':
                self._run_level()
            elif choice == '2':
                self.renderer.draw_exit(self.total_time, self.level - 1)
                self.input.get_key()
                
                break

    def _run_level(self) -> None:
        """Запускает и управляет одним уровнем.

        Размер уровня: 11 + 2 * текущий_уровень → 13, 15, ...
        """
        
        size = 11 + (self.level * 2)
        maze = MazeMap(size, size)
        ManualGenerator().generate(maze)
        player = Point(maze.start.x, maze.start.y)
        steps = 0
        start_t = time.time()

        while True:
            elapsed = time.time() - start_t
            self.renderer.draw_game(maze, player, steps, elapsed)
            if maze.grid[player.y][player.x] == 2:
                self.total_time += elapsed
                self.renderer.draw_level_complete(self.level, steps, elapsed)
                self.input.get_key()
                self.level += 1
                
                return

            key = self.input.get_key()
            if key == 'q' or key == 'й':
                self.total_time += elapsed
                
                return

            dx, dy = 0, 0
            if key in ('w', 'ц'):
                dy = -1
            elif key in ('s', 'ы'):
                dy = 1
            elif key in ('a', 'ф'):
                dx = -1
            elif key in ('d', 'в'):
                dx = 1

            new_x, new_y = player.x + dx, player.y + dy
            if 0 <= new_x < maze.width and 0 <= new_y < maze.height:
                if maze.grid[new_y][new_x] != 1:
                    player.x, player.y = new_x, new_y
                    steps += 1
                    