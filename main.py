import pygame as pg
from pygame import mixer
from random import randrange

#Postavke
WIN_SIZE = 800
FPS = 60
TITLE = "Jere Papić 4.D"

pg.init()
pg.font.init()
mixer.init()

TILE_SIZE = 40
RANGE = (TILE_SIZE // 2, WIN_SIZE - TILE_SIZE // 2, TILE_SIZE)
get_random_pos = lambda: [randrange(*RANGE), randrange(*RANGE)]

font = pg.font.SysFont("Arial", 36)

pickup_sound = mixer.Sound("pickup.wav")
game_over_sound = mixer.Sound("game_over.wav")

snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_pos()
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)

time, time_step = 0, 100

food = snake.copy()
food.center = get_random_pos()

SCREEN = pg.display.set_mode([WIN_SIZE] * 2)
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                snake_dir = (0, -TILE_SIZE)
            if event.key == pg.K_s:
                snake_dir = (0, TILE_SIZE)
            if event.key == pg.K_a:
                snake_dir = (-TILE_SIZE, 0)
            if event.key == pg.K_d:
                snake_dir = (TILE_SIZE, 0)
                
    score_text = font.render("Score: " + str(length - 1), True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)

    SCREEN.fill("BLACK")

    

    #Gubljenje
    self_eating = pg.Rect.collidelist(snake, segments[:-1]) != -1

    if snake.left < 0 or snake.right > WIN_SIZE or snake.top < 0 or snake.bottom > WIN_SIZE or self_eating:
        mixer.Sound.play(game_over_sound)
        snake.center, food.center = get_random_pos(), get_random_pos()
        length, snake_dir = 1, (0, 0)
        segments = [snake.copy()]
        
    #Provjeri hranu
    if snake.center == food.center:
        mixer.Sound.play(pickup_sound)
        food.center = get_random_pos()
        length += 1

    #Nacrtaj hranu
    pg.draw.rect(SCREEN, "RED", food)

    #Nacrtaj zmiju
    [pg.draw.rect(SCREEN, "GREEN", segment) for segment in segments]

    #Nacrtaj tekst
    SCREEN.blit(score_text, score_rect)
    
    #Kretanje zmije
    time_now = pg.time.get_ticks()
    if time_now - time > time_step:
        time = time_now
        snake.move_ip(snake_dir)
        segments.append(snake.copy())
        segments = segments[-length:]

    pg.display.flip()
    clock.tick(FPS)