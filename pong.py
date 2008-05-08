#!/usr/bin/env python
 
import states
import pygame
from pygame.constants import *
import versus
import campaign
 
def main():
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode( (640,480), DOUBLEBUF)
    
    driver = states.StateDriver(screen)
    title = TitleScreen(driver,screen)
    driver.start(title)
    driver.run()
 
class TitleScreen(states.State):
    
    def __init__(self,driver,screen):
        states.State.__init__(self,driver,screen)
        self.pongFont = pygame.font.Font(None,92)
        self.font = pygame.font.Font(None, 16)
    
    def paint(self,screen):
        white = (255, 255, 255)
        
        w,h = screen.get_size()
        surface = self.pongFont.render("Mongon",0, white)
        
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.25 - surface.get_height()/2
        
        screen.blit(surface, (centerX,centerY))
        
        surface = self.font.render("Balls. Splits. Bullits. Angrys.",0,(128,128,128))
        centerX = w/2 - surface.get_width()/2
        centerY = h/2 - surface.get_height()/2
        
        screen.blit(surface, (centerX, centerY))
        
        surface = self.font.render("Press 1 for One Player", 0, (255,128,128))
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.80 - surface.get_height()/2
        
        screen.blit(surface, (centerX, centerY))
        
        surface = self.font.render("Press 2 for Two Players", 0, (255,128,128))
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.85 - surface.get_height()/2
        
        screen.blit(surface, (centerX, centerY))
        
    def keyEvent(self,key,unicode,pressed):
	if key == K_q:
	    pygame.quit()
        elif(pressed and key == K_2):
            playing = versus.VersusGameState(self._driver,self.screen)
            self._driver.replace(playing)
        elif(pressed and key == K_1):
            playing = campaign.CampaignGameState(self._driver,self.screen)
            self._driver.replace(playing)
    
if __name__ == '__main__':
    main()
