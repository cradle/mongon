import pygame
import sys
import gui # So we can have a common interface between gui stuff and state stuff
from  common import SubclassShouldImplement
from pygame.locals import *
 
class StateDriver:
    def __init__(self,screen):
        self._states = []
        self._screen = screen
 
    def done(self):
        self._states.pop()
        self.getCurrentState().reactivate()
 
    def getCurrentState(self):
        try:
            return self._states[len(self._states) - 1]
        except IndexError:
            raise SystemExit  # we're done if theren't any states left
 
    def getScreenSize(self):
        return self._screen.get_size()
 
    def quit(self):
        # Was 'raise SystemExit', but pychecker assumes any function that
        # unconditionally raises an exception is abstract
        sys.exit(0) 
 
    def replace(self, state):
        self._states.pop()
        self.start(state)
 
    def run(self):
        currentState = self.getCurrentState()
        lastRan = pygame.time.get_ticks()
        while(currentState):
            # poll queue
            event = pygame.event.poll()
            while(event.type != NOEVENT):
                if event.type == QUIT:
                    currentState = None
                    break
                elif event.type == KEYUP or event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        #currentState = None
                        #break
                        pass
                    if event.type == KEYUP:
                        currentState.maskEvent(event.key, None, 0)
                    if event.type == KEYDOWN:
                        currentState.maskEvent(event.key, event.unicode, 1)
                elif (event.type == MOUSEMOTION):
                    currentState.mouseEvent(event)
                elif (event.type == MOUSEBUTTONDOWN or
                    event.type == MOUSEBUTTONUP):
                        currentState.mouseEvent(event)
            
                event = pygame.event.poll()
            self._screen.fill( (0, 0, 0) )
            if currentState:
                currentState.paint(self._screen)
                
                curTime = pygame.time.get_ticks()
                elapsed = float(curTime-lastRan)/1000.0
                currentState.update(elapsed)
                lastRan = curTime
                
                currentState = self.getCurrentState()
                
                pygame.display.flip()
                pygame.time.delay(10);
 
    def start(self, state):
        self._states.append(state)
        self.getCurrentState().activate()
 
class State(gui.Keyable,gui.Mouseable):
    def __init__(self, driver,screen):
        gui.Keyable.__init__(self) # States listen to everything
        gui.Mouseable.__init__(self)
        self._driver = driver
        self.screen = screen
 
    def activate(self):
        pass
 
    # maskEvent is handled by Keyable
    
    def keyEvent(self,key,unicode,pressed):
        pass
        
    def paint(self,screen):
        raise SubclassShouldImplement
 
    def reactivate(self):
        pass
 
    def update(self, delay):
        pass
    
class GuiState(State):
    def __init__(self,driver, screen):
        State.__init__(self,driver,screen)
        self.paintables = []
        self.mouseables = []
        self.keyables = []
        self.updateables = []
        
    def add(self,item):
        # Add to the appropriate list(s) based on type
        if(isinstance(item,gui.Paintable)):
            self.paintables.append(item)
        if(isinstance(item,gui.Mouseable)):
            self.mouseables.append(item)
        if(isinstance(item,gui.Keyable)):
            self.keyables.append(item)
        if(isinstance(item,gui.Updateable)):
            self.updateables.append(item)
            
    def paint(self,screen):
        for paintable in self.paintables:
            paintable.paint(screen)
            
    def keyEvent(self,key,unicode,pressed):
        for keyable in self.keyables:
            keyable.keyEvent(key,unicode,pressed)
            
    def mouseEvent(self,event):
        x,y = event.pos
        for mouseable in self.mouseables:
            x1,y1 = mouseable.loc[0:2]
            try:
                w,h = mouseable.loc[2:4]
            except IndexError:
                w,h = self.screen.get_width(),self.screen.get_height()
            if ( x >= x1   and y >= y1 and
                 x <  x1+w and y <  y1+h):
                mouseable.mouseEvent(event)
                
    def update(self,delay):
        for updateable in self.updateables:
            updateable.update(delay)
