import pygame,sys
from pygame.locals import *

class Board_env:
    def __init__(self):
        self.square = 100
        self.radius = self.square//2 - 3 #radius of the circle in the game
        self.row = 6
        self.column = 7
        self.board = [[0 for x in range(self.column)] for y in range(self.row)]
        self.width = self.column * self.square
        self.height = (self.row+1) * self.square
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.count = 0

    def addToBoard(self, row, column, turn):
        self.board[row][column] = turn + 1
        self.count+=1

    def isValid(self, col): return self.board[0][col] == 0

    def nextFreeSpace(self, col):
        for i in range(self.row-1,-1,-1):
            if self.board[i][col] == 0: return i

    def drawCircle(self,r,c,colour):
        pygame.draw.circle(self.screen, colour, (c*self.square+self.square//2, r*self.square+self.square + self.square//2), self.radius)

    def drawBoard(self,winning_squares):
        colour = None
        for r in range(self.row):
            for c in range(self.column):
                if (r,c) in winning_squares: colr = green
                else: colr = blue
                pygame.draw.rect(self.screen, colr, (c* self.square, r*self.square+self.square, self.square, self.square))
                self.drawCircle(r,c,black)

        for r in range(self.row):
            for c in range(self.column):
                if self.board[r][c] == 1: colour = red
                elif self.board[r][c] == 2: colour = yellow
                if colour:
                    self.drawCircle(r,c,colour)
                    colour = None
        pygame.display.update()

class Game:
    def __init__(self):
        self.b = Board_env()
        self.turn = 0 # 0 for Red and 1 for Yellow
        self.winning_squares=[]
        self.clock = pygame.time.Clock()
        self.xPos = 120

    def _check_win(self, x, y, dx, dy):
        a = self.b.board
        if a[x][y] > 0 and a[x][y] == a[x + dx][y + dy] == a[x + 2 * dx][y + 2 * dy] == a[x + 3 * dx][y + 3 * dy]:
            self.winning_squares = [(x + i * dx, y + i * dy) for i in range(4)]

    def check_win(self):
        #check rows
        for c in range(self.b.column-3):
            for r in range(self.b.row):
                self._check_win(r, c, 0, 1)

        # Check column
        for c in range(self.b.column):
            for r in range(self.b.row-3):
                self._check_win(r, c, 1, 0)

        # check diagonal /
        for c in range(self.b.column-3):
            for r in range(self.b.row-3):
                self._check_win(r, c, 1, 1)

        # Check diagonal \
        for c in range(self.b.column-3):
            for r in range(3, self.b.row):
                self._check_win(r,  c, -1, 1)

    def move_circle_on_mouse_movement(self,xPos,col=None):
        if col: pygame.draw.rect(self.b.screen, col, (0,0, self.b.width, self.b.square))
        if self.turn == 0: #if red's turn:
             pygame.draw.circle(self.b.screen, red, (xPos, self.b.square//2), self.b.radius)
        else: #yellow's turn
             pygame.draw.circle(self.b.screen, yellow, (xPos, self.b.square//2), self.b.radius)

    def displayEndScreen(self):
        while True:
            event = pygame.event.wait()
            if event.type == QUIT: sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                a = Game()
                a.playGame()

    def playGame(self):
        while True:
            event = pygame.event.wait()
            if event.type == QUIT: sys.exit()
            if event.type == MOUSEMOTION:
                self.xPos = event.pos[0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.b.screen, black, (0,0, self.b.width, self.b.square))
                col = event.pos[0]//self.b.square
                if self.b.isValid(col):
                    row = self.b.nextFreeSpace(col)
                    self.b.addToBoard(row, col,self.turn)
                    self.check_win()
                    self.turn = (self.turn+1) % 2
            self.b.drawBoard(self.winning_squares)
            self.clock.tick(35)
            if self.winning_squares or self.b.count == (self.b.row * self.b.column): break
            if self.b.radius <= self.xPos <= self.b.width-self.b.radius: self.move_circle_on_mouse_movement(self.xPos,black)
            pygame.display.update()
        self.displayEndScreen()

blue = (0,0,255)
black = (0,0,0)
red= (255,0,0)
yellow = (255,255,0)
green = (0, 255, 0)
pygame.init()
pygame.display.set_caption('Connect Four')
g = Game()
g.playGame()
