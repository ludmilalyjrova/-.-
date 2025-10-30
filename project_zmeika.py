import pygame
import random
import sys
from pygame.locals import *

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BOARD_BACKGROUND_COLOR = BLACK

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None):
        """
        Инициализация игрового объекта.

        Args:
            position: Позиция объекта (по умолчанию центр экрана)
            body_color: Цвет объекта
        """
        if position is None:
            position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для яблока в игре."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = RED
        self.randomize_position()

    def randomize_position(self):
        """Установка случайной позиции для яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока на поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Класс для змейки в игре."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.body_color = GREEN
        self.reset()
        self.last = None

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейки."""
        head = self.get_head_position()
        x, y = self.direction

        # Вычисление новой позиции головы с учетом телепортации
        new_x = (head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Проверка на столкновение с собой
        if new_position in self.positions[1:]:
            self.reset()
            return

        # Сохраняем последнюю позицию для стирания следа
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        # Добавляем новую голову
        self.positions.insert(0, new_position)

    def draw(self, surface):
        """Отрисовка змейки на поверхности."""
        # Стираем последний сегмент
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        # Отрисовываем все сегменты змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)

        # Отрисовываем голову другим цветом
        if self.positions:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLUE, head_rect)
            pygame.draw.rect(surface, WHITE, head_rect, 1)


def handle_keys(snake):
    """
    Обработка нажатий клавиш для управления змейкой.

    Args:
        snake: Объект змейки для управления
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    """Основная функция игры."""
    # Инициализация Pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона - Змейка')

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Основной игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появляется на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Контроль FPS
        clock.tick(10)  # 10 кадров в секунду


if __name__ == "__main__":
    main()
