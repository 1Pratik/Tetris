# !/usr/bin/env python

# game of tetris


from random import randrange as rd
import pygame
import sys

# configuration
config = {
    'cell_size': 20,
    'cols': 16,
    'rows': 20,
    'delay': 750,
    'maxfps': 30
}

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# shape of single parts
tetris_shape = [
    [[1, 1, 1], [0, 1, 0]],
    [[0, 2, 2], [2, 2, 0]],
    [[3, 3, 0], [0, 3, 3]],
    [[4, 0, 0], [4, 4, 4]],
    [[0, 0, 5], [5, 5, 5]],
    [[6, 6, 6, 6]],
    [[7, 7], [7, 7]]
]


# images icon, fighter, background
icon = pygame.image.load('images/GameIcon.png')
jetImage = pygame.image.load('images/fighter-plane.png')
backImage1 = pygame.image.load('images/background3.jpg')
backImage2 = pygame.image.load('images/RetroBackground.png')
backImage3 = pygame.image.load('images/sunnyday.png')
backImage4 = pygame.image.load('images/back1.png')


def new_board():
    board = [[0 for x in range(config['cols'])] for y in range(config['rows'])]
    board += [[1 for x in range(config['cols'])]]
    return board


def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0])-1, -1, -1)]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def join_matrices(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1


def remove_row(board, row):
    del(board[row])
    return [[0 for i in range(config['cols'])]] + board


class TetrisApp(object):
    def __init__(self):
        # initialize the pygame
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        pygame.key.set_repeat(250, 25)
        self.width = config['cell_size'] * config['cols']
        self.height = config['cell_size'] * config['rows']

        # set the dispay screen with height and width
        self.screen = pygame.display.set_mode((self.width, self.height))
        # pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.imageNo = 0
        self.score_value = 0

        self.init_game()

    def new_stone(self):
        self.stone = tetris_shape[rd(len(tetris_shape))]
        self.stone_x = int(config['cols']/2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()

    def show_score(self):
        # self.score_value += 1
        score = self.font.render("SCORE: "+str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (config['cols'] * 13, 10))

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image = pygame.font.Font(pygame.font.get_default_font(), 12).render(
                line, False, (255, 255, 255), (0, 0, 0))
            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2
            self.screen.blit(msg_image, (self.width // 2 - msgim_center_x,
                                         self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, colors[val], pygame.Rect((off_x + x) * config['cell_size'], (off_y+y) * config['cell_size'],
                                                                           config['cell_size'], config['cell_size']), 0)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > config['cols'] - len(self.stone[0]):
                new_x = config['cols'] - len(self.stone[0])
            if not check_collision(self.board, self.stone, (new_x, self.stone_y)):
                self.stone_x = new_x

    def fighter(self):
        print('fighter')

    def fighterMove(self, deltaX):
        print('move', deltaX)

    def fire(self):
        print('fire')

    def setImage(self):
        self.imageNo += 1
        if self.imageNo == 5:
            self.imageNo = 1

    def quit(self):
        self.center_msg("Exiting.......")
        pygame.display.update()
        sys.exit()

    def drop(self):
        if not self.gameover and not self.paused:
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrices(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.score_value += 10
                            self.board = remove_row(self.board, i)
                            break
                    else:
                        break

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def run(self):
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'DOWN': self.drop,
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game,
            'f': self.fire,
            'a': self.fighterMove(-1),
            's': self.fighterMove(+1),
            'b': self.setImage
        }

        self.gameover = False
        self.paused = False

        pygame.time.set_timer(pygame.USEREVENT+1, config['delay'])
        dont_burn_my_cpu = pygame.time.Clock()

        # Game loop
        while 1:
            self.screen.fill((0, 0, 0))
            # set background
            if self.imageNo == 1:
                self.screen.blit(backImage1, (0, 0))
            elif self.imageNo == 2:
                self.screen.blit(backImage2, (0, 0))
            elif self.imageNo == 3:
                self.screen.blit(backImage3, (0, 0))
            else:
                self.screen.blit(backImage4, (0, 0))

            self.screen.blit(jetImage, (0, 0))
            self.show_score()

            if self.gameover:
                self.center_msg("""Game Over! Press space to continue.....""")
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    self.draw_matrix(self.board, (0, 0))
                    self.draw_matrix(self.stone, (self.stone_x, self.stone_y))

            pygame.display.update()

            # pygame events are captured
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop()
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(config['maxfps'])


if __name__ == '__main__':
    App = TetrisApp()
    App.run()
