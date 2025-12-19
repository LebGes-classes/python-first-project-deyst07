import os
import random
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Colors:
    """
    Класс для управления ANSI-цветами в консоли.
    """

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """
        Оборачивает текст в цветовые коды.

        Args:
            text (str): Исходный текст.
            color (str): ANSI-код цвета.

        Returns:
            str: Раскрашенная строка.
        """

        return f"{color}{text}{Colors.RESET}"


class CellType(Enum):
    """
    Типы ячеек лабиринта и их строковые представления.
    """

    WALL = "██"
    PATH = "  "
    START = "ST"
    EXIT = "░░"
    PLAYER = "☻ "


@dataclass
class Point:
    """
    Представление точки в двумерном пространстве.
    """

    x: int
    y: int

    def __add__(self, other: 'Point') -> 'Point':
        """
        Складывает две точки.

        Args:
            other (Point): Другая точка.

        Returns:
            Point: Новая точка с суммированными координатами.
        """

        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает две точки на равенство.

        Args:
            other (object): Объект для сравнения.

        Returns:
            bool: True если координаты равны.
        """

        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y


class MazeMap:
    """
    Класс модели лабиринта. Хранит структуру игрового поля.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Инициализирует карту.

        Args:
            width (int): Ширина.
            height (int): Высота.
        """

        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = [
            [CellType.WALL for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.start = Point(1, 1)
        self.exit = Point(self.width - 2, self.height - 2)

    def is_within_bounds(self, p: Point) -> bool:
        """
        Проверяет, входит ли точка в границы массива.

        Args:
            p (Point): Точка.

        Returns:
            bool: Результат проверки.
        """

        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def get_cell(self, p: Point) -> CellType:
        """
        Получает тип ячейки в точке.

        Args:
            p (Point): Точка.

        Returns:
            CellType: Тип ячейки.
        """

        if self.is_within_bounds(p):
            return self.grid[p.y][p.x]

        return CellType.WALL

    def set_cell(self, p: Point, cell_type: CellType) -> None:
        """
        Устанавливает тип ячейки.

        Args:
            p (Point): Точка.
            cell_type (CellType): Тип.
        """

        if self.is_within_bounds(p):
            self.grid[p.y][p.x] = cell_type


class IMazeGenerator(ABC):
    """
    Абстрактный класс генератора.
    """

    @abstractmethod
    def generate(self, width: int, height: int) -> MazeMap:
        """
        Генерирует объект карты.

        Args:
            width (int): Ширина.
            height (int): Высота.

        Returns:
            MazeMap: Сгенерированная карта.
        """

        pass


class RecursiveBacktracker(IMazeGenerator):
    """
    Реализация генератора лабиринтов.
    """

    def generate(self, width: int, height: int) -> MazeMap:
        """
        Генерирует лабиринт алгоритмом DFS.

        Args:
            width (int): Ширина.
            height (int): Высота.

        Returns:
            MazeMap: Карта с путями.
        """

        maze = MazeMap(width, height)
        self._carve_passages(maze.start.x, maze.start.y, maze)
        maze.set_cell(maze.exit, CellType.EXIT)
        maze.set_cell(maze.start, CellType.START)

        return maze

    def _carve_passages(self, cx: int, cy: int, maze: MazeMap) -> None:
        """
        Рекурсивно прокладывает пути.

        Args:
            cx (int): Текущий X.
            cy (int): Текущий Y.
            maze (MazeMap): Ссылка на карту.
        """

        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        maze.set_cell(Point(cx, cy), CellType.PATH)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            neighbor = Point(nx, ny)

            if (maze.is_within_bounds(neighbor) and
                    maze.get_cell(neighbor) == CellType.WALL):
                wall_p = Point(cx + dx // 2, cy + dy // 2)
                maze.set_cell(wall_p, CellType.PATH)
                self._carve_passages(nx, ny, maze)


class Player:
    """
    Класс сущности игрока.
    """

    def __init__(self, start_pos: Point) -> None:
        self.position = start_pos

    def move(self, direction: Point, maze: MazeMap) -> bool:
        """
        Перемещает игрока.

        Args:
            direction (Point): Вектор движения.
            maze (MazeMap): Карта для проверки стен.

        Returns:
            bool: True если движение совершено успешно.
        """

        new_pos = self.position + direction
        if maze.get_cell(new_pos) != CellType.WALL:
            self.position = new_pos

            return True

        return False


class ConsoleRenderer:
    """
    Класс для отображения игры в консоли.
    """

    def clear(self) -> None:
        """Очищает экран."""

        os.system('cls' if os.name == 'nt' else 'clear')

    def render_menu(self, level: int) -> None:
        """
        Рисует меню.

        Args:
            level (int): Номер уровня.
        """

        self.clear()

        print(Colors.colorize("╔════════════════════════════╗", Colors.CYAN))

        print(Colors.colorize("║      NEON MAZE RUNNER      ║", Colors.BOLD + Colors.CYAN))

        print(f"║      УРОВЕНЬ: {level:<2}           ║")

        print(f"║  1. Начать игру            ║")

        print(f"║  2. Выход                  ║")

        print(Colors.colorize("╚════════════════════════════╝", Colors.CYAN))

    def render_game(self, maze: MazeMap, player: Player, steps: int, elapsed: float) -> None:
        """
        Рисует игровое поле, счетчик шагов и время.

        Args:
            maze (MazeMap): Карта.
            player (Player): Игрок.
            steps (int): Количество шагов.
            elapsed (float): Время в секундах.
        """

        self.clear()
        lines = []
        for y in range(maze.height):
            row = ""
            for x in range(maze.width):
                p = Point(x, y)
                cell = maze.get_cell(p)
                if p == player.position:
                    row += Colors.colorize(CellType.PLAYER.value, Colors.YELLOW)
                elif cell == CellType.WALL:
                    row += Colors.colorize(cell.value, Colors.BLUE)
                elif cell == CellType.EXIT:
                    row += Colors.colorize(cell.value, Colors.RED)
                else:
                    row += cell.value
            lines.append(row)

        print("\n".join(lines))

        time_str = f"{elapsed:.1f}с"

        print(f"Шаги: {Colors.colorize(str(steps), Colors.GREEN)} | "
              f"Время: {Colors.colorize(time_str, Colors.YELLOW)} | Q - Выход")

    def render_finish(self, steps: int, elapsed: float) -> None:
        """
        Рисует сообщение о прохождении уровня.

        Args:
            steps (int): Всего шагов.
            elapsed (float): Время прохождения.
        """

        self.clear()

        print(Colors.colorize("★ ★ ★ ПОЗДРАВЛЯЕМ! ★ ★ ★", Colors.YELLOW + Colors.BOLD))

        print(f"\nУровень пройден за {Colors.colorize(str(steps), Colors.GREEN)} шагов.")

        print(f"Время прохождения: {Colors.colorize(f'{elapsed:.2f}с', Colors.YELLOW)}")

        print("\nНажмите любую клавишу, чтобы продолжить...")

    def render_exit_thanks(self, total_time: float) -> None:
        """
        Рисует прощальное сообщение с итоговым временем.

        Args:
            total_time (float): Общее время в игре.
        """

        self.clear()

        print(Colors.colorize("Благодарим за игру в Neon Maze Runner!", Colors.CYAN + Colors.BOLD))

        print(f"Вы провели в лабиринтах суммарно: {Colors.colorize(f'{total_time:.2f}с', Colors.YELLOW)}")

        print(Colors.colorize("До скорых встреч!", Colors.CYAN))


class InputHandler:
    """
    Класс обработки ввода.
    """

    def get_key(self) -> Optional[str]:
        """
        Читает нажатую клавишу.

        Returns:
            Optional[str]: Символ клавиши.
        """

        if os.name == 'nt':
            import msvcrt
            raw = msvcrt.getch()
            if raw in (b'\x00', b'\xe0'):
                raw = msvcrt.getch()
            try:

                return raw.decode('cp866').lower()
            except UnicodeDecodeError:

                return None

        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)

            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


class GameEngine:
    """
    Главный контроллер игры.
    """

    def __init__(self) -> None:
        self.generator = RecursiveBacktracker()
        self.renderer = ConsoleRenderer()
        self.input = InputHandler()
        self.level = 1
        self.total_time = 0.0
        self.running = True

    def run(self) -> None:
        """Запускает основной цикл."""

        while self.running:
            self.renderer.render_menu(self.level)
            key = self.input.get_key()
            if key == '1':
                self._play_level()
            elif key == '2':
                self.renderer.render_exit_thanks(self.total_time)
                self.running = False

    def _play_level(self) -> None:
        """Запускает игровой цикл уровня с подсчетом шагов и времени."""

        size = 11 + (self.level * 2)
        maze = self.generator.generate(size, size)
        player = Player(maze.start)
        
        steps_count = 0
        start_time = time.time()

        while True:
            current_elapsed = time.time() - start_time
            self.renderer.render_game(maze, player, steps_count, current_elapsed)
            
            if player.position == maze.exit:
                self.total_time += current_elapsed
                self.renderer.render_finish(steps_count, current_elapsed)
                self.input.get_key()
                self.level += 1

                return

            cmd = self.input.get_key()
            if cmd == 'q':
                self.total_time += current_elapsed

                return

            move_map = {
                'w': Point(0, -1), 'ц': Point(0, -1),
                's': Point(0, 1), 'ы': Point(0, 1),
                'a': Point(-1, 0), 'ф': Point(-1, 0),
                'd': Point(1, 0), 'в': Point(1, 0)
            }

            if cmd in move_map:
                if player.move(move_map[cmd], maze):
                    steps_count += 1


if __name__ == "__main__":
    os.system('')
    GameEngine().run()