from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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

# Базовый цвет
BASE_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self, body_color=BASE_COLOR, position=START_POSITION):
        """Конструктор класса GameObject."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки."""
        raise NotImplementedError


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, body_color=SNAKE_COLOR, position=START_POSITION):
        """Конструктор класса Snake."""
        super().__init__(body_color, position)
        self.length = 1
        self.position = position
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple:
        """Возвращает координаты первого квадрата змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку по полю."""
        new_x_coord = (
            self.get_head_position()[0] + (self.direction[0] * GRID_SIZE)
        )
        if 0 > new_x_coord or new_x_coord > (SCREEN_WIDTH - GRID_SIZE):
            new_x_coord = (new_x_coord % SCREEN_WIDTH)
        new_y_coord = (
            self.get_head_position()[1] + (self.direction[1] * GRID_SIZE)
        )
        if 0 > new_y_coord or new_y_coord > (SCREEN_HEIGHT - GRID_SIZE):
            new_y_coord = (new_y_coord % SCREEN_HEIGHT)
        new_head_position = (new_x_coord, new_y_coord)
        if new_head_position in self.positions:
            self.reset()
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def draw(self, surface):
        """Отрисовывает змейку на поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает состояние змейки в исходное положение."""
        self.length = 1
        self.positions = GameObject.start_position
        self.positions = [self.position]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывает Яблоко."""

    def __init__(self, body_color=APPLE_COLOR, position=START_POSITION):
        """Конструктор класса Apple."""
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайные координаты яблока."""
        self.position = (
            randint(0, int(SCREEN_WIDTH / GRID_SIZE - 1)) * GRID_SIZE,
            randint(0, int(SCREEN_HEIGHT / GRID_SIZE - 1)) * GRID_SIZE)
        return self.position

    def draw(self, surface):
        """Отрисовывает яблоко на поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиши и задает направление движения."""
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
    """Обрабатывает основной цикл игры."""
    pygame.init()
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    while True:
        record = 0
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        if apple.position in snake.positions:
            record += 1
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            apple.draw(screen)
        pygame.display.update()
        print(record)


if __name__ == '__main__':
    main()
