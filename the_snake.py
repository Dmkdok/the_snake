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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
       
    def __init__(self):
        """Метод инициализирует базовые атрибуты объекта."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None
        
    def draw(self):
        """Абстрактный метод, который предназначен для переопределения в дочерних классах."""    
        pass
        
class Apple(GameObject):
    body_color = (255, 0, 0)
      

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = (255, 0, 0)
    
    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE, randint(0, GRID_HEIGHT) * GRID_SIZE)
        return self.position
        
    # Метод draw класса Apple    
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None
        
    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
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
                self.positions.pop()
        
    # Метод draw класса Snake
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

     # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

     # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            
    def get_head_position(self):
        return self.positions[0]
    
    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        self.next_direction = None
        
# Функция обработки действий пользователя
def handle_keys(game_object):
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
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        # Проверка столкновения с яблоком
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()
         
        # Проверка столкновения с собой
        if len(set(snake.positions)) != len(snake.positions):
            snake.reset()
           
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

