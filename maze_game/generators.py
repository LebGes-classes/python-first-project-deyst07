import random


class ManualGenerator:
    """Собственный алгоритм генерации (Recursive Backtracker)."""

    def generate(self, maze) -> object:
        """Генерирует лабиринт с использованием рекурсивного вырезания.

        Args:
            maze: Объект MazeMap для модификации.

        Returns:
            Обновлённый объект MazeMap.
        """
        
        self._carve(maze.start.x, maze.start.y, maze)
        maze.grid[maze.exit.y][maze.exit.x] = 2
        
        return maze

    def _carve(self, cx, cy, maze) -> None:
        """Рекурсивно вырезает проходы из клетки (cx, cy).

        Args:
            cx: Текущая координата X.
            cy: Текущая координата Y.
            maze: Объект MazeMap.
        """
        
        maze.grid[cy][cx] = 0
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < maze.width and 0 < ny < maze.height:
                if maze.grid[ny][nx] == 1:
                    maze.grid[cy + dy // 2][cx + dx // 2] = 0
                    self._carve(nx, ny, maze)
