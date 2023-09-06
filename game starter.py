from arena_actors import Arena, Actor, Dragon, Booble, Opposite, Wall
import random
import g2d_pygame as g2d


class BBgame:
    def __init__(self,file: str):
        self._arena = None
        self._player = None
        self._player2 = None
        self._multiplayer = False
        with open(file,"r") as f:
            for line in f:
                data = line 
                if line[0] == "A":
                    new_line = line[1:-1]
                    data = new_line.split(",")
                    print(data)
                    self._arena = Arena((int(data[0]),int(data[1])))
                elif line[0] == "P":
                    new_line = line[1:-1]
                    data = new_line.split(",")
                    print(data)
                    wall = Wall(self._arena,int(data[0]),int(data[1]))  
                elif line[0] == "p":
                    new_line = line[1:-1]
                    data = new_line.split(",")
                    print(data)
                    self._player = Dragon(self._arena,(int(data[0]),int(data[1])))
                elif line[0] == "t":
                    new_line = line[1:-1]
                    data = new_line.split(",")
                    self._multiplayer = True
                    self._player2 = Dragon(self._arena,(int(data[0]),int(data[1])))
                    print(data)
                elif line[0] == "a":
                    new_line = line[1:-1]
                    data = new_line.split(",")
                    print(data)
                    opposite = Opposite(self._arena,(int(data[0]),int(data[1])))
            self._playtime = 60

                
    def arena(self) -> object :
        return self._arena

    def return_play_time(self) -> int :
        return self._playtime
    
    def game_not_over(self) -> bool:
        ''' this function check if time is left and players have minimum 1 life '''
        return (self._player.return_lives() > 0) and self.remaining_time() > 0 and not(self.game_won())
        self.remaining_time()
    
    def game_won(self) -> bool:
        '''thi function check if there are opponents in the arena'''
        counter = 0
        for element in self._arena.actors():
            if isinstance(element,Opposite):
                counter += 1
        if counter == 0:
            return True
                
    
    def remaining_time(self) -> int:
        return self._playtime - self._arena.count() // 30 
    
    def controller(self):
            if self._multiplayer:
                if g2d.key_pressed("Enter"):
                    self._player.create_ball()
                if g2d.key_pressed("ArrowUp"):
                    self._player.go_up()
                if g2d.key_pressed("ArrowRight"):
                    self._player.go_right()
                if g2d.key_pressed("ArrowLeft"):
                    self._player.go_left()
                if g2d.key_pressed("Spacebar"):
                    self._player2.create_ball()
                if g2d.key_pressed("<"):
                    self._player2.go_up()
                if g2d.key_pressed("RightButton"):
                    self._player2.go_right()
                if g2d.key_pressed("LeftButton"):
                    self._player2.go_left()
                    
            else:
                if g2d.key_pressed("Enter"):
                    self._player.create_ball()
                if g2d.key_pressed("ArrowUp"):
                    self._player.go_up()
                if g2d.key_pressed("ArrowRight"):
                    self._player.go_right()
                if g2d.key_pressed("ArrowLeft"):
                    self._player.go_left()
        
    
            
class BBgui:
    def __init__ (self,game:object):
        self._game = game
        g2d.init_canvas(self._game.arena().size())
        g2d.alert(f"you have {self._game.return_play_time()} seconds to kill al your opponents  ")
        g2d.alert("Controls:\n Player1:\n arrows to move\n Enter to shoot\n Player2:\n RightButton, LeftButton and < to move\n Spacebar to shoot")
        self._sprites = g2d.load_image("bb.PNG")
        g2d.main_loop(self.tick)
        
    def tick(self):
        if self._game.game_not_over():
            g2d.clear_canvas()
            g2d.set_color((0,0,0))
            g2d.fill_rect((0,0,self._game.arena().size()[0],self._game.arena().size()[1]))
            if self._game.remaining_time() > 5:   
                g2d.set_color((250,250,250))
            else:
                g2d.set_color((255,0,0))
            g2d.draw_text(str(self._game.remaining_time()),(550, 0),  50)
            self._game.arena().move_all()
            self._game.controller()
            for actor in self._game.arena().actors():
                if isinstance(actor, Wall):
                    g2d.set_color((200,100,100))
                    g2d.fill_rect(actor.position())
                else:
                    g2d.draw_image_clip(self._sprites,actor.symbol(),actor.position())
        else:
            if self._game.game_won():
                g2d.alert("You won")
                g2d.close_canvas()
            else:
                g2d.alert("You lost")
                g2d.close_canvas()
        
        
      
game = BBgame("level.txt")
guigame = BBgui(game)
g2d.main_loop(guigame.tick())



