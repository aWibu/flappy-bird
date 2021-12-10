import pygame
import sys
import random
from pygame.locals import *

#Game Variables
g = 0.6
bird_movement = 0
game_active = True
score = 0
final_score = 0
can_score = True
speed = 4
FPS = 50


def draw_floor():
    screen.blit(floor_surface,(floor_x,450))
    screen.blit(floor_surface,(floor_x+288,450))


def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (300,random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (300,random_height-130))
    return bottom_pipe,top_pipe


def move_pipe(pipes): 
    global speed ,t
    for pipe in pipes:
        pipe.centerx -= speed
        if score%5 == 0 and score!=0:
            speed += 0.003
        if game_active == False:
            speed = 4
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 400:   
           screen.blit(pipe_surface,pipe)   
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)


def check_collision(pipes):
    global score,can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            can_score = True
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 450:
        can_score = True
        hit_sound.play()
        return False

    return True


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'{str(int(score))}',True,(20,56,235))
        score_rect = score_surface.get_rect(center = (144,40))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        final_score_surface = game_font.render(f'Score: {int(final_score)}',True,(20,56,235))
        final_score_rect = final_score_surface.get_rect(center = (144,100))
        screen.blit(final_score_surface,final_score_rect)


def score_check():
    if pipe_list:
        global score,can_score
        for pipe in pipe_list: 
            if 96 < pipe.centerx < 103 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


def update_score(score,final_score):
    final_score = score
    return final_score 


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*4,1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50,bird_rect.centery))
    return new_bird, new_bird_rect


def welcome_screen():
    global floor_x
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE):
                return
            else:
                screen.blit(bg_surface,(0,0))
                screen.blit(game_over_surface,game_over_rect) 
                score_display('game_over')
        floor_x -= 2
        draw_floor()
        if floor_x <= -290:
            floor_x = 0
        screen.blit(floor_surface,(floor_x,450))
        pygame.display.update()
        clock.tick(FPS)


def gameplay(): 
    global game_active,bird_movement,pipe_list,floor_x,score,final_score,bird_index,bird_surface,bird_rect
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = 0
                    bird_movement -= 8
                    flap_sound.play()
                        
                if event.key == pygame.K_SPACE and game_active==False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (50,100)
                    score = 0
            
            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())
            
            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface,bird_rect = bird_animation() 

        screen.blit(bg_surface,(0,0)) 
    

        if game_active:
                
            #Bird
            bird_movement += g 
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement  
            screen.blit(rotated_bird,bird_rect)  
            game_active = check_collision(pipe_list)   
            
            #Pipes
            pipe_list = move_pipe(pipe_list)    
            draw_pipes(pipe_list)  

            #Score
            score_display('main_game') 
            score_check()
        else:
            screen.blit(game_over_surface,game_over_rect)
            final_score = update_score(score,final_score)
            score_display('game_over')

        #Floor
        floor_x -= 2
        draw_floor()
        if floor_x <= -290:
            floor_x = 0
        screen.blit(floor_surface,(floor_x,450))

        pygame.display.update()
        clock.tick(FPS)  





if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((288,512))
    clock = pygame.time.Clock()

    game_font = pygame.font.Font('04B_19.ttf',30)

    bg_surface = pygame.image.load('images/background.png')

    bird_downflap = pygame.image.load('images/bluebird-downflap.png').convert_alpha()
    bird_midflap = pygame.image.load('images/bluebird-midflap.png').convert_alpha()
    bird_upflap = pygame.image.load('images/bluebird-upflap.png').convert_alpha()
    bird_frames = [bird_downflap,bird_midflap,bird_upflap]
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    bird_rect = bird_surface.get_rect(center = (50,100))
    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP,300)


    floor_surface = pygame.image.load('images/base.png')
    floor_x = 0

    pipe_surface = pygame.image.load('images/pipe.png').convert_alpha()
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT 
    pygame.time.set_timer(SPAWNPIPE,900)   
    pipe_height = [200,240,260,280,320,360] 


    game_over_surface = pygame.image.load('images/message.png')
    game_over_rect = game_over_surface.get_rect(center = (144,256))

    # Game Sounds
    flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
    hit_sound = pygame.mixer.Sound('sound/sfx_bonk.mp3')
    score_sound = pygame.mixer.Sound('sound/sfx_point.wav') 
    while True:
        welcome_screen()
        gameplay()