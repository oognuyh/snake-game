# --------------------------------------------
#                 by oognuyh
# --------------------------------------------
import sys, os, random
import pygame as pg
from pygame.locals import *
# --------------------------------------------
# pygame initialize
pg.init()
# set program title
pg.display.set_caption("basicsnakegame")
# set screen size and screen
width = 800
height = 800
screen = pg.display.set_mode((width, height))
# --------------------------------------------
SPLASHFONT = pg.font.Font("PrStart.ttf", 40)
GAMEOVERFONT = pg.font.Font("PrStart.ttf", 60)
# --------------------------------------------
# define colors
BLACK = (0, 0, 0)
GREY = (157, 157, 157)
YELLOW = (157, 157, 0)
RED = (157, 0, 0)
WHITE = (255, 255, 255)
# --------------------------------------------
# define FPS
FPS = 60
# --------------------------------------------
# set grid size 
cellsize = 40
gridwidth = width // cellsize
gridheight = height // cellsize
# --------------------------------------------
# define direction
UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]
# --------------------------------------------
# define snake's structure index
HEAD = 0
TAIL = -1
# --------------------------------------------
def splash():
    screen.fill(WHITE) # fill background
    obj = SPLASHFONT.render("SNAKE GAME", True, BLACK)# display 
    obj_rect = obj.get_rect()
    obj_rect.center = width // 2, height // 2
    screen.blit(obj, obj_rect)
    pg.display.flip() # update
    pg.time.wait(2000)# delay 2 sec

def gameover():
    screen.fill(WHITE) # fill background
    obj = GAMEOVERFONT.render("GAME OVER!!", True, BLACK)# display "GAME OVER"
    obj_rect = obj.get_rect()
    obj_rect.center = width // 2, height // 2
    screen.blit(obj, obj_rect)
    pg.display.flip() # update
    pg.time.wait(2000)# delay 2 sec
# --------------------------------------------
def game():
    # initialize
    snake = Snake()
    feed = Feed()
    feed.randomly(snake.structure)

    is_running = True

    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT: # terminate program
                is_running = False
                sys.exit() 
        
        if snake.is_dead(): is_running = False
        
        screen.fill(BLACK) # fill background
        snake.draw() # draw the snake
        feed.draw() # draw the feed

        keys = pg.key.get_pressed()
        if keys[K_UP]:
            snake.move(UP)
        elif keys[K_DOWN]:
            snake.move(DOWN)
        elif keys[K_LEFT]:
            snake.move(LEFT)
        elif keys[K_RIGHT]:
            snake.move(RIGHT)
        
        if snake.structure[HEAD] == feed.coord:
            feed.randomly(snake.structure)
            if not snake.grow():
                is_running = False
        
        pg.display.flip() # screen update
        pg.time.Clock().tick(FPS) # speed
# --------------------------------------------   
class Snake:
    def __init__(self):
        x, y = gridwidth // 2, gridheight // 2 # initialize the snake's location
        self.structure = [[x, y], [x, y + 1], [x, y + 2], [x, y + 3]] # snake's head and body
        self.color = GREY # default color(body = grey, head = red)

    def move(self, direction):
        coord = add(self.structure[HEAD], direction)
        if -1 < coord[0] and coord[0] < gridwidth and -1 < coord[1] and coord[1] < gridheight:
            if not coord in self.structure:
                for body in range(len(self.structure) - 1, 0, -1):
                    self.structure[body] = self.structure[body - 1]
                self.structure[HEAD] = coord
    
    def is_dead(self):
        head = self.structure[HEAD]
        
        up = add(head, UP)
        down = add(head, DOWN) 
        left = add(head, LEFT)
        right = add(head, RIGHT)

        directions = [up, down, left, right]

        around = 0

        for direction in directions:
            if -1 < direction[0] and -1 < direction[1] and direction[0] < gridwidth and direction[1] < gridheight:
                if direction not in self.structure:
                    around = around + 1

        return around == 0

    def grow(self):
        # when the snake ate the feed, add a body
        #      UP
        # LEFT T RIGHT
        #     DOWN
        tail = self.structure[TAIL]
        
        up = add(tail, UP)
        down = add(tail, DOWN) 
        left = add(tail, LEFT)
        right = add(tail, RIGHT)

        directions = [up, down, left, right]
        possible = []

        for direction in directions:
            if -1 < direction[0] and -1 < direction[1] and direction[0] < gridwidth and direction[1] < gridheight:
                if direction not in self.structure:
                    possible.append(direction)
              
        if not possible: return False
        
        self.structure.append(random.choice(possible))
        
        return True

    def draw(self):
        head = self.structure[HEAD] 
        for s in self.structure: # draw the snake
            pg.draw.rect(screen, self.color, (s[0] * cellsize, s[1] * cellsize, cellsize, cellsize))
        pg.draw.rect(screen, RED, (head[0] * cellsize, head[1] * cellsize, cellsize, cellsize)) # draw the snake's head

class Feed:
    def __init__(self):
        self.coord = None
        self.color = YELLOW
    
    def randomly(self, structure):
        possible = [[x, y] for x in range(gridwidth) for y in range(gridheight)]
        for exist in structure: # remove the snake's coordinates
            if exist in possible:
                possible.remove(exist)

        self.coord = random.choice(possible)

    def draw(self):
        x, y = self.coord
        pg.draw.rect(screen, YELLOW, (x * cellsize, y * cellsize, cellsize, cellsize)) # draw the feed

# --------------------------------------------
def add(one, another):
    result = []
    for a, b in zip(one, another):
        result.append(a + b)
    
    return result
# --------------------------------------------
if __name__ == "__main__":
    splash() # display splash
    
    is_running = True
    while is_running:
        game() # run game
        gameover() # display gameover