from campaign import * 
	
class World1GameState(GameState):
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
        ai.disableGun()
        return ai

