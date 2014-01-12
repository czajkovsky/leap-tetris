import pygame

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.row = 0
        self.col = 0

    def update(self, key, time, game_board):
        pass
        

class GameShape:
    def __init__(self, game_board, shape, image):
        self.pieces = []
        self.game_board = game_board
        self.shape = shape
        self.shape_rotation = 1
        self.last_move = 0
        self.active = True
        self.can_move = True
        self.fill_pieces(image)
        self.make_shape()

    def make_shape(self):
        if self.shape == 1:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#     00
            self.pieces[1].col = 7#      0
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 8
        if self.shape == 2:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#     0
            self.pieces[1].col = 7#     0
            self.pieces[2].row = 2#     0
            self.pieces[2].col = 7
            self.pieces[3].row = 3
            self.pieces[3].col = 7
        if self.shape == 3:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#     0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 7
        if self.shape == 4:
            self.pieces[0].row = 0
            self.pieces[0].col = 6#     00
            self.pieces[1].row = 0#     00
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 6
            self.pieces[3].row = 1
            self.pieces[3].col = 7
        if self.shape == 5:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#    00
            self.pieces[1].col = 7#    0  
            self.pieces[2].row = 1
            self.pieces[2].col = 6
            self.pieces[3].row = 2
            self.pieces[3].col = 6
        if self.shape == 6:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#    0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 6
        if self.shape == 7:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#      0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 8
            
    def fill_pieces(self, image):
        self.pieces.append(GamePiece(image))
        self.pieces.append(GamePiece(image))
        self.pieces.append(GamePiece(image))
        self.pieces.append(GamePiece(image))

    def update(self, time):
        pass

    def rotate(self):
        if self.shape == 1:
            self.rotate_shape_1()
            return
        if self.shape == 2:
            self.rotate_shape_2()
            return
        if self.shape == 3:
            self.rotate_shape_3()
            return
        if self.shape == 4:
            return
        if self.shape == 5:
            self.rotate_shape_5()
            return
        if self.shape == 6:
            self.rotate_shape_6()
        if self.shape == 7:
            self.rotate_shape_7()

    def set_row_offset(self):
        flag_offset = False
        for gp in self.pieces:
            if gp.row > 0:
                flag_offset = True
            else:
                flag_offset = False
                return
        if flag_offset:
            for gp in self.pieces:
                gp.row -= 1
                
    def set_col_offset(self):
        col_index = []
        gp_cols = 0
        for gp in self.pieces:
            if gp.col not in col_index:
                col_index.append(gp.col)
                gp_cols += 1
        if 6 not in col_index and self.shape != 2:
            for gp in self.pieces:
                gp.col -= 1
                    
    def move_left(self):
        flag = False
        for gp in self.pieces:
            if gp.col > 0:
                if self.game_board.cells[gp.row][gp.col-1].active:
                    flag = True
            if gp.col == 0:
                flag = True
        if flag:
            return
        else:
            for gp in self.pieces:
                gp.col -= 1
                
    def move_right(self):
        flag = False
        for gp in self.pieces:
            if gp.col != self.game_board.cols - 1:
                if self.game_board.cells[gp.row][gp.col+1].active:
                    flag = True
            if gp.col == self.game_board.cols -1:
                flag = True
        if flag:
            return
        else:
            for gp in self.pieces:
                gp.col += 1
                
    def move_down(self):
        flag = False
        for gp in self.pieces:
            if gp.row < self.game_board.rows - 1:
                if self.game_board.cells[gp.row+1][gp.col].active:
                    flag = True
                    self.active = False
            if gp.row == self.game_board.rows - 1 or gp.row < 0:
                flag = True
                self.active = False
        if flag:
            return
        else:
            for gp in self.pieces:
                gp.row += 1

    def rotate_shape_1(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p1r = self.pieces[2].row
        p1c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].col -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].col += 2
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p1r
            self.pieces[2].col = p1c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_2(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row -= 2
            self.pieces[3].col += 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row += 2
            self.pieces[3].col -= 2
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_3(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 1
            self.pieces[3].col -= 1
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 1
            self.pieces[3].col += 1
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row += 1
            self.pieces[3].col += 1
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].row += 1
            self.pieces[3].col -= 1
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1

    def rotate_shape_4(self):
        pass

    def rotate_shape_5(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row += 2
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_6(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].col += 2
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row += 2
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].col -= 2
            
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1
                
    def rotate_shape_7(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].col -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].col += 2
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].row += 2
        for gp in self.pieces:
            if gp.col < 0 or gp.col > self.game_board.cols - 1:
                flag_rotate = True
                break
            if gp.row > self.game_board.rows - 1 or gp.row < 0:
                flag_rotate = True
                break
            
        if flag_rotate == False:
            for gp in self.pieces:
                if self.game_board.cells[gp.row][gp.col].active:
                    flag_rotate = True
                    break
                
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1
