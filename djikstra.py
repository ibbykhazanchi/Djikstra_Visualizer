import pygame
import math
import heapq

#initialize game and window of game
pygame.init()
WIDTH = 800
WIN  = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DJIKSTRA's Path Finding Algorithm")

#colors 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#spot class (same as node)
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE
    
    def make_path(self):
        self.color = PURPLE
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        #down
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        #up
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        #right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        #left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def update_values(q, distances):
    for i in range(len(q)):
        dist, spot = q[i]
        x, y = spot.get_pos()
        dist = distances[x][y]
        q[i] = (dist, spot)
    return q

#performs algorithm
def algorithm(draw, grid, rows, start, end):

    #intialize distances and predecessors
    distances = []
    predecessors = []
    for i in range(rows):
        distances.append([])
        predecessors.append([])
        for j in range(rows):
            distances[i].append(math.inf)
            blankSpot = Spot(-1,-1,-1,-1)
            predecessors[i].append(blankSpot)
    
    #set source distance = 0
    i, j = start.get_pos()
    distances[i][j] = 0

    #intialize & build priority queue
    q = []
    for row in grid:
        for spot in row:
            if not spot.is_barrier(): 
                i, j = spot.get_pos()
                heapq.heappush(q, (distances[i][j], spot))
    
    f = open("glo.txt", 'w')

    #begin process    
    while not len(q) == 0:
        
        vDist, vSpot = heapq.heappop(q)
        vI, vJ = vSpot.get_pos()
        vSpot = grid[vI][vJ]
        if(vSpot == end):
            break

        for neighbor in vSpot.neighbors:
            nI, nJ = neighbor.get_pos()

            if distances[vI][vJ] + 1 < distances[nI][nJ]:
                distances[nI][nJ] = distances[vI][vJ] + 1
                predecessors[nI][nJ] = vSpot

        
        q = update_values(q, distances)
        heapq.heapify(q)

    eI, eJ = end.get_pos()
    if distances[eI][eJ] == math.inf:
        pygame.display.set_caption('THERE IS NO PATH!!')
        return
                      
    
    curr = end
    x,y = curr.get_pos()
    pred = predecessors[x][y]
    curr = pred
    count = 0
    while not curr == start:
        curr.make_path()
        x,y = curr.get_pos()
        pred = predecessors[x][y]
        curr = pred
        draw()
        count+=1
    pygame.display.set_caption("The shortest path is {} blocks".format(count))





#makes the 2-d array of nodes and puts spots in each designated index
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

#draws the gridlines
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#draws the grid with appropriate colors for each spot
def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

#gets index of the place where you clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap 

    return row, col

#main method
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:

        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()
                
                elif spot != end and spot != start:
                    spot.make_barrier()
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, ROWS, start, end)
                
                elif event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    pygame.display.set_caption("DJIKSTRA's Path Finding Algorithm")


    pygame.quit()

main(WIN, WIDTH)

