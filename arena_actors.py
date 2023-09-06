import random
import g2d_pygame as g2d

class Actor():
    '''Interface to be implemented by each game character
    '''
    def move(self):
        '''Called by Arena, at the actor's turn
        '''
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        '''Called by Arena, whenever the `self` actor collides with some
        `other` actor'''
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        '''Return the rectangle containing the actor, as a 4-tuple of ints:
        (left, top, width, height)
        '''
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        '''Return the position (x, y, w, h) of current sprite, if it is contained in
        a larger image, with other sprites. Otherwise, simply return (0, 0, 0, 0)
        '''
        raise NotImplementedError('Abstract method')

class Jumper(Actor):
    def move(self):
        raise NotImplementedError("abstract method")
    def position(self):
        raise NotImplementedError("abstract method")
    def symbol(self):
        raise NotImplementedError("abstract method")
    def collide(self,a):
        raise NotImplementedError("abstract method")
    
class Stable(Actor):
    def move(self):
        raise NotImplementedError("abstract method")
    def position(self):
        raise NotImplementedError("abstract method")
    def symbol(self):
        raise NotImplementedError("abstract method")
    def collide(self,a):
        raise NotImplementedError("abstract method")


class Wall(Stable):
    def __init__(self,arena,x,y):
        arena.add(self)
        self._x = x
        self._y = y
        self._w = 100
        self._h = 25
        
    def position(self):
        return self._x,self._y,self._w,self._h

    def move(self):
        pass
    
    def collide(self,other):
        pass
    
    def symbol(self):
        pass

        
        
    
class Booble(Jumper):
    def __init__(self,arena:object, pos: tuple , dx: int): #the dx of the ball is the same of the Dragon 
        arena.add(self)
        self._dx = dx
        self._x,self._y = pos
        self._counter = 0
        self._w, self._h = 20, 20
        
    def move(self):
        self._counter += 1
        self._x += self._dx * 3
        if self._counter >= 20:
            self._y -= 3
            
    def position(self):
        return self._x, self._y, self._w, self._h
        
    def symbol(self):
        return 0, 1200, self._w, self._h
    
    def collide(self,a):
        pass

        


class Dragon(Jumper):
    
    def __init__(self, arena:object, pos: tuple):
        self._x, self._y = pos
        self._w, self._h =  20, 18
        self._SPEED = 5
        self._dx, self._dy = 0, 0
        self._lives = 3
        self._arena = arena
        self._called = 0 # This variable is used  to avoid multiple jump in a single frame
        arena.add(self)
        self._landed = False
        self._g = 0.5

    def move(self):
        self._landed = False
        arena_w, arena_h = self._arena.size()
        self._called -= 0.25
        if self._called < 0:
            self._called = 0

        self._dy += self._g
        self._y += self._dy
        
        if self._y < 0:
            self._y = 0
        if self._y  > arena_h - self._h:
            self._y = arena_h  - self._h + 2 
            self._landed = True

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w
        


    def go_left(self):
        self._dx = -self._SPEED


    def go_right(self):
        self._dx = self._SPEED
   


    def go_up(self):
        arena_w, arena_h = self._arena.size()
        if (self._landed and self._called == 0):
            self._dy = -2*self._SPEED
            self._called = 1
            self._landed = False
        
         
                            
    def collide(self, other:object):
        arena_w, arena_h = self._arena.size()
        if isinstance(other, Wall) and self._dy > 0:
            wx, wy, ww, wh = other.position()
            px, py, pw, ph = self.position()
            previous_x, previous_y = px - self._dx, py - self._dy

            if previous_x + ww <= wx:
                self._x = wx - pw
            elif previous_x >= wx + ww:
                self._x = wx + ww
            elif previous_y + ph <= wy:
                self._y, self._dy = wy - ph, 1
                self._landed = True
            elif previous_y >= wy + wh:
                self._y, self._dy = wy + wh, 1
        if isinstance(other, Opposite):
            self._lives -= 1
            self._y = 0
            self._x = 0
            self._landed = False
            g2d.alert("You lost one life")
            

    def position(self ) -> tuple :
        return self._x, self._y, self._w, self._w
    
    def state(self)  -> str :
        ''' This function return the state of the actor to the function symbol in order to choose the right image'''
        arena_w, arena_h = self._arena.size()
        if not self._landed or self._dx == 0:
            return "up"
        else:
            if self._dx < 0:
                return "sx"
            elif self._dx > 0 and self:
                return "dx"
            

    def symbol(self) -> tuple :
        if self.state() == "sx":
            print("sx")
            return 0, 18, self._w, self._h
        elif self.state() == "dx":
            print("dx")
            return 1225, 18, self._w, self._h
        elif self.state() == "up":
            print("up")
            return 0, 90, self._w, self._h
        
    def create_ball(self):
        ball = Booble(self._arena,(self._x,self._y-10),self._dx/2)
        
    def return_lives(self)  -> int :
        return self._lives
    


class Opposite(Jumper):
    
    def __init__(self, arena:object, pos:tuple):
        self._x, self._y = pos
        self._w, self._h = 20, 18
        self._SPEED = 5
        self._dx, self._dy = 0, 0
        self._g = 0.5
        self._arena = arena
        arena.add(self)
        self._counter = 0 # this variable is used to control the random movements of the opponent 
        self._landed = False


 
    def move(self):
        arena_w, arena_h = self._arena.size()
        self._counter += 1
        self._landed = False
        self._x += self._dx
        if self._x < 0:
            self._x = 0
            self._dx = -self._dx
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w
            self._dx = - self._dx
        #in this point the funcion decides the random movement of the actor   
        rand_move = random.choice((-1,0,1))
        print(rand_move)
        if self._counter >= 75 and rand_move == -1:
                    self._dx = -self._SPEED
                    self._counter = 0
        elif self._counter >= 75 and rand_move == 1:
                    self._dx = self._SPEED
                    self._counter = 0
        if self._counter >= 75 and rand_move == 0:
            self._dy = -4*self._SPEED #modificato -2 -> -4
            self._landed = False
            
        self._dy += self._g  
        self._y += self._dy 
        if self._y < 0:
            self._y = 0
        if self._y  > arena_h - self._h:
            self._y = arena_h  - self._h +2
            self._landed = True
       



    def collide(self, other:object):
        arena_w, arena_h = self._arena.size()
        
        if isinstance(other, Wall) and self._dy > 0:
            wx, wy, ww, wh = other.position()
            px, py, pw, ph = self.position()
            previous_x, previous_y = px - self._dx, py - self._dy

            if previous_x + ww <= wx:
                self._x = wx - pw
            elif previous_x >= wx + ww:
                self._x = wx + ww
            elif previous_y + ph <= wy:
                self._y, self._dy = wy - ph, 1
                self._landed = True
            elif previous_y >= wy + wh:
                self._y, self._dy = wy + wh, 1
                
        if isinstance(other, Booble):
            self._arena.remove(self)
        
        
            

    def position(self):
        return self._x, self._y, self._w, self._w
    
    def state(self) -> str :
        ''' This function return the state of the actor to the function symbol in order to choose the right image
        '''
        arena_w, arena_h = self._arena.size()
        if not self._landed or self._dx == 0:
            return "up"
        else:
            if self._dx < 0:
                return "sx"
            elif self._dx > 0 and self:
                return "dx"
            

    def symbol(self) -> tuple :
        if self.state() == "sx":
            print("sx")
            return 5, 455, self._w, self._h 
        elif self.state() == "dx":
            print("dx")
            return 1265, 455, self._w, self._h
        elif self.state() == "up":
            print("up")
            return 76, 455, self._w, self._h
      

  


class Arena():
    '''A generic 2D game, with a given size in pixels and a list of actors
    '''
    def __init__(self, size: (int, int)):
        '''Create an arena, with given dimensions in pixels
        '''
        self._w, self._h = size
        self._count = 0
        self._actors = []


    def add(self, a: Actor):
        '''Register an actor into this arena.
        Actors are blitted in their order of registration
        '''
        if a not in self._actors:
            self._actors.append(a)

    def remove(self, a: Actor):
        '''Cancel an actor from this arena
        '''
        if a in self._actors:
            self._actors.remove(a)

    def move_all(self):
        '''Move all actors (through their own move method).
        After each single move, collisions are checked and eventually
        the `collide` methods of both colliding actors are called
        '''
        actors = list(reversed(self._actors))
        for a in actors:
            a.move()
            for other in actors:
    
                if other is not a and self.check_collision(a, other):
                        a.collide(other)
                        other.collide(a)
        self._count += 1

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        '''Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        '''
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
            and x2 < x1 + w1 and x1 < x2 + w2
            and a1 in self._actors and a2 in self._actors)

    def actors(self) -> list:
        '''Return a copy of the list of actors
        '''
        return list(self._actors)

    def size(self) -> (int, int):
        '''Return the size of the arena as a couple: (width, height)
        '''
        return (self._w, self._h)

    def count(self) -> int:
        '''Return the total count of ticks (or frames)
        '''
        return self._count
    


    
    
                
                                

                
            
    
    

