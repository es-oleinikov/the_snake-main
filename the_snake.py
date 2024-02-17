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

    def __init__(self, body_color=BASE_COLOR):
        """Конструктор класса GameObject."""
        self.position = START_POSITION
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод отрисовки."""
        print(f'Вызван абстрактный метод класса {self.__class__.__name__}')
        raise NotImplementedError


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Конструктор класса Snake."""
        super().__init__(body_color)
        self.position = self.position
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты первого квадрата змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку по полю."""
        new_x_coord = ((self.get_head_position()[0]
                        + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH)
        new_y_coord = ((self.get_head_position()[1]
                        + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT)
        new_head_position = (new_x_coord, new_y_coord)
        if new_head_position in self.positions:
            self.reset()
        else:
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
        self.positions = [START_POSITION]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывает Яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
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


def handle_keys(game_object, record):
    """
    Обрабатывает нажатия клавиши и задает направление движения,
    изменяет скорость движения.
    """
    directions_comb = {
        (pygame.K_UP, RIGHT): UP,
        (pygame.K_UP, LEFT): UP,
        (pygame.K_DOWN, RIGHT): DOWN,
        (pygame.K_DOWN, LEFT): DOWN,
        (pygame.K_RIGHT, UP): RIGHT,
        (pygame.K_RIGHT, DOWN): RIGHT,
        (pygame.K_LEFT, UP): LEFT,
        (pygame.K_LEFT, DOWN): LEFT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            save_record(record)
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            combination = (event.key, game_object.direction)
            if combination in directions_comb:
                game_object.next_direction = directions_comb[combination]
            elif event.key == pygame.K_PAGEUP:
                global SPEED
                SPEED += 5
            elif event.key == pygame.K_PAGEDOWN:
                if SPEED > 5:
                    SPEED -= 5
                else:
                    SPEED = 1


def save_record(record):
    """Выводит рекорд сессии и сохраняет в файл"""
    message = f'Session record: {record}.'
    print(message)
    with open('records.txt', 'a') as r:
        r.write(message)


def main():
    """Обрабатывает основной цикл игры."""
    pygame.init()
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    record = 0
    while True:
        clock.tick(SPEED)
        handle_keys(snake, record)
        snake.update_direction()
        snake.move()
        snake.draw(screen)
        apple.draw(screen)
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
            apple.draw(screen)
        if snake.length > record:
            record = snake.length
        pygame.display.update()


if __name__ == '__main__':
    main()
