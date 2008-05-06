from states import *
import gui
 
import random
 
import pygame
from pygame.constants import *
from done import GameOver
 
class Score(gui.Paintable):
    def __init__(self,loc):
        gui.Paintable.__init__(self,loc)
        self.scoreFont = pygame.font.Font(None, 36)
        self.setScore(0)
        
    def setScore(self,score):
        self.score = score
        white = (255,255,255)
        self.scoreImage = self.scoreFont.render(str(score),0,white)
        
    def getScore(self):
        return self.score
        
    def paint(self,screen):
        if(self.scoreImage and self.loc):
            screen.blit(self.scoreImage, self.loc)
            
class Ball(gui.Paintable, gui.Updateable):
    
    AXIS_X = 1
    AXIS_Y = 2
    
    def __init__(self,loc,bounds,radius=16,speed=110,increase=0.1):
        """The 'bounds' parameter indicates the width and height
        of the playing area"""
        gui.Paintable.__init__(self,loc)
        self.bounds = bounds
        self.radius = radius
        self.speed = speed
        self.increase = increase
        self.originalSpeed = speed
        self.dx = self.dy = 0
        self.center()
        
    def bounce(self, axis):
        if(axis & self.AXIS_X):
            self.dx = -self.dx
        if(axis & self.AXIS_Y):
            self.dy = -self.dy
        
        self.speed = self.speed + self.speed * self.increase;
            
    def center(self):
        self.loc = [self.bounds[0]/2, self.bounds[1]/2]
        self.dx = random.choice((-1,1))
        self.dy = random.choice((-1,1))
        self.outOfBounds = 0
        self.speed = self.originalSpeed
        
    def paint(self,screen):
        x = int(self.loc[0])
        y = int(self.loc[1])
        pygame.draw.circle(screen, (255,255,0), (x,y),self.radius)
        
    def update(self,delay):
        x,y = self.loc
        radius = self.radius
        toMove = delay * self.speed
        moveX = self.dx * toMove
        moveY = self.dy * toMove
        
        newX = x + moveX
        newY = y + moveY
    
        if(newY < radius or newY > self.bounds[1] - radius):
            self.bounce(self.AXIS_Y)
            moveY = self.dy * toMove * 2
            newY = y + moveY
        if(newX < radius):
            self.outOfBounds = -1
        elif(newX > self.bounds[0] - radius):
            self.outOfBounds = 1
            
        self.loc[0] = newX
        self.loc[1] = newY
        
class Paddle(gui.Paintable, gui.Keyable, gui.Updateable):
    
    def __init__(self,loc,size,maxY,keys=(K_UP, K_DOWN), speed=200):
        gui.Keyable.__init__(self,keys)
        gui.Paintable.__init__(self,loc)
        self.keys = keys
        self.upKey = keys[0]
        self.downKey = keys[1]
        self.size = size
        self.maxY = maxY
        self.dy = 0
        self.speed = speed
        self.center()
        
    def center(self):
        y = self.maxY / 2 - self.size[1] / 2
        self.loc = (self.loc[0],y)
        
    def collidesWithBall(self,ball):
        topLeftX = self.loc[0] - self.size[0] / 2
        topLeftY = self.loc[1] - self.size[1] / 2
        width = self.size[0]
        height = self.size[1]
        ourRect = Rect(topLeftX,topLeftY,width,height)
        
        ballLeftX = ball.loc[0] - ball.radius
        ballLeftY = ball.loc[1] - ball.radius
        ballWidth = ball.radius * 2
        ballHeight = ball.radius * 2
        ballRect = Rect(ballLeftX,ballLeftY,ballWidth,ballHeight)
        
        if(ourRect.colliderect(ballRect)):
            ball.bounce(Ball.AXIS_X)
            return True
        return False
        
    def update(self,delay):
        x,y = self.loc
        halfHeight = self.size[1]/2
        toMove = delay * self.speed
        moveY = self.dy * toMove
        
        newY = y + moveY
        if(newY < halfHeight or newY > self.maxY - halfHeight):
            return
        
        self.loc = (self.loc[0],newY)
    
    def keyEvent(self,key,unicode, pressed):
        if key not in self.keys:
            return
        
        if(key == self.upKey):
            if pressed:
                self.dy = -1
            else:
                if self.dy == -1:
                    self.dy = 0
        elif(key == self.downKey):
            if pressed:
                self.dy = 1
            else:
                if self.dy == 1:
                    self.dy = 0
            
    def paint(self,screen):
        topLeftX = self.loc[0] - (self.size[0] / 2)
        topLeftY = self.loc[1] - (self.size[1] / 2)
        rect = [topLeftX,topLeftY, self.size[0], self.size[1]]
        pygame.draw.rect(screen, (255,255,255), rect)
        
class AIPaddle(Paddle):
    def __init__(self,loc,size,maxY,ball,speed=125):
        Paddle.__init__(self,loc,size,maxY,speed)
        self.ball = ball
        
    def keyEvent(self,key,unicode,pressed):
        pass
    
    def update(self,delay):
        Paddle.update(self,delay)
        
        if(self.ball.loc[1] > self.loc[1] + 5):
            self.dy = 1
        elif(self.ball.loc[1] < self.loc[1] - 1):
            self.dy = -1
        else:
            self.dy = 0
        
class PlayingGameState(GuiState):
 
    def __init__(self,driver,screen):
        GuiState.__init__(self,driver,screen)
        self.ball = Ball(None, (640,480))
        self.ball.center()
        self.add(self.ball)
        
        self.player1 = Paddle( (10,0), (15,75), 480,(K_w, K_s) )
        self.player1.center()
        self.add(self.player1)
        
        self.score1 = Score((20,5))
        self.add(self.score1)

        self.player2 = Paddle( (630,0), (15,75), 480, (K_UP, K_DOWN))
        #self.player2 = AIPaddle( (630,0), (15,75), 480,self.ball)
        self.player2.center()
        self.add(self.player2)
        
        self.score2 = Score((610,5))
        self.add(self.score2)
        
    def update(self,delay):
        GuiState.update(self,delay)
        
        self.player1.collidesWithBall(self.ball)
        self.player2.collidesWithBall(self.ball)
        
        score = 0
        if(self.ball.outOfBounds < 0):
            score = self.score2.getScore() + 1
            self.score2.setScore(score)
        elif(self.ball.outOfBounds > 0):
            score = self.score1.getScore() + 1
            self.score1.setScore(score)
            
        if(score):
            self.ball.center()
            if(score >= 3):
                done = GameOver(self._driver,self.screen,
                                self.score1,self.score2)
                self._driver.replace(done)
