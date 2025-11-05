import pygame
import random
import sys
from typing import Tuple

# Константы, которые требуются тестам
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Глобальные переменные, которые требуются тестам
# Инициализируем их сразу, чтобы тесты видели правильные типы
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(
        self,
        position: Tuple[int, int] = (0, 0),
        body_color: Tuple[int, int, int] = (255, 255, 255)
    ):
        """
        Инициализирует игровой объект.

        Args:
            position: начальная позиция объекта
            body_color: цвет объекта в формате RGB
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, которое змейка должна съесть."""

    def __init__(self, position: Tuple[int, int] = None):
        """Инициализирует яблоко."""
        super().__init__(position, (255, 0, 0))
        if position is None:
            self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(self, position: Tuple[int, int] = None):
        """Инициализирует змейку."""
        if position is None:
            position = (
                (GRID_WIDTH // 2) * GRID_SIZE,
                (GRID_HEIGHT // 2) * GRID_SIZE
            )

        super().__init__(position, (0, 255, 0))

        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            current_x, current_y = self.direction
            next_x, next_y = self.next_direction

            if (current_x, current_y) != (-next_x, -next_y):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]

        dir_x, dir_y = self.direction
        new_head_x = head_x + (dir_x * GRID_SIZE)
        new_head_y = head_y + (dir_y * GRID_SIZE)

        # Обработка прохождения через стены
        if new_head_x >= SCREEN_WIDTH:
            new_head_x = 0
        elif new_head_x < 0:
            new_head_x = SCREEN_WIDTH - GRID_SIZE
        if new_head_y >= SCREEN_HEIGHT:
            new_head_y = 0
        elif new_head_y < 0:
            new_head_y = SCREEN_HEIGHT - GRID_SIZE

        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self) -> Tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]


    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(
            (GRID_WIDTH // 2) * GRID_SIZE,
            (GRID_HEIGHT // 2) * GRID_SIZE
        )]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0],
                position[1],
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)


def handle_keys(snake: Snake) -> None:
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.display.set_caption("Изгиб Питона")

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
