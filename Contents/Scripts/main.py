debug=[
 0, #0 show frame start/end
 0, #1 print rect coords
 0, #2 display hitboxes
 [""], #3 place()
 0, #4 player position
 0, #5 other things position
 0, #6 room position
 1, #7 check collision
 0,
 0,
 0,
 0
 ] 
fps=60 #framerate
#-------------------------modules-------------------------
import os, random, time, sys, math, pygame 
screen = pygame.display.set_mode((1306, 681), pygame.SCALED) #set up the pygame screen
#x, y = (50, 50); os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) #sets the position of the screen
for c in os.getcwd().split(chr(92)): #makes a list of the steps in the directory
    try: a.append(c) #move onto the next step
    except: a=[c] #if i is first step
    try:
        exec(open("/".join(a)+r"PyGameTemplate.py").read()) #attempt to locate template file at current dir level
        break #if the file is opened
    except: pass #function to load template from anywhere on directory path

print(f"your screen size is {display_size}.")
s=1; #screen = pygame.display.set_mode((int(display_size[0]/s), int(display_size[1]/s)), pygame.RESIZABLE, pygame.SCALED) #set up the pygame screen
screen = pygame.display.set_mode((1306, 681), pygame.SCALED) #set up the pygame screen
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
                setattr(self.flipped, axis, not getattr(self.flipped, axis))
        except:
            pass
        #print(self.last, self.flipped, "left" if pressed("LEFT") else "right")
        self.blocked=False, 0
        _=(Vector(x, y).unit()*(self.speed/2)) #use the circle_movement function to create a vector with constant magnitude in direction of above
        self.velocity+=_
        return
    x, y = 0, 0 #zero vector
    if (pressed("LEFT") or pressed("a")) and found("A"):
        x-=self.speed
    if (pressed("RIGHT") or pressed("d")) and found("D"):
        x+=self.speed
    if (pressed("DOWN") or pressed("s")) and found("S"):
        y+=self.speed
    if (pressed("UP") or pressed("w")) and found("W"):
        y-=self.speed
    if debug[4]: print(f"x, y is {x, y}")
    x*=(-1)**self.flipped.x
    y*=(-1)**self.flipped.y
    ###all above creates the vector in x and y###
    match (x, y):
        case (0, 0): _=Vector(0, 0)
        case (x, y): _=(Vector(x, y).unit()*self.speed) #create a vector with magnitude speed in direction of above
    if debug[4]: print(f"The controls vector is: {_.tup()}")
    if self.block_check(): print("g")
    self.velocity+=_ #if zero vector (nothing pressed), do nothing
    #wrap-\/-\/-\/-\/-\/-\/
    w, h = pygame.display.get_surface().get_size() #screen size
    if debug[6]: print("The room you are currently in is: ", self.game.room_pos.tup())
    if self.position.x<0: #if at left side of screen
        if self.game.room_pos.x>0: self.game.room_pos.x-=1
        self.velocity += (Vector((w+1), 0)) #move to right side
    elif self.position.x>w: #if at right side
        self.velocity += (Vector((-w+1), 0)) #move to left side
        if self.game.room_pos.x<len(self.game.levels)-1: self.game.room_pos.x+=1
    if self.position.y<0: #if at top of screen
        self.velocity += (Vector(0, (h-1))) #move to bottom
        if self.game.room_pos.y>0: self.game.room_pos.y-=1
    elif self.position.y>h: #if at bottom
        self.velocity += (Vector(0, (-h+1))) #move to top
        if self.game.room_pos.y<len(self.game.levels[self.game.room_pos.x])-1: self.game.room_pos.y+=1
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
class Game:
    def __init__(self, data="""{"start_room":(0, 0), "level_name":"", "background":"", "player":Player(), "rooms":[[{"elements":[Element()]}]]}"""):
        self.player=Player(coords=(95, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=80, _), name="THEplayer", speed=10)
        data=eval(data)
        self.data=data
        self.start=data["start_room"]
        self.name=data["level_name"]
        try: self.default_bg=data["background"]
        except: input(err); self.default_bg=data["background_colour"]
        self.player.game=self
        self.levels=data["rooms"]
        self.room_pos=Position(self.start)
        self.recharging=[]
        self.onscreen_elements=(elements:=self.levels[self.room_pos.x][self.room_pos.y]["elements"])
        self.mute_timer=Timer()
        self.click_timer=Timer()

    def base_loop_start(self, level_data, i, colour): #ALWAYS DO t=base_loop_start
        list_of_elements = level_data["elements"]
        if debug[0]: print(f"frame {i}")
        t=Timer()
        try: self.default_bg.place()
        except: screen.fill(default_bg)
        for a in list_of_elements:
            if debug[5]: print(a.name, a.position.tup())
            if debug[1]: print([i.tup() for i in a.rect()])
            if debug[2]: a.show_hitbox() #shows bot of hit
            if type(a) in [Booster]: a.anim()
            a.move()
            a.velocity = Vector(0, 0)
            if a.name in debug[3]: print(a.name, a.size, a.rotation, a.flipped.tup())
            a.place()
        return t
    def base_loop_end(self, t, i): #ALWAYS DO return base_loop_end
        pl=self.player
        if debug[0]: print("player")
        pl.anim()
        pl.move()
        if debug[2]: pl.show_hitbox()
        pl.velocity = Vector(0, 0)
        pl.place()
        pygame.display.flip()
        if debug[0]: print(f"{t.time()*1000} milliseconds\nframe {i} end\n")
        pygame.time.delay(int(1000/fps - t.time()))
        if pressed("m") and self.mute_timer.time() >=1:
            self.mute_timer.reset()
            back_mus
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return True
        return False

    def anim_loop(self, level_data, i, colour=(132, 30, 95), frames=100, final_scale=1.5):
        t=self.base_loop_start(level_data, c, colour)
        self.player.rescale(final_scale**(1/frames))
        return self.base_loop_end(t, i) 
        "" #triggers upon collection of key

    def main_loop(self, level_data, c, colour, act):
        list_of_elements=level_data["elements"]
        t=self.base_loop_start(level_data, c, colour)
        for i in self.recharging:
            i.recharge()
        collect_1=[]
        for i in list_of_elements:
            if type(i)==Key: collect_1.append(i.rect_check())
            else: 
                #try: 
                    i.rect_check()
               # except: i.place()
        act[1]=True in collect_1
        if debug[0]: print("player")
        self.player.check_clicked()
        if pygame.mouse.get_pressed()[0] and self.click_timer.time()>1:
            self.click_timer.reset()
            print(f"Mouse clicked at: {Position(pygame.mouse.get_pos()).cartesian().tup()}")
        self.player.controls()
        return act, self.base_loop_end(t, c)

    def wrapper(self):
        loop=(self.main_loop, self.anim_loop)
        act = [0, 0, 0, 0]
        ended=0
        c=0
        while not ended==True:
            level_data=self.levels[self.room_pos.x][self.room_pos.y]
            self.onscreen_elements=(elements:=level_data["elements"])
            act, ended=loop[0](level_data, c, colour, act)
            c+=1
            if True in act:
                for n, i in enumerate(act):
                    if i:
                        act[i]=0
                        if n==1:
                            for e in range(frames:=10):
                                if not ended and loop[1](level_data, c, colour, frames, 1.3):
                                        ended=1
                            for e in range(frames:=10):
                                if not ended and loop[1](level_data, c, colour, frames, 1/1.3):
                                        ended=1


class Key(Interactive):
    def __init__(self, coords=(0, 0), key_name="base", size_tuple=(20, 20), degrees_of_rotation=0, sprite_num=1, name="", game=chr(0)):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/key_{key_name}.png', size_tuple, degrees_of_rotation, sprite_num)
        self.name=key_name+" key"+name
        self.key=key_name.upper()
        self.game=game
        self.player=self.game.player
        self.collected=False
    
    def kill(self): 
        try: self.game.onscreen_elements.remove(self)
        except: pass

    def collide(self):
        super().collide()
        global found_keys
        found_keys+=[self.key]
        self.kill()

class Booster(Interactive):
    def __init__(self, coords=(0, 0), size_tuple=(35, 35), degrees_of_rotation=0, sprite_num=1, name="someBooster", game=chr(0), boost_vector=Vector(3, 0)):
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Booster/booster1.png', rf'{get_target("GameAssets.lnk")}/Booster/booster2.png'], size_tuple, boost_vector.angle*180/math.pi-90, sprite_num, name=name)
        self.game=game
        self.player=self.game.player
        self.collected=False
        self.boost_vector = boost_vector

    def collide(self):
        super().collide()
        travel=0
        n=8
        while travel<self.boost_vector.magnitude:
            self.player.move(self.boost_vector.unit()*(self.player.speed/n))
            travel+=1/n
            print(f"Looped for {n*travel} frames")
            if not travel%4: self.player.place()
            self.anim()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    travel=self.boost_vector.magnitude

class Wall(Blocker):
    def __init__(self, rect_coords, name="someWall", game=chr(0)):
        print((((rect_coords[1][0]+rect_coords[0][0])/2, (rect_coords[1][1]+rect_coords[0][1])/2)), (abs(rect_coords[1][0]-rect_coords[0][0]), abs(rect_coords[1][1]-rect_coords[0][1])))
        coords = ((rect_coords[1][0]+rect_coords[0][0])/2, (rect_coords[1][1]+rect_coords[0][1])/2)
        size_tuple = (abs(rect_coords[1][0]-rect_coords[0][0]), abs(rect_coords[1][1]-rect_coords[0][1]))
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Wall/Wall_active.png', rf'{get_target("GameAssets.lnk")}/Wall/Wall_inactive.png'], size_tuple, 0, name=name)
        self.active=True
        self.game=game
        self.player=self.game.player

    def collide(self):
        return
        #self.toggle()

    def toggle(self):
        self.rect_check=lambda x: None
        self.sprite_num=2


class Flip(Blocker):
    def __init__(self, coords, axis="x", name="flip", game=chr(0)):
        assert axis.lower() in ("x", "y"), ValueError(f'The given axis is {axis}, but the axis must be "x" or "y"')
        if axis=="y": self.axis="y"
        if axis=="x": self.axis="x"
        degrees_of_rotation=(0 if self.axis=="x" else 90)
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Flipper/flipper.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_half_used.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_used.png'], (50, 50), degrees_of_rotation)
        self.name=name
        self.active=2
        self.game=game
        try: self.player=self.game.player
        except: self.player = Player(); exit()
    
    def recharge(self):
        if self.a.time()>=2 and self.active==0:
            self.active=1
            self.sprite_num=3-self.active
        if self.a.time()>=4 and self.active==1:
            self.active=2
            self.sprite_num=3-self.active
            self.game.recharging.remove(self)

    def kill(self):
        self.a=Timer()
        self.active=0
        self.sprite_num=3-self.active
        self.game.recharging.append(self)

    def collide(self):
        if self.active==2:
            if debug[0]: pass
            setattr(self.player.flipped, self.axis, not getattr(self.player.flipped, self.axis))
            self.kill()

#--------------------------setup--------------------------
for i in "1":
    found_keys=["W", "A", "S", "D"] #the keys the player can use
    trombone=play(get_target("GameAssets.lnk")+"\Sounds\lose_trombone.mp3")[1]; trombone.set_volume(0.15); trombone.stop()
    back_mus=chanplay((_:=play(get_target("GameAssets.lnk")+"\Sounds\TitleMus.wav"))[0], _[1], -1)
    back_mus.queue(play(get_target("GameAssets.lnk")+"\Sounds\TitleMus.wav")[1])
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

config_data=open(r"level.cfg").read() #unpack and assign level configurations
game=Game(config_data)

game.wrapper()
back_mus.stop()
trombone.play()
pygame.display.quit()
time.sleep(3.5)
input("Press Enter to exit the script...")
pygame.quit()
