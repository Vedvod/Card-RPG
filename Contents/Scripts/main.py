debug=[
 1, #show frame start/end
 0, #print rect coords
 1, #display hitboxes
 [""], #place()
 0] #player position
fps=60 #framerate
#-------------------------modules-------------------------
import os, random, time, sys, math, pygame 
x, y = (0, 30); os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) #sets the position of the screen
for c in os.getcwd().split(chr(92)): #makes a list of the steps in the directory
    try: a.append(c) #move onto the next step
    except: a=[c] #if i is first step
    try:
        exec(open("/".join(a)+r"PyGameTemplate.py").read()) #attempt to locate template file at current dir level
        break #if the file is opened
    except: pass #function to load template from anywhere on directory path

print(f"your screen size is {display_size}.")
s=1; #screen = pygame.display.set_mode((int(display_size[0]/s), int(display_size[1]/s)), pygame.RESIZABLE, pygame.SCALED) #set up the pygame screen
screen = pygame.display.set_mode((display_size[0]//s, display_size[1]//s), pygame.RESIZABLE, pygame.SCALED) #set up the pygame screen
FPStimer = Timer()
#-----------------------function(s)-----------------------
found=lambda x: x in found_keys #shorthand for brevity
pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]") #check if key pressed

def con(self): #temporary controls function, almost same as template one
    if debug[4]: print(f"Player's position is {self.position.tup()}") 
    if self.blocked[0]:
        x, y = -self.last[0], -self.last[1]
        try:
            if self.blocked[1].name.startswith("flip") and self.blocked[1].active==2:
                axis = self.blocked[1].axis
                exec(f"""self.flipped.{axis}=not self.flipped.{axis}""")
        except:
            pass
        #print(self.last, self.flipped, "left" if pressed("LEFT") else "right")
        self.blocked=False, 0
        _=(Vector(x, y).unit()*self.speed) #use the circle_movement function to create a vector with constant magnitude in direction of above
        self.velocity+=_
        return
    x, y = 0, 0 #zero vector
    if pressed("LEFT") and found("A"):
        x-=self.speed
    if pressed("RIGHT") and found("D"):
        x+=self.speed
    if pressed("DOWN") and found("S"):
        y+=self.speed
    if pressed("UP") and found("W"):
        y-=self.speed
    if debug[4]: print(f"x, y is {x, y}")
    x*=(-1)**self.flipped.x
    y*=(-1)**self.flipped.y
    ###all above creates the vector in x and y###
    match (x, y):
        case (0, 0): _=Vector(0, 0); print("a")
        case (x, y): _=(Vector(x, y).unit()*self.speed) #create a vector with magnitude speed in direction of above
    if debug[4]: print(f"The controls vector is {_.tup()}")
    if self.block_check(): print("g")
    self.velocity+=_ #if zero vector (nothing pressed), do nothing
    #wrap-\/-\/-\/-\/-\/-\/
    w, h = pygame.display.get_surface().get_size() #screen size
    if self.position.x<0: #if at left side of screen
        self.move(Vector((w+1), 0)) #move to right side
        room.x+=1
    elif self.position.x>w: #if at right side
        self.move(Vector((-w+1), 0)) #move to left side
    if self.position.y<0: #if at top of screen
        self.move(Vector(0, (h-1))) #move to bottom
    elif self.position.y>h: #if at bottom
        self.move(Vector(0, (-h+1))) #move to top
    #self.place() #place the player
    self.last=(_.i, _.j)

Player.controls=con #override default controls with new ones

#--------------------------loops--------------------------

def changColor(image, color): #from stackoverflow lmao
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT) #????????????????????????????????????
    return finalImage

#-------------------------classes-------------------------
class Key(Element):
    def __init__(self, coords=(0, 0), key_name="base", size_tuple=(20, 20), degrees_of_rotation=0, sprite_num=1, name=""):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/key_{key_name}.png', size_tuple, degrees_of_rotation, sprite_num)
        self.name=key_name+" key"+name
        self.key=key_name.upper()
        self.player=Player()
        self.game=Game()
    
    def kill(self): 
        game.elements.remove(self)

    def collide(self):
        if debug[0]: print("collided")
        global found_keys
        found_keys+=self.key
        self.kill()
        
    def rect_check(self):
        if self.in_rect(self.player): self.collide(); return True

class PressShow(Element):
    pass

class Flip(Element):
    def __init__(self, coords, axis="x", name="flip"):
        assert axis.lower() in ("x", "y"), ValueError(f'The given axis is {axis}, but the axis must be "x" or "y"')
        if axis=="y": self.axis="y"
        if axis=="x": self.axis="x"
        degrees_of_rotation=(0 if self.axis=="x" else 90)
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Flipper/flipper.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_half_used.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_used.png'], (50, 50), degrees_of_rotation)
        self.name=name
        self.player=Player()
        self.game=Game()
        self.active=2
        self.block=True
    
    def respawn(self):
        if self.a.time()>=2 and self.active==0:
            self.active=1
            self.sprite_num=3-self.active
            self.reinit()
        if self.a.time()>=4 and self.active==1:
            self.active=2
            self.sprite_num=3-self.active
            self.game.respawners.remove(self)
            self.reinit()

    def kill(self):
        self.a=Timer()
        self.active=0
        self.sprite_num=3-self.active
        self.game.respawners.append(self)

    def collide(self):
        if self.active==2:
            if debug[0]: pass
            raise ValueError
            self.player.flipped[self.axis]=not self.player.flipped[self.axis]
            self.kill()
        self.reinit()
        
    def rect_check(self):

        if self.in_rect(self.player):
            self.player.blocked=True, self
            self.collide()
            return True
       

class Game:
    def __init__(self, elements=list(), player=Player()):
        self.elements=elements
        for i in elements:
            i.player=player
            i.game=self
        self.player=player
        self.respawners=[]

    def base_loop_start(self, list_of_elements, i, colour): #ALWAYS DO t=base_loop_start
        if debug[0]: print(f"frame {i}")
        t=Timer()
        screen.fill(colour.out())
        for a in list_of_elements:
            if debug[1]: print([i.tup() for i in a.rect()])
            if debug[2]: a.show_hitbox() #shows 
            a.move(a.velocity)
            a.velocity = Vector(0, 0)
            if a.name in debug[3]: print(a.name, a.size, a.rotation, a.flipped.tup())
            a.place()
        return t
    def base_loop_end(self, t, i): #ALWAYS DO return base_loop_end
        pl=self.player
        print("player")
        pl.anim()
        pl.move()
        pl.show_hitbox()
        pl.velocity = Vector(0, 0)
        pl.place()
        pygame.display.flip()
        if debug[0]: print(f"{t.time()*1000} milliseconds\nframe {i} end\n")
        pygame.time.delay(int(1000/fps - t.time()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return True
        return False

    def anim_loop(self, list_of_elements, i, colour=(132, 30, 95), frames=100, final_scale=1.5):
        colour=self.rainbow(colour) #change colour across cyclic rainbow spectrum
        t=self.base_loop_start(list_of_elements, c, colour)
        self.player.rescale(final_scale**(1/frames))
        return self.base_loop_end(t, i) 
        "" #triggers upon collection of key

    def rainbow(self, colour):
        return colour
        global max_val
        for c in [colour.r, colour.b, colour.g]:
            if c.tick%1!=0:
                c.tick+=0.5
                continue
            if c.tick>=max_val*3:
                c.tick=0
            if c.tick<max_val:
                c.val+=1
            elif c.tick<max_val*2:
                c.val-=1
            c.tick+=0.5
        #print(space(a.val), space(b.val), space(c.val))
        return colour

    def main_loop(self, list_of_elements, c, colour, act):
        t=self.base_loop_start(list_of_elements, c, colour)
        for i in self.respawners:
            i.respawn()
        collect_1=[]
        for i in list_of_elements:
            if type(i)==Key: collect_1.append(i.rect_check())
            else: 
                try: i.rect_check()
                except: i.place()
        act[1]=True in collect_1
        if debug[0]: print("player")
        self.player.check_clicked()
        self.player.controls()
        return act, self.base_loop_end(t, c)

    def wrapper(self):
        loop=(self.main_loop, self.anim_loop)
        act = [0, 0, 0, 0]
        ended=0
        c=0
        while not ended==True:
            elements=self.level_config["room"][room_row][room_column]
            act, ended=loop[0](elements, c, colour, act)
            c+=1
            if True in act:
                for n, i in enumerate(act):
                    if i:
                        act[i]=0
                        if n==1:
                            for e in range(frames:=150):
                                if not ended and loop[1](elements, c, colour, frames, 1.25):
                                        ended=1

#--------------------------setup--------------------------
for i in "1":
    found_keys="a".upper() #the keys the player can use
    #the_player=Player(coords=(0, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _), name="player") #player
    W=Key(coords=(100, 300), key_name="w") 
    D=Key(coords=(0, 91), key_name="d")
    S=Key(coords=(-253, 0), key_name="s")
    F=Flip((-250, 160), "x")
    F2=Flip((330, 250), "y")
    #collectable keys
    trombone=play(get_target("GameAssets.lnk")+"\Sounds\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
    back_mus=play(get_target("GameAssets.lnk")+"\Sounds\TitleMus.wav"); back_mus.stop(); back_mus.play(-1)
    #sounds

#SOME FPS COUNTER STUFF NEED TO UPDATE TO FIT WITH NEW FORMAT PLS DO THIS THANKS OK I TRUST YOU!!!
#myfont = pygame.font.SysFont('comic sans ms', 20)
#class Text(Element):

#    def __init__(self, path=myfont.render("Default", False, (100, 100, 100)), coords=(0, 0), scale=1, rotate=0):
#        super().__init__(path, coords, (scale*pygame.Surface.get_size(path)[0], scale*pygame.Surface.get_size(path)[1]), rotate)

#    def reinit(self):
#        self.size=(scale*pygame.Surface.get_size(self.image)[0], scale*pygame.Surface.get_size(self.image)[1])
#        self.icon=pygame.transform.rotate(pygame.transform.scale(self.image, self.size), self.spin)

#thing=Text(myfont.render("FPS: 0", False, (0, 0, 200)), (100, 100), 5)

#------------------------main line------------------------
ended=False
c=0
def space(x, l=3):
    while len(str(x))<l:
        x=str(x)+" "
    return x
class N:
    def __init__(self, val, tick):
        self.val=val
        self.tick=tick
max_val=165
class Colour:
    def __init__(self, c1, c2, c3):
        self.r=c1
        self.g=c2
        self.b=c3
    
    def out(self):
        return (self.r.val, self.g.val, self.b.val)

#colour=(132, 30, 95)
colour = Colour(N(max_val, max_val), N(0, max_val*2), N(0, max_val*3))

config_data=eval((g:=open(r"level.cfg")).read()) #unpack and assign level configurations

game=Game(config_data)
    [W, D, S, F, F2],
    #[], 
    Player(coords=(0, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=80, _), name="player")); game.player.speed=game.player.size[0]/15; game.player.game=game
game.wrapper()
back_mus.stop()
trombone.play(1)
pygame.display.quit()
time.sleep(3.5)
input("Press Enter to exit the script...")
pygame.quit()
