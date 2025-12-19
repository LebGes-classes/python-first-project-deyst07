import os
from engine import Game


def main():
    """Точка входа в игру Neon Runner."""
    # Активируем цвета в терминале Windows
    os.system('')
    game = Game()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nСистема отключена пользователем.")


if __name__ == "__main__":
    main()