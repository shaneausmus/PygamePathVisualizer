import pygame

pygame.font.init()

class button: 
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        
        if self.text != '':
            btn_font = pygame.font.Font(None, 20)
            btn_text = btn_font.render(self.text, True, (0,0,0))
            window.blit(btn_text, (self.x + (self.width/2 - btn_text.get_width()/2), self.y + (self.height/2 - btn_text.get_height()/2)))
