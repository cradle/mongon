import pygame
from pygame.constants import *
 
from states import *
import mongon
 
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
            self.setMessage("Player 1 ams teh weiner!")
        else:
            self.setMessage("You lose!")
            
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
        
        surface = self.messageFont.render("Press (M)ongon", 0, (255,255,255))
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.75 - surface.get_height()/2
        
        screen.blit(surface, (centerX, centerY))
        
    def keyEvent(self,key,unicode,pressed):
        if(pressed and key == K_m):
            goplay = mongon.TitleScreen(self._driver,self.screen)
            self._driver.replace(goplay)
