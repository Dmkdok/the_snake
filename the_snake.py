from random import choice, randint, choice

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (26, 26, 28)

# Цвет границы ячейки
BORDER_COLOR = (15, 16, 18)

# Цвет яблока
APPLE_COLOR = (255, 59, 48)

# Цвет змейки
SNAKE_COLOR = (40, 205, 65)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self):
        """Метод инициализирует базовые атрибуты объектов."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw_cell(self, position, color=None):
        """Метод отрисовывает ячейку на игровом поле."""
        rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, color or self.body_color, rect)
        if not color:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """
        Абстрактный метод, который предназначен для переопределения
        в дочерних классах.
        """
        raise NotImplementedError


class Apple(GameObject):
    """Класс, представляющий яблоко в игре"""

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions=[]):
        """Метод случайным образом размещает яблоко на игровом поле"""
        while True:
            apple_x = randint(0, GRID_WIDTH) * GRID_SIZE
            apple_y = randint(0, GRID_HEIGHT) * GRID_SIZE
            self.position = (apple_x, apple_y)
            if (self.position not in snake_positions
                    and 0 < apple_x < SCREEN_WIDTH
                    and 0 < apple_y < SCREEN_HEIGHT):
                break
        return self.position

    def draw(self):
        """Метод отрисовывает яблоко на игровом поле"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, представляющий змейку в игре"""

    def __init__(self):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, управляющий движением змейки."""
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_head_x, new_head_y)

        if self.length > 2 and new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self):
        """Метод отрисовывает змейку на игровом поле."""
        # Отрисовка головы змейки
        self.draw_cell(self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает игру в начальное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """
    Функция обработки нажатий клавиатуры для изменения
    направления движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция, которая запускает игровой цикл."""
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой
        if len(set(snake.positions)) != len(snake.positions):
            snake.reset()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
