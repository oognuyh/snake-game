# --------------------------------------------
#                 by oognuyh 
# --------------------------------------------
# TODO: need to fix some bugs
# screen delay loop - FIXED 19/11/24
# self.grid[body[0]][body[1]] = 1 => list index out of range - FIXED 19/11/24
# snake's structure have same coord like  [[27, 14], [28, 14], [28, 14], [28, 15]] - FIXED 19/11/25
# --------------------------------------------
import sys, os, random
import heapq
import pygame as pg
# --------------------------------------------
# pygame initialize
pg.init()
# center
os.environ['SDL_VIDEO_CENTERED'] = '1'
# set program title
pg.display.set_caption("snakegame")
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
cellsize = 20
gridwidth = width // cellsize
gridheight = height // cellsize
# --------------------------------------------
# define direction
UP = [0, -1]
DOWN = [0, 1]
LEFT = [-1, 0]
RIGHT = [1, 0]
DIRECTION = [UP, DOWN, LEFT, RIGHT]
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
    path = Finder(snake, feed).find()
    if not path: return # if no path, game over

    is_running = True

    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT: # terminate program
                is_running = False
                sys.exit() 
        
        screen.fill(BLACK) # fill background
        snake.draw() # draw the snake
        feed.draw() # draw the feed
        
        coord = path.pop()
        snake.move(coord) 
        if snake.structure[HEAD] == feed.coord: # if the snake ate the feed, set feed location randomly and find new path
            snake.grow()
            feed.randomly(snake.structure) # new feed
            path = Finder(snake, feed).find()
        
        if not path: # if no path, game over
            snake.draw()
            pg.display.flip()
            pg.time.wait(1500) # delay 
            is_running = False 

        pg.display.flip() # screen update
        pg.time.Clock().tick(FPS) # speed
# --------------------------------------------
class Element:
    # grid's detail 
    def __init__(self, coord):
        self.coord = coord
        self.parent = None # the coord's parent coord
        self.H = 0 # H cost
        self.G = 0 # G cost
        self.F = 0 # F cost = H cost + G cost

    def __lt__(self, other): # define operator <
        return self.F < other.F
    
    def __eq__(self, other): # define operator ==
        return self.coord == other.coord
    
class Finder: 
    # find the shortest path using A* algorithm
    def __init__(self, snake, feed):
        self.grid = [[0 for y in range(gridheight)] for x in range(gridwidth)] # wall = 1, path = 0
        for body in snake.structure: # check the snake's body
            self.grid[body[0]][body[1]] = 1
        self.head = snake.structure[HEAD] # same as starting point
        self.feed = feed.coord # same as end point
        self.open = [] # open list
        self.closed = [] # closed list
        heapq.heapify(self.open) # list into heap

    def is_valid(self, coord):
        x, y = coord # in range, not wall, not is in closed list
        return -1 < x and x < gridwidth and -1 < y and y < gridheight and not self.grid[x][y] and not self.is_in_closed(coord)

    def is_in_closed(self, coord):
        for exist in self.closed:
            if coord == exist.coord:
                return True
        return False

    def is_in_open(self, element):
        for exist in self.open:
            if exist == element: # if already exist, compare
                if exist > element:
                    exist = element
                return True
        return False

    def calculate_heuristic(self, coord):
        # calculate H cost using Manhattan distance(xDiff + yDiff)
        return (abs(coord[0] - self.feed[0]) + abs(coord[1] - self.feed[1])) * 10  

    def neighbors(self, obj):
        # visit neighbors(4 direction)
        up = add(obj.coord, UP)
        down = add(obj.coord, DOWN)
        right = add(obj.coord, RIGHT)
        left = add(obj.coord, LEFT)

        if self.is_valid(up):
            element = Element(up)
            element.parent = obj.coord
            element.G = obj.G + 10
            element.H = self.calculate_heuristic(element.coord)
            element.F = element.G + element.H
            if not self.is_in_open(element):
                heapq.heappush(self.open, element)

        if self.is_valid(down):
            element = Element(down)
            element.parent = obj.coord
            element.G = obj.G + 10
            element.H = self.calculate_heuristic(element.coord)
            element.F = element.G + element.H
            if not self.is_in_open(element):
                heapq.heappush(self.open, element)

        if self.is_valid(right):
            element = Element(right)
            element.parent = obj.coord
            element.G = obj.G + 10
            element.H = self.calculate_heuristic(element.coord)
            element.F = element.G + element.H
            if not self.is_in_open(element):
                heapq.heappush(self.open, element)

        if self.is_valid(left):
            element = Element(left)
            element.parent = obj.coord
            element.G = obj.G + 10
            element.H = self.calculate_heuristic(element.coord)
            element.F = element.G + element.H
            if not self.is_in_open(element):
                heapq.heappush(self.open, element)

    def find(self):
        flag = False
        path = []
        element = Element(self.head)
        heapq.heappush(self.open, element)
        while True:
            if len(self.open) == 0: break
            element = heapq.heappop(self.open)
            self.closed.append(element)
            if element.coord == self.feed: 
                flag = True
                break

            self.neighbors(element)

        if flag: # if Finder found the path, trace the parent coord
            while True:
                path.append(element.coord)
                if element.coord == self.head:
                    break

                for exist in self.closed:
                    if element.parent == exist.coord:
                        element = exist
                        break

        return path
            
class Snake:
    def __init__(self):
        x, y = gridwidth // 2, gridheight // 2 # initialize the snake's location
        self.structure = [[x, y], [x, y + 1], [x, y + 2], [x, y + 3]] # snake's head and body
        self.color = GREY # default color(body = grey, head = red)

    def move(self, coord):
        for body in range(len(self.structure) - 1, 0, -1):
            self.structure[body] = self.structure[body - 1]
        self.structure[HEAD] = coord

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
        grid = [[x, y] for x in range(gridwidth) for y in range(gridheight)]
        
        for direction in directions:
            if direction in grid:
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