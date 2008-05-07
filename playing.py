from states import *
import gui
 
import random, math
 
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

class Bullet(gui.Paintable, gui.Updateable):
    def __init__(self,loc,direction = 1, height=5,width=10):
        gui.Paintable.__init__(self,loc)
        self.direction = direction
        self.height = height
        self.width = width
        self.dead = False
        self.dx = 10 * self.direction
        self.loc = (loc[0] + self.width * self.direction + 5, loc[1])
        
    def paint(self,screen):
        topLeftX = self.loc[0] - (self.width / 2)
        topLeftY = self.loc[1] - (self.height / 2)
        rect = [topLeftX,topLeftY, self.width, self.height]
        pygame.draw.rect(screen, (0,0,255), rect)

    def update(self,delay):
        self.loc = (self.loc[0] + self.dx, self.loc[1])

    def rect(self):
        topLeftX = self.loc[0] - self.width / 2
        topLeftY = self.loc[1] - self.height / 2
        return Rect(topLeftX,topLeftY,self.width,self.height)
            
    def collidesWithBall(self,ball,player):
        if(self.rect().colliderect(ball.rect())):
            self.dead = True
            ball.dead = True
            return True

    def collidesWithPaddle(self,player):
        if(self.rect().colliderect(player.rect())):
            self.dead = True
            return True

class Laser(gui.Paintable, gui.Updateable):
    
    def __init__(self,loc,height=480,width=10):
        """The 'bounds' parameter indicates the width and height
        of the playing area"""
        gui.Paintable.__init__(self,loc)
        self.counterFont = pygame.font.Font(None, 36)
        self.height = height
        self.width = width
        self.angry = False
        self.counterImage = None
        self.clobberinTime = pygame.time.get_ticks() + random.randrange(10000,20000)
        
    def paint(self,screen):
        if self.angry:
            topLeftX = self.loc[0] - (self.width / 2)
            topLeftY = 0
            rect = [topLeftX,topLeftY, self.width, self.height]
            pygame.draw.rect(screen, (255,0,0), rect)
        if self.counterImage:
            screen.blit(self.counterImage, self.loc)

    def update(self,delay):
        timeLeft = self.clobberinTime - pygame.time.get_ticks()
        
        if timeLeft < 0:
            self.angry = True
            self.counterImage = self.counterFont.render("ANGRY",0,(255,255,255))
        elif timeLeft < 3000:
            self.counterImage = self.counterFont.render(str(timeLeft/1000+1),0,(255,255,255))
        else:
            self.counterImage = None
            
    def collidesWithBall(self,ball):
        if self.angry:
            topLeftX = self.loc[0] - self.width / 2
            topLeftY = 0
            ourRect = Rect(topLeftX,topLeftY,self.width,self.height)

            if(ourRect.colliderect(ball.rect())):
                ball.dead = True
                self.angry = False
                self.clobberinTime = pygame.time.get_ticks() + random.randrange(10000,20000)
                return True
            return False
            
            
class Ball(gui.Paintable, gui.Updateable):
    
    AXIS_X = 1
    AXIS_Y = 2
    
    def __init__(self,loc,bounds,generation=1):
        """The 'bounds' parameter indicates the width and height
        of the playing area"""
        gui.Paintable.__init__(self,loc)
        self.maxGenerations = 6
        if generation > self.maxGenerations:
            generation = self.maxGenerations
        self.generation = generation
        self.bounds = bounds
        self.radius = 32 / float(generation)
        self.speed = 50 + 45 * generation
        self.dead = False
        self.loc = list(loc)
        self.dx, self.dy = [random.random()*2.0-1.0,random.random()*1.0-0.5]
        self.normalise()
        self.colour = [(255,255,255),
                       (255,0,255),
                       (0,255,255),
                       (255,255,0),
                       (255,0,0),
                       (0,0,255)][generation-1]
        self.outOfBounds = 0
        self.value = (generation + 1) ** 2
        self.damage = (self.maxGenerations - generation + 1) ** 2

    def normalise(self):
        vel = [self.dx, self.dy]
        length = sum([v**2 for v in vel])
        vel = [a/math.sqrt(length) for a in vel]
        self.dx = vel[0]
        self.dy = vel[1]

    def length(array):
        '''Assuming array is nxmx...x2, return an array of the length of
        each vector.'''
        return math.sqrt(sum(array**2, -1))
    
    def normalize(array):
        return array/length(array)

    def rect(self):
        ballLeftX = self.loc[0] - self.radius
        ballLeftY = self.loc[1] - self.radius
        ballWidth = self.radius * 2
        ballHeight = self.radius * 2
        return Rect(ballLeftX,ballLeftY,ballWidth,ballHeight)
        
    def bounce(self, axis):
        if(axis & self.AXIS_X):
            self.dx = -self.dx
        if(axis & self.AXIS_Y):
            self.dy = -self.dy
        
        #self.speed = self.speed + self.speed * self.increase;
        
    def paint(self,screen):
        x = int(self.loc[0])
        y = int(self.loc[1])
        pygame.draw.circle(screen, self.colour, (x,y),self.radius)

    def update(self,delay):
        x,y = self.loc
        radius = self.radius
        toMove = delay * self.speed
        moveX = self.dx * toMove
        moveY = self.dy * toMove
        print moveX, self.radius
        
        newX = x + moveX
        newY = y + moveY
    
        if(newY < radius or newY > self.bounds[1] - radius):
            self.bounce(self.AXIS_Y)
            moveY = self.dy * toMove * 2
            newY = y + moveY
        if(newX < -radius):
            self.outOfBounds = -1
        elif(newX > self.bounds[0] + radius):
            self.outOfBounds = 1
            
        self.loc[0] = newX
        self.loc[1] = newY
        
class Paddle(gui.Paintable, gui.Keyable, gui.Updateable):
    
    def __init__(self,loc,size,maxY,keys=(K_UP, K_DOWN, K_RSHIFT),guiLoc=(10,0),direction=1,speed=300):
        gui.Keyable.__init__(self,keys)
        gui.Paintable.__init__(self,loc)
        self.guiLoc = guiLoc
        self.keys = keys
        self.upKey = keys[0]
        self.downKey = keys[1]
        self.shootKey = keys[2]
        self.size = size
        self.maxY = maxY
        self.dy = 0
        self.speed = speed
        self.center()
        self.reloadTime = 5000
        self.maxEnergy = self.reloadTime
        self.bulletEnergy = self.reloadTime / 5.0
        self.exhausted = False
        self.energy = 0
        self.bullets = []
        self.direction = direction
        
    def center(self):
        y = self.maxY / 2 - self.size[1] / 2
        self.loc = (self.loc[0],y)

    def rect(self):
        return Rect(self.topLeftX(),self.topLeftY(),self.size[0],self.size[1])

    def topLeftX(self):
        return self.loc[0] - self.size[0] / 2

    def topLeftY(self):
        return self.loc[1] - self.size[1] / 2
        
    def collidesWithBall(self,ball):
        # If ball moved more than radius last move, HACK IT
        while ball.loc[0] > self.topLeftX() and ball.loc[0] < self.topLeftX() + self.size[0] and \
              ball.loc[1] > self.topLeftY() and ball.loc[1] < self.topLeftY() + self.size[1]:
            ball.loc[0] -= ball.dx/abs(ball.dx) * ball.radius
            
        testX = ball.loc[0]
        testY = ball.loc[1]
        if testX < self.topLeftX():
            testX = self.topLeftX()
        if testX > (self.topLeftX() + self.size[0]):
            testX = (self.topLeftX() + self.size[0])
        if testY < self.topLeftY():
            testY = self.topLeftY()
        if testY > (self.topLeftY() + self.size[1]):
            testY = (self.topLeftY() + self.size[1])

        distanceBetween = ((ball.loc[0]-testX)*(ball.loc[0]-testX)+ \
                           (ball.loc[1]-testY)*(ball.loc[1]-testY))
        if distanceBetween < ball.radius*ball.radius:
            distanceBetween = math.sqrt(distanceBetween)
            normalVector = [ball.loc[0]-testX, ball.loc[1]-testY]
            if distanceBetween == 0:
                print "NOOOOOOOOOOOOO!!!!!!!!!!!!"
            normalisedNormalVector = [a/distanceBetween for a in normalVector]

            ball.loc[0] = ball.loc[0] + normalisedNormalVector[0] * (ball.radius - distanceBetween)
            ball.loc[1] = ball.loc[1] + normalisedNormalVector[1] * (ball.radius - distanceBetween)
            if normalisedNormalVector[0] != 0:
                ball.dx = math.fabs(ball.dx) * normalisedNormalVector[0]
            if normalisedNormalVector[1] != 0:
                ball.dy = math.fabs(ball.dy) * normalisedNormalVector[1]

            ball.normalise()
            return True
        return False
##        # http://www.2dgamecreators.com/tutorials/gameprogramming/collision/T1%20Collision2.html#mozTocId39150
        
    def update(self,delay):
        for bullet in self.bullets:
            bullet.update(delay)
                
        if self.energy < self.maxEnergy:
            self.energy += int(delay * 1000)

        if self.exhausted and self.energy >= self.maxEnergy:
            self.exhausted = False

        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy

        x,y = self.loc
        halfHeight = self.size[1]/2
        toMove = delay * self.speed
        moveY = self.dy * toMove
        
        newY = y + moveY
        if(newY < halfHeight or newY > self.maxY - halfHeight):
            return
        
        self.loc = (self.loc[0],newY)


    def shoot(self):
        if not self.exhausted:
            self.energy -= self.bulletEnergy
            self.bullets.append(Bullet(self.loc, self.direction))

        if self.energy <= 0:
            self.exhausted = True
            self.energy = 0
    
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
        elif(key == self.shootKey and pressed):
            self.shoot()
            
    def paint(self,screen):
        for bullet in self.bullets:
            bullet.paint(screen)
            
        topLeftX = self.loc[0] - (self.size[0] / 2)
        topLeftY = self.loc[1] - (self.size[1] / 2)
        rect = [topLeftX,topLeftY, self.size[0], self.size[1]]
        pygame.draw.rect(screen, (255,255,255), rect)

        topLeftX = self.guiLoc[0]
        topLeftY = self.guiLoc[1]
        rect = [topLeftX,topLeftY, self.energy/float(self.maxEnergy)*100, 10]
        pygame.draw.rect(screen, (255,0,0) if self.exhausted else (0,0,255), rect)

        
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
        random.seed(pygame.time.get_ticks())
        self.balls = []
        self.balls.append(Ball((320,240), (640,480)))

        for ball in self.balls:
            self.add(ball)
        
        self.player1 = Paddle( (10,0), (15,75), 480,(K_w, K_s, K_LSHIFT),(10,0),1 )
        self.player1.center()
        self.add(self.player1)
        
        self.score1 = Score((20,5))
        self.add(self.score1)

        self.player2 = Paddle( (630,0), (15,75), 480, (K_UP, K_DOWN, K_RSHIFT), (380,0),-1)
        #self.player2 = AIPaddle( (630,0), (15,75), 480,self.ball)
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

        for ball in self.balls[:]:
            self.player1.collidesWithBall(ball)
            self.player2.collidesWithBall(ball)
            self.laser.collidesWithBall(ball)

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
