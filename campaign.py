from states import *
import gui
import random
import pygame
import pong
from pygame.constants import *
import done
from objects import *
	
class CampaignGameState(GuiState):
 
    def __init__(self,driver,screen,level=0):
        GuiState.__init__(self,driver,screen)
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        random.seed(pygame.time.get_ticks())
        self.pongFont = pygame.font.Font(None,92)
        self.font = pygame.font.Font(None, 16)
        self.level = level
        self.balls = []
        self.balls.append(Ball((320,150), (640,480), 8-level))

        for ball in self.balls:
            self.add(ball)
        
        #self.player1 = Paddle( (10,0), (15,75), 480,(K_w, K_s, K_LSHIFT),(10,0),1 )
	self.player1 = MousePaddle( (10,0),(15,75), 480, (10,0), 1)
        self.player1.center()
        self.add(self.player1)
        
        self.score1 = Score((20,5))
        self.add(self.score1)

        #self.player2 = Paddle( (630,0), (15,75), 480, (K_UP, K_DOWN, K_LEFT), (380,0),-1)
        self.player2 = None
        if level < 4:
            self.player2 = AIPaddle( (630,0), (15,75), 480,
                                     self.balls, (460,0), -1, 75 + 75*self.level)
        else:
            self.player2 = BiffPaddle( (630,0), (15,75), 480,
                                       self.balls, (460,0), -1, 500 + 10*self.level)

        self.player2.center()
        self.add(self.player2)
        
        self.score2 = Score((600,5))
        self.add(self.score2)

        self.laser = Laser((320,0))
        self.add(self.laser)
        
    def update(self,delay):
        GuiState.update(self,delay)

        for bullet in self.player1.bullets[:]:
            bullet.collidesWithPaddle(self.player2)

            for ball in self.balls[:]:
                if bullet.collidesWithBall(ball,self):
                    self.score1.setScore(self.score1.getScore() + ball.value)

            if bullet.dead:
                self.player1.bullets.remove(bullet)

        for bullet in self.player2.bullets[:]:
            bullet.collidesWithPaddle(self.player1)

            for ball in self.balls[:]:
                if bullet.collidesWithBall(ball,self):
                    self.score2.setScore(self.score2.getScore() + ball.value)

            if bullet.dead:
                self.player2.bullets.remove(bullet)

        ballNum = 1
        for ball in self.balls[:]:
            self.player1.collidesWithBall(ball)
            self.player2.collidesWithBall(ball)
            self.laser.collidesWithBall(ball)

            for otherBall in self.balls[:ballNum]:
                ball.collidesWithBall(otherBall)

            ballNum += 1

            if ball.dead:
                b1 = Ball(ball.loc, (640,480), ball.generation+1)
                b2 = Ball(ball.loc, (640,480), ball.generation+1)
                self.balls.append(b1)
                self.balls.append(b2)
                self.add(b1)
                self.add(b2)
        
            score = 0
            if(ball.outOfBounds < 0):
                score = self.score2.getScore() + ball.damage
                self.score2.setScore(score)
            elif(ball.outOfBounds > 0):
                score = self.score1.getScore() + ball.damage
                self.score1.setScore(score)
                
            if(score):
                ball.dead = True

            if ball.dead:
                self.remove(ball)
                self.balls.remove(ball)
        
        if(len(self.balls) == 0):
            if self.score1.getScore() > self.score2.getScore(): 
                nextLevel = CampaignGameState(self._driver,self.screen,self.level+1)
            elif self.level > 0:
                nextLevel = CampaignGameState(self._driver,self.screen,self.level-1)
            else:
                nextLevel = done.GameOver(self._driver,self.screen, self.score1,self.score2)
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
            self._driver.replace(nextLevel)

    def paint(self, screen):
        w,h = screen.get_size()
        surface = self.pongFont.render("WORLD 1",0, (40, 40, 40))
        
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.1 - surface.get_height()/2
        
        screen.blit(surface, (centerX,centerY))
        surface = self.pongFont.render("LEVEL %s" % (self.level+1),0, (40, 40, 40))
        
        centerX = w/2 - surface.get_width()/2
        centerY = h*0.25 - surface.get_height()/2
        
        screen.blit(surface, (centerX,centerY))
        
        GuiState.paint(self,screen)
    
    def keyEvent(self, key, unicode, value):
	if key == K_q:
		title = pong.TitleScreen(self._driver, self.screen)
		self._driver.replace(title)
