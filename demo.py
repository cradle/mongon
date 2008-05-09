from campaign import *
	
class DemoGameState(GameState):
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
