import pygame
from pygame.locals import *

class Button:
    def __init__(self, parent = None, name = 'NEW_BUTTON', image = None, position = (1,1), size = (80,28)):
        self.parent = parent
        self.name = name
        self.image = image
        self.x, self.y = position
        self.width, self.height = size
        if self.image is not None:
            self.width, self.height = self.image.get_size()
            self.image.set_colorkey((255,0,255))
        self.font = pygame.font.SysFont('arial', 15)
        self.font_w,self.font_h = self.font.size(name)
        self.rect = ((self.x,self.y),(self.width, self.height))
        parent.buttons.append(self)

    def set_name(self, name='NEW_NAME'):
        self.name = name
        self.font_w, self.font_h = self.font.size(name)

    def set_position(self, position = (1,1)):
        self.x, self.y = position

    def set_parent(self, parent_array):
        self.parent = parent_array

    def on_click(self):
        print self.name, ' clicked'

    def check_click(self, position):
        for x in range(self.x+1, self.x+self.width-1, 1):
            for y in range(self.y+1, self.y+self.height-1, 1):
                if position == (x,y):
                    self.on_click()

    def on_mouse_over(self):
        pass

    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image, (self.x,self.y))
        else:
            pygame.draw.rect(surface, (255,255,255), self.rect,0)
            surface.blit(self.font.render(self.name, True, (0,0,0)), (self.x+(self.width/2)-(self.font_w/2),self.y+(self.height/2)-(self.font_h/2)))

class EXIT_BUTTON(Button):
    def __init__(self, parent, position = (800-81,1)):
        Button.__init__(self, parent,'EXIT', None, position)

    def on_click(self):
        pygame.event.post(pygame.event.Event(QUIT))
