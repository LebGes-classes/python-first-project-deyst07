class Colors:
    """Палитра для создания неоновой атмосферы."""

    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @staticmethod
    def colorize(text, color) -> str:
        """Применяет ANSI-цвет к тексту и сбрасывает форматирование.

        Args:
            text: Текст для окраски.
            color: ANSI-код цвета (например, Colors.CYAN).

        Returns:
            Строка с применённым цветом и сбросом в конце.
        """
        
        return f"{color}{text}{Colors.RESET}"


class Point:
    """Координаты точки на карте."""

    def __init__(self, x, y) -> None:
        """Инициализирует точку с координатами.

        Args:
            x: Горизонтальная координата (столбец).
            y: Вертикальная координата (строка).
        """
        
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        """Сравнивает две точки по координатам.

        Args:
            other: Объект для сравнения.

        Returns:
            True, если other — Point и координаты совпадают.
        """
        
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


class MazeMap:
    """Карта лабиринта."""

    def __init__(self, width, height) -> None:
        """Инициализирует карту лабиринта заданного размера.

        Размеры корректируются до нечётных.

        Args:
            width: Желаемая ширина.
            height: Желаемая высота.
        """
        
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        # 1 - стена, 0 - проход, 2 - выход
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.start = Point(1, 1)
        self.exit = Point(self.width - 2, self.height - 2)
