import os
import sys
from typing import Optional
from models import Colors


class Renderer:
    """Визуальное оформление игры."""

    def clear(self) -> None:
        """Очищает консоль в зависимости от ОС."""
        
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_menu(self, level) -> None:
        """Отображает главное меню.

        Args:
            level: Текущий номер уровня.
        """
        
        self.clear()
        c = Colors.CYAN
        
        print(Colors.colorize("  ◢" + "■" * 32 + "◣", c))
        print(Colors.colorize("  █      ", c) + Colors.colorize("N E O N   R U N N E R", Colors.BOLD + Colors.YELLOW) + Colors.colorize("      █", c))
        print(Colors.colorize("  ◥" + "■" * 32 + "◤", c))
        print(f"\n      СТАТУС: {Colors.colorize('ONLINE', Colors.GREEN)}")
        print(f"      ЭТАП:   {Colors.colorize(str(level), Colors.YELLOW)}")
        print(f"\n   [{Colors.colorize('1', Colors.MAGENTA)}] НАЧАТЬ")
        print(f"   [{Colors.colorize('2', Colors.MAGENTA)}] ВЫХОД")

    def draw_game(self, maze, player, steps, elapsed) -> None:
        """Отображает игровое поле в реальном времени.

        Args:
            maze: Карта лабиринта.
            player: Объект Point — позиция игрока.
            steps: Количество сделанных шагов.
            elapsed: Время прохождения уровня (в секундах).
        """
        
        self.clear()
        
        print(Colors.colorize("╔" + "══" * maze.width + "╗", Colors.CYAN))
        
        for y in range(maze.height):
            line = Colors.colorize("║", Colors.CYAN)
            for x in range(maze.width):
                if player.x == x and player.y == y:
                    line += Colors.colorize("⚉ ", Colors.YELLOW + Colors.BOLD)
                elif maze.grid[y][x] == 1:
                    color = Colors.BLUE if (x + y) % 2 == 0 else Colors.CYAN
                    line += Colors.colorize("▓▓", color)
                elif maze.grid[y][x] == 2:
                    line += Colors.colorize("◈ ", Colors.RED + Colors.BOLD)
                else:
                    line += "  "
        
            print(line + Colors.colorize("║", Colors.CYAN))
       
        print(Colors.colorize("╚" + "══" * maze.width + "╝", Colors.CYAN))
        
        stats = f" ШАГИ: {steps:03} | ВРЕМЯ: {elapsed:05.1f}s | [Q] МЕНЮ "
        
        print(Colors.colorize(stats.center(maze.width * 2 + 2), Colors.WHITE + Colors.BOLD))

    def draw_level_complete(self, level, steps, elapsed) -> None:
        """Поздравляет с прохождением уровня и выводит статистику.
        
        Args:
            level: Номер пройденного уровня.
            steps: Количество сделанных шагов.
            elapsed: Время прохождения уровня (в секундах).
        """
        
        self.clear()
        
        print(Colors.colorize("\n  Поздравляем! Уровень пройден!\n", Colors.GREEN + Colors.BOLD))
        print(Colors.colorize(f"  ЭТАП: {level}", Colors.CYAN))
        print(Colors.colorize(f"  Шагов затрачено: {steps}", Colors.YELLOW))
        print(Colors.colorize(f"  Время: {elapsed:.2f} сек", Colors.MAGENTA))
        print(Colors.colorize("\n  Нажмите любую клавишу для продолжения...", Colors.WHITE))

    def draw_exit(self, total_time, levels) -> None:
        """Отображает итоговый экран после завершения игры.

        Args:
            total_time: Общее время игры (в секундах).
            levels: Количество пройденных уровней.
        """
        
        self.clear()
        stars = Colors.colorize("★ " * 20, Colors.YELLOW)
        
        print(stars)
        print(Colors.colorize("\n          ИТОГИ СЕССИИ NEON RUNNER          ", Colors.CYAN + Colors.BOLD))
        print(f"\n      Пройдено уровней:   {Colors.colorize(str(levels), Colors.GREEN)}")
        print(f"      Общее время в сети: {Colors.colorize(f'{total_time:.2f}с', Colors.YELLOW)}")
        print("\n" + stars)


class InputHandler:
    """Низкоуровневый ввод без Enter."""

    def get_key(self) -> Optional[str]:
        """Считывает один символ ввода без эха.

        Поддерживает WASD, стрелки (в Unix), русские буквы (Ц/Ы/Ф/В) и Q/Й.

        Returns:
            Символ в нижнем регистре или None при ошибке.
        """
        if os.name == 'nt':
            import msvcrt
            
            
            key = msvcrt.getch()
            if key in [b'\x00', b'\xe0']:
                key = msvcrt.getch()
            try:
                
                return key.decode('cp866').lower()
            except Exception:
                
                return None
        else:
            import tty
            import termios
            
            
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                
                return sys.stdin.read(1).lower()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
