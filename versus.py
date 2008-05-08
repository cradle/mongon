from states import *
import gui
import random
import pygame
from pygame.constants import *
from done import GameOver
from objects import *
	
class VersusGameState(GuiState):
 
    def __init__(self,driver,screen):
        GuiState.__init__(self,driver,screen)
        random.seed(pygame.time.get_ticks())
        self.balls = []
        self.balls.append(Ball((320,150), (640,480)))

        for ball in self.balls:
            self.add(ball)
        
        self.player1 = Paddle( (10,0), (15,75), 480,(K_w, K_s, K_LSHIFT),(10,0),1 )
        self.player1.center()
        self.add(self.player1)
        
        self.score1 = Score((20,5))
        self.add(self.score1)

        self.player2 = Paddle( (630,0), (15,75), 480, (K_UP, K_DOWN, K_LEFT), (380,0),-1)
        self.player2.center()
        self.add(self.player2)
        
        self.score2 = Score((610,5))
        self.add(self.score2)

        self.laser = Laser((320,0))
        self.add(self.laser)
        
    def update(self,delay):
        GuiState.update(self,delay)

        for bullet in self.player1.bullets[:]:
            if bullet.collidesWithPaddle(self.player2):
                self.score2.setScore(self.score2.getScore() - 1)

            for ball in self.balls[:]:
                if bullet.collidesWithBall(ball,self):
                    self.score1.setScore(self.score1.getScore() + ball.value)

            if bullet.dead:
                self.player1.bullets.remove(bullet)

        for bullet in self.player2.bullets[:]:
            if bullet.collidesWithPaddle(self.player1):
                self.score1.setScore(self.score1.getScore() - 1)

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
            done = GameOver(self._driver,self.screen,
                            self.score1,self.score2)
            self._driver.replace(done)
        
    def keyEvent(self,key,unicode,pressed):
        GuiState.keyEvent(self,key,unicode,pressed)
	if key == K_q:
	    pygame.quit()
