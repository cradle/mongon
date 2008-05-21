import campaign
import mongon
import done
from objects import *

class CoopState(campaign.GameState):
    def __init__(self,driver,screen,level=0):
	campaign.GameState.__init__(self,driver,screen,level)
	self._player3 = self._initPlayer3()
	self.add(self._player3)

    def _initPlayer2(self):
        return Paddle( (35,0), (15,75), 480, (K_UP, K_DOWN, K_LEFT), (10,0),1)
    def _initPlayer3(self):
        return Paddle( (10,0), (15,75), 480,(K_w, K_s, K_LSHIFT),(10,0),1 )
    def _initPlayer1(self):
        return BiffPaddle( (630,0), (15,75), 480, self.balls, (460,0), -1, 200)

    def _backgroundText(self):
	return "COOP"
	
class TagGameState(campaign.GameState):
    def _initBalls(self):
        return TagBall((320,150), (640,480))

    def _initPlayer1(self):
        return MousePaddle( (10,0),(15,75), 480, (10,0), 1) 

    def _initPlayer2(self):
        return BiffPaddle( (630,0), (15,75), 480, self.balls, (460,0), -1, 200)

    def _backgroundText(self):
        return "RED VS BLUE"
	
class World1GameState(campaign.GameState):
    def _initLaser(self):
        return None

    def _initBalls(self):
        return Ball((320,150), (640,480), 8)

    def _initPlayer1(self):
        p1 = MousePaddle( (10,0),(15,75), 480, (10,0), 1)
        p1.disableGun()
        return p1 

    def _initPlayer2(self):
        ai = BiffPaddle( (630,0), (15,75), 480, self.balls, (460,0), -1, 200)
	ai.speed = 50 + 50 * self.level
        ai.disableGun()
        return ai
	
class DemoGameState(campaign.GameState):
    def _initBalls(self):
        return Ball((320,150), (640,480))

    def _initPlayer1(self):
        return AIPaddle( (10,0), (15,75), 480,
                                     self.balls, (10,0), 1)

    def _initPlayer2(self):
        return BiffPaddle( (630,0), (15,75), 480,
                                       self.balls, (460,0), -1)
        
    def _noBallsLeft(self):
        self.balls.append(Ball((320,150), (640,480)))

    def _backgroundText(self):
        return "DEMO MODE"
    
    def keyEvent(self, key, unicode, pressed):
        if(pressed):
            goplay = mongon.TitleScreen(self._driver,self.screen)
            self._driver.replace(goplay)
	
class VersusGameState(campaign.GameState):
 
    def _initBalls(self):
        return Ball((320,150), (640,480))

    def _initPlayer1(self):
        return Paddle( (10,0), (15,75), 480,(K_w, K_s, K_LSHIFT),(10,0),1 )

    def _initPlayer2(self):
        return Paddle( (630,0), (15,75), 480,(K_UP, K_DOWN, K_LEFT), (380,0),-1)

    def _noBallsLeft(self):
        godone = done.GameOver(self._driver,self.screen,
                        self.player1.score,self.player2.score)
        self._driver.replace(godone)

