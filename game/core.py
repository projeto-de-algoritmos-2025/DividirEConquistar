import pygame
import random
import time
from constants import *

pygame.init()
FONT = pygame.font.SysFont("arial", 24)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Invaders")

original_enemies = [(i+1, ENEMY_COLORS[i]) for i in range(NUM_ENEMIES)]
enemies = random.sample(original_enemies, NUM_ENEMIES)

cannon_pos = NUM_ENEMIES // 2
cannon_y = HEIGHT - 60

bullet_active = False
bullet_y = cannon_y

start_time = time.time()
record_times = []

reveal_values = False
reveal_start_time = None
reveal_count = 0

inversion_timer = 0
last_check = time.time()

lives = INITIAL_LIVES 


def reset_game():
    global enemies, cannon_pos, bullet_active, bullet_y
    global start_time, reveal_values, reveal_start_time, reveal_count
    global inversion_timer, last_check

    enemies = random.sample(original_enemies, NUM_ENEMIES)
    cannon_pos = NUM_ENEMIES // 2
    bullet_active = False
    bullet_y = cannon_y
    start_time = time.time()
    reveal_values = False
    reveal_start_time = None
    reveal_count = 0
    inversion_timer = 0
    last_check = time.time()


def count_inversions(arr):
    values = [x[0] for x in arr]

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, inv_left = merge_sort(arr[:mid])
        right, inv_right = merge_sort(arr[mid:])
        merged, inv_split = merge_and_count(left, right)
        return merged, inv_left + inv_right + inv_split

    def merge_and_count(left, right):
        result = []
        i = j = inv_count = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                inv_count += len(left) - i
                j += 1
        result += left[i:]
        result += right[j:]
        return result, inv_count

    _, total_inversions = merge_sort(values)
    return total_inversions


def draw_game():
    global reveal_values, reveal_start_time

    WIN.fill(BLACK)
    spacing = WIDTH // (NUM_ENEMIES + 1)

    if reveal_values and reveal_start_time:
        if time.time() - reveal_start_time >= REVEAL_DURATION:
            reveal_values = False
            reveal_start_time = None

    for i, (val, color) in enumerate(enemies):
        x = (i + 1) * spacing
        y = HEIGHT // 2
        pygame.draw.circle(WIN, color, (x, y), 30)
        if reveal_values:
            text = FONT.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=(x, y))
            WIN.blit(text, text_rect)

    cannon_x = (cannon_pos + 1) * spacing
    pygame.draw.rect(WIN, GREEN, (cannon_x - 20, cannon_y, 40, 20))

    if bullet_active:
        pygame.draw.rect(WIN, WHITE, (cannon_x - 5, bullet_y, 10, 20))

    inv_count = count_inversions(enemies)
    elapsed_time = round(time.time() - start_time, 2)
    info = FONT.render(f"Inversões: {inv_count}", True, WHITE)
    timer = FONT.render(f"Tempo: {elapsed_time:.2f}s", True, WHITE)
    lives_text = FONT.render(f"Vidas: {lives}", True, WHITE)
    WIN.blit(info, (10, 10))
    WIN.blit(timer, (10, 40))
    WIN.blit(lives_text, (WIDTH - 120, 10))

    inst = FONT.render("Setas = mover | Espaço = atirar | R = revelar", True, WHITE)
    WIN.blit(inst, (10, HEIGHT - 30))

    pygame.display.update()


def victory_screen(time_taken):
    WIN.fill(BLACK)
    msg = FONT.render("Parabéns! Você venceu!", True, GREEN)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    WIN.blit(msg, rect)

    record_times.append(time_taken)
    record_times.sort()
    top_times = record_times[:5]

    for i, t in enumerate(top_times):
        txt = FONT.render(f"#{i+1}: {t:.2f}s", True, WHITE)
        WIN.blit(txt, (WIDTH // 2 - 60, HEIGHT // 2 - 20 + i * 30))

    continue_msg = FONT.render("Pressione a tecla enter para jogar novamente", True, WHITE)
    WIN.blit(continue_msg, (WIDTH // 2 - 180, HEIGHT // 2 + 160))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    reset_game()


def game_over():
    WIN.fill(BLACK)
    msg = FONT.render("GAME OVER! Muitos inimigos fora de ordem.", True, RED)
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WIN.blit(msg, rect)
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    exit()


def game_loop():
    global cannon_pos, bullet_active, bullet_y, reveal_values, reveal_start_time
    global reveal_count, inversion_timer, last_check, enemies, lives

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        draw_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and cannon_pos > 0:
                    cannon_pos -= 1
                if event.key == pygame.K_RIGHT and cannon_pos < NUM_ENEMIES - 2:
                    cannon_pos += 1
                if event.key == pygame.K_SPACE and not bullet_active:
                    bullet_active = True
                    bullet_y = cannon_y
                if event.key == pygame.K_r and reveal_count < MAX_REVEALS:
                    reveal_values = True
                    reveal_start_time = time.time()
                    reveal_count += 1

        if bullet_active:
            bullet_y -= 10
            if bullet_y <= HEIGHT // 2:
                bullet_active = False
                enemies[cannon_pos], enemies[cannon_pos + 1] = enemies[cannon_pos + 1], enemies[cannon_pos]

        if count_inversions(enemies) == 0:
            victory_screen(round(time.time() - start_time, 2))

        now = time.time()
        if now - last_check >= 1:
            inversions = count_inversions(enemies)
            if inversions > inversion_limit:
                inversion_timer += 1
            else:
                inversion_timer = max(inversion_timer - 1, 0)
            last_check = now

            if inversion_timer >= MAX_INV_TIME:
                lives -= 1
                if lives <= 0:
                    game_over()
                else:
                    reset_game()

    pygame.quit()

