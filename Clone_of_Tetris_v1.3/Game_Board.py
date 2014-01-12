import pygame, random
from Game_Piece import *
from pyButton import Button
from pyButton import EXIT_BUTTON
pygame.mixer.pre_init(44100, -16, 2, 2048)

pygame.init()

pygame.mixer.music.load('bg_music.ogg')
pygame.mixer.music.set_volume(0.3)

#remove_row_sound = pygame.mixer.Sound('vaporize_1.ogg')
#if not remove_row_sound:
    #pygame.event.post(pygame.QUIT)

screen_w = 651
screen_h = 651
screen = pygame.display.set_mode((screen_w,screen_h), 0, 32)
pygame.display.set_caption("Clone of Tetris")
font = pygame.font.SysFont("arial black", 16)

clock = pygame.time.Clock()
cell_image = pygame.image.load('cell1.png').convert()
cell_image.set_colorkey((255,0,255))
shape_1_image = pygame.image.load('shape_1_image.png').convert()
shape_1_image.set_colorkey((255,0,255))
shape_2_image = pygame.image.load('shape_2_image.png').convert()
shape_2_image.set_colorkey((255,0,255))
shape_3_image = pygame.image.load('shape_3_image.png').convert()
shape_3_image.set_colorkey((255,0,255))
shape_4_image = pygame.image.load('shape_4_image.png').convert()
shape_4_image.set_colorkey((255,0,255))
shape_5_image = pygame.image.load('shape_5_image.png').convert()
shape_5_image.set_colorkey((255,0,255))
shape_6_image = pygame.image.load('shape_6_image.png').convert()
shape_6_image.set_colorkey((255,0,255))
shape_7_image = pygame.image.load('shape_7_image.png').convert()
shape_7_image.set_colorkey((255,0,255))
game_over_image = pygame.image.load('game_over.png').convert()
game_over_image.set_colorkey((255,0,255))
board_bg = pygame.image.load('board_bg.png').convert()
queue_bg = pygame.image.load('queue_bg_color.png').convert()
side_bar = pygame.image.load('side_bar.png').convert()


class Pause_Button(Button):
    def __init__(self, parent, position = (300,300)):
        Button.__init__(self, parent, 'Start / Pause', pygame.image.load('start_stop_btn.png').convert(), position)
    def on_click(self):
        self.parent.paused = not self.parent.paused

class New_Game_Button(Button):
    def __init__(self, parent, position = (300,300)):
        Button.__init__(self, parent, 'New Game', pygame.image.load('new_game_btn.png').convert(), position)
    def on_click(self):
        self.parent.reset(pygame.time.get_ticks())

class Cell(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.active = False
        self.row = 0
        self.col = 0
        self.x = 0
        self.y = 0

class GameBoard:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cells = []
        self.buttons =[]
        self.rows = 21
        self.cols = 14
        self.cell_width = 31
        self.width = self.cell_width * self.cols
        self.cell_height = 31
        self.height = self.cell_height * self.rows
        self.current_gp = None
        self.next_gp = None
        self.queue_image = pygame.Surface((162, 162))
        self.show_grid = False
        self.game_speed = 1000
        self.last_strafe = 0
        self.slow_time = False
        self.key_down_flag = False
        self.key_left_flag = False
        self.key_right_flag = False
        self.strafe_rate = 50
        self.last_strafe = 0
        self.paused = False
        self.game_over = False
        self.lines_done = 0
        self.level = 1
        self.score = 0
        Pause_Button(self, ((self.cols+1)*self.cell_width, ((self.rows)*self.cell_height) - 45))
        New_Game_Button(self, ((self.cols+4)*self.cell_width, ((self.rows)*self.cell_height) - 45))
        
    def initialize(self,time):
        self.current_gp = None
        shape_id = random.randint(1,7)
        rand_rotate = random.randint(0,5)
        self.next_gp = GameShape(self, shape_id, self.get_shape_image(shape_id))
        for row in range(self.rows):
            self.cells.append([])
            for col in range(self.cols):
                new_cell = Cell(cell_image)
                new_cell.row = row
                new_cell.col = col
                new_cell.x = col*self.cell_height + self.x
                new_cell.y = row*self.cell_width + self.y
                new_cell.rect.topleft = (new_cell.x, new_cell.y)
                self.cells[row].append(new_cell)
        for x in range(rand_rotate):
            self.next_gp.rotate()
        self.next_gp.set_row_offset()
        self.generate_gp(time)

    def reset(self, time):
        self.paused = False
        self.current_gp = None
        shape_id = random.randint(1,7)
        rand_rotate = random.randint(0,5)
        self.next_gp = GameShape(self, shape_id, self.get_shape_image(shape_id))
        self.game_speed = 1000
        self.slow_time = False
        self.game_over = False
        self.lines_done = 0
        self.level = 1
        self.score = 0
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].active = False
                self.cells[row][col].image = cell_image
        for x in range(rand_rotate):
            self.next_gp.rotate()
        self.next_gp.set_row_offset()
        self.next_gp.set_col_offset()
        self.generate_gp(time)

    def generate_gp(self, time):
        self.key_down_flag = False
        self.key_left_flag = False
        self.key_right_flag = False
        shape_id = random.randint(1,7)
        rand_rotate = random.randint(0,5)
        self.current_gp = self.next_gp
        self.current_gp.last_move = time
        self.next_gp = GameShape(self, shape_id, self.get_shape_image(shape_id))
        for x in range(rand_rotate):
            self.next_gp.rotate()
        self.next_gp.set_row_offset()
        self.next_gp.set_col_offset()
        self.queue_image.fill((255,255,255))
        col_index = []
        row_index = []
        gp_rows = 0
        gp_cols = 0
        for gp in self.next_gp.pieces:
            if gp.row not in row_index:
                row_index.append(gp.row)
                gp_rows += 1
            if gp.col not in col_index:
                col_index.append(gp.col)
                gp_cols += 1
        x_offset = (self.queue_image.get_width()/2) - ((gp_cols * self.cell_width)/2)
        y_offset = (self.queue_image.get_height()/2) - ((gp_rows * self.cell_height)/2)
        self.queue_image.blit(queue_bg, (0,0))
        for gp in self.next_gp.pieces:
            if self.next_gp.shape == 2 and self.next_gp.shape_rotation == 1:
                x = x_offset
            else:
                x = x_offset + ((gp.col - 6) * self.cell_width)
            y = y_offset + (gp.row * self.cell_height)
            self.queue_image.blit(gp.image, (x, y))
        

    def update(self, time):
        if self.paused or self.game_over:
            return
        if self.current_gp.active:
            speed = self.game_speed
            if self.slow_time:
                speed = 1000
            if self.key_down_flag:
                speed = 25
            elif self.key_left_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_gp.move_left()
                    self.last_strafe = time
            elif self.key_right_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_gp.move_right()
                    self.last_strafe = time
            if time - self.current_gp.last_move >= speed:
                self.current_gp.move_down()
                self.current_gp.last_move = time
        else:
            for gp in self.current_gp.pieces:
                if gp.row <= 0:
                    gp.row = 0
                    self.game_over = True
                self.cells[gp.row][gp.col].active = True
                self.cells[gp.row][gp.col].image = gp.image
            self.check_rows()
            self.generate_gp(time)

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def check_rows(self):
        row_count = 0
        for row in range(self.rows):
            flag_row = True
            for col in range(self.cols):
                if self.cells[row][col].active:
                    flag_row = True
                    continue
                if not self.cells[row][col].active:
                    flag_row = False
                    break
            if flag_row:
                self.shift_row(row)
                row_count += 1
                self.lines_done += 1
        #if row_count >= 1:
            #remove_row_sound.play(0)
        self.score += pow(row_count,2)*100
        self.score += self.level * row_count * 20
            
        if self.lines_done >= (self.level*self.level)+(self.level*6):
            self.level += 1
            self.game_speed -= 65
            if self.game_speed < 100:
                self.game_speed = 100

    def shift_row(self, row_number):
        for row in range(row_number, 0, -1):
            for col in range(self.cols):
                self.cells[row][col].active = self.cells[row-1][col].active
                self.cells[row][col].image = self.cells[row-1][col].image

    def get_shape_image(self, shape_id):
        if shape_id == 1:
            return shape_1_image
        if shape_id == 2:
            return shape_2_image
        if shape_id == 3:
            return shape_3_image
        if shape_id == 4:
            return shape_4_image
        if shape_id == 5:
            return shape_5_image
        if shape_id == 6:
            return shape_6_image
        if shape_id == 7:
            return shape_7_image

    def game_over_prompt(self, surface):
        choice = False
        x = screen_w
        y = screen_h
        xx = game_over_image.get_width()
        yy = game_over_image.get_height()
        surface.blit(game_over_image, ((x - xx)/2, (y - yy)/2))
        pygame.display.flip()
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_n:
                        self.reset(pygame.time.get_ticks())
                        return True

    def draw(self, surface):
        surface.blit(board_bg, (0,0))
        surface.blit(side_bar, ((14*31),0))
        x = (self.cols + 1) * self.cell_width
        y = self.cell_height
        surface.blit(self.queue_image, (x,y))
        #pygame.draw.rect(surface, (0,0,0), ((x-1,y-1),(self.queue_image.get_width()+2, self.queue_image.get_height()+2)), 2)
        surface.blit(font.render("LEVEL: %d" %self.level, True, (255,255,255)), (x, (surface.get_height() - (20*font.get_height()))))
        surface.blit(font.render("LINES: %d" %self.lines_done, True, (255,255,255)), (x, (surface.get_height() - (19*font.get_height()))))
        surface.blit(font.render("SCORE: %d" %self.score, True, (255,255,255)), (x, (surface.get_height() - (18*font.get_height()))))
        font_w,font_h = font.size("NEXT")
        x += ((self.queue_image.get_width()/2) - (font_w/2))
        y -= font_h
        surface.blit(font.render("NEXT", True, (255,255,255)), (x,y))
        border_topx, border_topy = self.cells[0][0].rect.topleft
        border_btmx, border_btmy = self.cells[20][13].rect.bottomright
        pygame.draw.rect(surface, (0,0,0), ((border_topx,border_topy),(border_btmx+1,border_btmy)), 1)
        for item in self.cells:
            for cell in item:
                if self.show_grid:
                    surface.blit(cell.image, cell.rect.topleft)
                if cell.active:
                    surface.blit(cell.image, cell.rect.topleft)
        for gp in self.current_gp.pieces:
            gp_position = self.cells[gp.row][gp.col].rect.topleft
            surface.blit(gp.image, gp_position)
        for buttons in self.buttons:
            buttons.draw(surface)
        for buttons in self.buttons:
            buttons.draw(surface)
                            
