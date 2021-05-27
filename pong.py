import numpy
import pygame
import sys

# Ball,bar speed 1-10
ball_speed = 10
bar_speed = 5

width = 600
height = 400
size = width, height
screen = pygame.display.set_mode(size)
pygame.init()
game_over = False
end_point = False
player1_score = 0
player2_score = 0
font = pygame.font.SysFont("Arial", 75)

def reset():
    global end_point
    end_point = True

def update_player1_score():
    global player1_score
    player1_score += 1

def update_player2_score():
    global player2_score
    player2_score += 1

class Ball:
    def __init__(self):
        self.x = width/2
        self.y = height/2
        self.xv = ball_speed
        self.yv = 0
        self.rad = 5

class Bar:
    def __init__(self, side):
        self.width = 10
        self.height = 70
        if (side == "left"):
            self.x = 0 + width/20
            self.y = height/2
        elif (side == "right"):
            self.x = width  - width/20 - self.width
            self.y = height/2


ball = Ball()
left_bar = Bar("left")
right_bar = Bar("right") 

def update_board():
    pygame.draw.rect(screen, (0,0,0), (0, 0, width, height))
    pygame.draw.rect(screen, (255,255,255), (width/2 + 2.5, 0, 5, height))
    pygame.draw.circle(screen, (255,255,255), (ball.x, ball.y), ball.rad)
    pygame.draw.rect(screen, (255, 255, 255), ( int(left_bar.x), int(left_bar.y - 35), left_bar.width , 70) )
    pygame.draw.rect(screen, (255, 255, 255), ( int(right_bar.x), int(right_bar.y - 35), right_bar.width , 70) )
    draw_score(player1_score, 1)
    draw_score(player2_score, 2)
    pygame.display.update()
    pygame.time.wait(40)

def init_board():
    global end_point
    global ball, left_bar, right_bar
    ball = Ball()
    left_bar = Bar("left")
    right_bar = Bar("right")
    end_point = False
    update_board()

def game_loop():
    ball.x += ball.xv
    ball.y += ball.yv
    detect_collision()
    update_board()

def draw_score(text, player):
    label = font.render(str(text), 1, (255,255,255))
    if player == 1:
        screen.blit(label, (width/2 - 65, 10))
    if player == 2:
        screen.blit(label, (width/2 + 40 , 10))

def update_velocity(bally, bary):
    ydiff = bary - bally
    ball.xv = -ball.xv + ydiff
    ball.yv += ydiff/ball_speed

def detect_collision():
    if (ball.x >= (right_bar.x) and (ball.y >= right_bar.y - right_bar.height/2 and ball.y <= right_bar.y + right_bar.height/2)):
        update_velocity(ball.y, right_bar.y)
    elif (ball.x <= (left_bar.x + left_bar.width) and (ball.y >= left_bar.y - left_bar.height/2 and ball.y <= left_bar.y + left_bar.height/2)):
        update_velocity(ball.y, left_bar.y)

    if (ball.y < ball_speed  or ball.y > height - ball_speed):
        ball.yv = -ball.yv

    if (ball.x == 0 or ball.x >= width):
        if (ball.x < ball_speed):
            update_player2_score() 
        else: 
            update_player1_score()
        reset()
        init_board()

def player2_update(dir):
    if right_bar.y - right_bar.height/2 >= 0 and right_bar.y + right_bar.height/2 <= height:
        right_bar.y += bar_speed * dir


def player1_update(dir):
    if left_bar.y - left_bar.height/2 >= 0 and left_bar.y + left_bar.height/2 <= height:
        left_bar.y += bar_speed * dir


update_board()

while not game_over:
    game_loop()

    keys = pygame.key.get_pressed()  
    if keys[pygame.K_UP]:
        player2_update(-1)
    if keys[pygame.K_DOWN]:
        player2_update(1)
    if keys[ord('w')]:
        player1_update(-1)
    if keys[ord('s')]:
        player1_update(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
    pass