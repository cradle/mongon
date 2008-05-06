import pygame
from pygame.constants import *
 
from states import *
 
class GameOver(State):
    
    def __init__(self,driver,screen,score1,score2):
        State.__init__(self,driver,screen)
        
        if(score1.getScore() > score2.getScore()):
            win = 1
        else:
            win = 0
            
        self.messageFont = pygame.font.Font(None,36)
        self.font = pygame.font.Font(None, 20)
            
        if(win):
            self.setMessage("You are victorious!")
        else:
            self.setMessage("You have lost!")
            
        self.score1 = score1
        self.score2 = score2
            
    def setMessage(self, message):
        self.message = message
        self.msgImage = self.messageFont.render(message, 0, (255,255,255))
        
    def paint(self,screen):
        w = screen.get_width()
        h = screen.get_height()
        
        surface = self.msgImage
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.25 - surface.get_height()/2
        screen.blit(surface, (centerX,centerY))
        
        surface = self.messageFont.render("to",0,(255,255,255))
        centerX = w/2 - surface.get_width()/2
        centerY = h/2 - surface.get_height()/2
        screen.blit(surface, (centerX,centerY))
        
        self.score1.loc = [30,centerY]
        self.score2.loc = [600,centerY]
        
        self.score1.paint(screen)
        self.score2.paint(screen)
