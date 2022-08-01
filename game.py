from turtle import delay
import pygame
pygame.font.init()
pygame.init()

SCORE_FONT = pygame.font.SysFont("comicsans", 30)
FPS = 60
GREEN = (0,100,0)
WHITE_SMOKE = (245,245,245) 
RED = (220,20,60)
BLACK = (105,105,105)
BLUE = (0,0,205)
DISPLAY_WIDTH, DISPLAY_HEIGHT = 1000, 900
WIN = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
WIDTH, HEIGHT = 15, 100
LEFT_OUT = pygame.USEREVENT + 1
RIGHT_OUT = pygame.USEREVENT + 2
WINNER_SCORE = 2

class Paddle:
    COLOR = GREEN
    VEL = 8
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
        
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        elif up==False:
            self.y += self.VEL

class Ball:
    COLOR = BLUE
    MAX_VEL = 8
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = - self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
def movement(keys_pressed, left_paddle, right_paddle):
    if keys_pressed[pygame.K_w] and left_paddle.y > 10:
        left_paddle.move(up=True)
    if keys_pressed[pygame.K_s] and left_paddle.height + left_paddle.y < DISPLAY_HEIGHT - 10:
        left_paddle.move(up=False)
    if keys_pressed[pygame.K_UP] and right_paddle.y > 10:
        right_paddle.move(up=True)
    if keys_pressed[pygame.K_DOWN] and right_paddle.y + right_paddle.height < DISPLAY_HEIGHT - 10:
        right_paddle.move(up=False)
        
def draw(left_paddle, right_paddle, ball, left_score, right_score):
    WIN.fill(WHITE_SMOKE)
    left_paddle.draw(WIN)
    right_paddle.draw(WIN)
    
    for i in range(0, DISPLAY_HEIGHT, DISPLAY_HEIGHT//20):
        if i % 2 == 0:
            continue
        pygame.draw.rect(WIN, GREEN, (DISPLAY_WIDTH//2 - 5, i - DISPLAY_HEIGHT//40, 10, DISPLAY_HEIGHT//20))
    #display score
    left_score_text = SCORE_FONT.render(f"SCORE: {left_score}", 1, GREEN)
    WIN.blit(left_score_text, (30, 10))
    right_score_text = SCORE_FONT.render(f"SCORE: {right_score}", 1, GREEN)
    WIN.blit(right_score_text, (DISPLAY_WIDTH - 30 - right_score_text.get_width(), 10))
    ball.draw(WIN)

    pygame.display.update()
    
def reset(ball):
    ball.x = ball.original_x
    ball.y = ball.original_y
    ball.x_vel *= -1
    ball.y_vel = 0 
    
def collision(ball, left_paddle, right_paddle):
    if ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.y + ball.radius >= DISPLAY_HEIGHT:
        ball.y_vel *= -1
    if ball.x - ball.radius <= 0:
        pygame.event.post(pygame.event.Event(LEFT_OUT))
        reset(ball)
    if ball.x + ball.radius >= DISPLAY_WIDTH:
        pygame.event.post(pygame.event.Event(RIGHT_OUT))
        reset(ball)
        
    if ball.y + ball.radius >= left_paddle.y and ball.y - ball.radius <= left_paddle.y + left_paddle.height:
        if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
            ball.x_vel *= -1
            middle_y = left_paddle.y + left_paddle.height/2
            reduction_factor = (middle_y - ball.y) / (middle_y - left_paddle.y)
            y_vel = ball.MAX_VEL * reduction_factor
            ball.y_vel = -1 * y_vel
                   
    if ball.y + ball.radius >= right_paddle.y and ball.y - ball.radius <= right_paddle.y + right_paddle.height:
        if ball.x  + ball.radius >= right_paddle.x:
            ball.x_vel *= -1
            middle_y = right_paddle.y + right_paddle.height/2
            reduction_factor = (middle_y - ball.y) / (middle_y - right_paddle.y)
            y_vel = reduction_factor * ball.MAX_VEL
            ball.y_vel = -1 * y_vel

def draw_winner(left_score, right_score):
    if left_score >= WINNER_SCORE:
        winner_text = SCORE_FONT.render("LEFT WINS!", 1, GREEN)
        WIN.blit(winner_text, (100, 100))
        pygame.display.update()
        pygame.time.delay(5000)
        main()
    
    elif right_score >= WINNER_SCORE:
        winner_text = SCORE_FONT.render("RIGHT WINS!", 1, GREEN)
        WIN.blit(winner_text, (DISPLAY_WIDTH - 100 - winner_text.get_width(), 100))
        pygame.display.update()
        pygame.time.delay(5000)
        main()
        

            
def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, DISPLAY_HEIGHT//2 - HEIGHT//2, WIDTH, HEIGHT)
    right_paddle = Paddle(DISPLAY_WIDTH - WIDTH - 10, DISPLAY_HEIGHT//2 - HEIGHT//2, WIDTH, HEIGHT)
    ball = Ball(DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, 9)
    left_score = 0
    right_score = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == LEFT_OUT:
                right_score += 1
            if event.type == RIGHT_OUT:
                left_score += 1
                
        keys_pressed = pygame.key.get_pressed()
        movement(keys_pressed ,left_paddle, right_paddle)
        ball.move()
        collision(ball, left_paddle, right_paddle)
        draw(left_paddle, right_paddle, ball, left_score, right_score)
        draw_winner(left_score, right_score)

                
                
if __name__ == "__main__":
    main()
                
                