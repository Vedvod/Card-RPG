debug=[
 0, # 0 show frame start/end
 0, # 1 print rect coords
 0, # 2 display hitboxes
 [""], # 3 place()
 0, # 4 player position
 0, # 5 other things position
 0, # 6 room position
 0, # 7 check collision
 0, # 8 boost stuff
 0, # 9
 0, #10 mouse position stuff
 0  #11
 ] 
fps=60 #framerate
#-------------------------modules-------------------------
import os, random, time, sys, math, pygame, pygame._sdl2 as sdl2
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
Element(
			paths_to_assets=[get_target("GameAssets.lnk")+r"/Backgrounds/Splash Screen.png"],
			name="splash",
            size_tuple=(1306, 681),
			coords=((0, 0))).place()
pygame.display.flip()
FPStimer = Timer()
#-----------------------function(s)-----------------------
Player.found=lambda self, x: x in self.game.found_keys #shorthand for brevity
pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]") #check if key pressed
pygame.joystick.init()
con_axis = lambda x: None if pygame.joystick.get_count()!=1 else round(joysticks()[0].get_axis(x))
joysticks = lambda: None if pygame.joystick.get_count()!=1 else [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

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
    for i in joysticks():
        pass
        #print(i.get_name(), i.get_guid(), ", ".join([f"axis {x}: {round(i.get_axis(x), 2)}" for x in range(i.get_numaxes())]), ", ".join([f"button {x}: {i.get_button(x)}" for x in range(i.get_numbuttons())]), ", ".join([f"hat {x}: {i.get_hat(x)}" for x in range(i.get_numhats())]))
    if (pressed("LEFT") or pressed("a") or round(con_axis(0))==-1) and self.found("A"):
        x-=self.speed
    if (pressed("RIGHT") or pressed("d") or round(con_axis(0))==1) and self.found("D"):
        x+=self.speed
    if (pressed("DOWN") or pressed("s") or round(con_axis(1))==1) and self.found("S"):
        y+=self.speed
    if (pressed("UP") or pressed("w") or round(con_axis(1))==-1) and self.found("W"):
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
listify = lambda x: ([x] if type(x) not in [list, tuple] else x)
#-------------------------classes-------------------------
class Game:
    def p_update(self):
        for column in self.levels:
            for row in column:
                for elem in row["elements"]:
                    elem.player=self.player
    
    def __init__(self, data="""{"start_room":(0, 0), "found_keys":["W"], "level_name":"", "background":"", "player":Player(), "rooms":[[{"elements":[Element()]}]]}"""):
        self.player=Player(); data=eval(data)
        #data=data[0]|data[1]
        del self.player
        self.data=data
        self.music_paused=False
        self.pause_timer=Timer()
        attr_dict=["start", "found_keys", "player", "name", "levels"]
        for n, i in enumerate(["start_room", "found_keys", "player", "level_name", "rooms"]):
            try: setattr(self, attr_dict[n], data[i])
            except: pass
        try: self.default_bg=data["background"]
        except: input(err); self.default_bg=data["background_colour"]
        self.player.game=self
        for i in self.found_keys:
            for x in self.levels:
                for y in x:
                    for elem in y["elements"]:
                        if elem.name.startswith(f"{i.lower()} key"):
                            y["elements"].remove(elem)
        self.room_pos=Position(self.start)
        self.recharging=[]
        self.p_update()
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
        pl.position=Position([(i//0.25)*0.25 for i in pl.position.tup()])
        pl.place()
        pygame.display.flip()
        if debug[0]: print(f"{t.time()*1000} milliseconds\nframe {i} end\n")
        pygame.time.delay(int(1000/fps - t.time()))
        if pressed("m") and self.mute_timer.time() >=1:
            self.mute_timer.reset()
            back_mus
        
        for event in pygame.event.get():
            if event.type==69:
                selected=random.choice(os.listdir(rf'{get_target("GameAssets.lnk")}/Sounds/Music'))
                print(f"Now playing: {selected}")
                back_mus.queue(play(rf'{get_target("GameAssets.lnk")}/Sounds/Music/'+selected)[1])
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
                try: i.rect_check()
                except: pass
        act[1]=True in collect_1
        if debug[0]: print("player")
        self.player.check_clicked()
        if (pygame.joystick.get_count()>0 and joysticks()[0].get_button(4) and self.pause_timer.time()>0.3):
            self.pause_timer.reset()
            back_mus.pause()
            if self.music_paused:
                back_mus.unpause()
            self.music_paused = not self.music_paused
        if (pygame.joystick.get_count()>0 and joysticks()[0].get_button(5) and self.pause_timer.time()>0.3):
            self.pause_timer.reset()
            back_mus.stop()
    
        if pygame.mouse.get_pressed()[0] and self.click_timer.time()>0.5:
            self.click_timer.reset()
            if debug[10]: print(f"Mouse clicked at: {Position(pygame.mouse.get_pos()).cartesian().tup()}")
            if self.player.in_rect((Position(pygame.mouse.get_pos()), Position(pygame.mouse.get_pos()))):
                if debug[10]: print(f"PLayer at: {self.player.position.cartesian().tup()}")
                if debug[10]: print(f"Player currently in room {self.room_pos.tup()}")
        if (pygame.mouse.get_pressed()[1] and self.click_timer.time()>0.5) or (pygame.joystick.get_count()>0 and joysticks()[0].get_button(9)):
            self.click_timer.reset()
            self.__init__(open(r"level.cfg").read()) 

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
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/key_{key_name}.png', size_tuple, degrees_of_rotation, sprite_num, game=game)
        self.name=key_name+" key"+name
        self.key=key_name.upper()
        self.game=game
        self.player=self.game.player
        self.collected=False
    
    def kill(self): 
        try: self.game.onscreen_elements.remove(self)
        except: pass

    def collide(self):
        clunk = chanplay(*play(get_target("GameAssets.lnk")+"\Sounds\powerup.mp3")); clunk.set_volume(0.35)
        super().collide()
        self.game.found_keys+=[self.key]
        self.kill()
    
class Home(Interactive):
    def __init__(self, coords=(0, 0), size_tuple=(80, 80), degrees_of_rotation=0, sprite_num=1, name="", game=chr(0)):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/house.png', size_tuple, degrees_of_rotation, sprite_num, game=game)
        self.game=game
        self.player=self.game.player
    
    def kill(self): 
        try: self.game.onscreen_elements.remove(self)
        except: pass

    def collide(self):
        super().collide()
        self.game.room_pos=Position((3, 3))

class Booster(Interactive):
    def __init__(self, coords=(0, 0), size_tuple=(35, 35), degrees_of_rotation=0, sprite_num=1, name="someBooster", game=chr(0), boost_vector=Vector(3, 0)):
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Booster/booster1.png', rf'{get_target("GameAssets.lnk")}/Booster/booster2.png'], size_tuple, -boost_vector.angle*180/math.pi, sprite_num, name=name, game=game)
        self.game=game
        self.player=self.game.player
        self.collected=False
        self.boost_vector = boost_vector

    def collide(self):
        super().collide()
        travel=0
        n=2
        pos=self.player.position
        while travel<self.boost_vector.magnitude:
            self.game.default_bg.place()
            for a in self.game.levels[self.game.room_pos.x][self.game.room_pos.y]["elements"]:
                if debug[5]: print(a.name, a.position.tup())
                if debug[1]: print([i.tup() for i in a.rect()])
                if debug[2]: a.show_hitbox() #shows bot of hit
                if type(a) in [Booster]: a.anim()
                a.move()
                a.velocity = Vector(0, 0)
                if a.name in debug[3]: print(a.name, a.size, a.rotation, a.flipped.tup())
                a.place()
            self.player.place(pos)
            self.player.move(self.boost_vector.unit()*(self.player.speed/n))
            travel+=1/n
            if not travel%1: self.player.place(pos); pos=self.player.position; self.player.anim()
            if debug[8]: print(f"Looped for {n*travel} frames")
            self.anim()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    travel=self.boost_vector.magnitude


class Wall(Blocker):
    def __init__(self, rect_coords=((0,0),(0,0)), name="someWall", game=Game(), active=True):
        coords = ((rect_coords[1][0]+rect_coords[0][0])/2, (rect_coords[1][1]+rect_coords[0][1])/2)
        size_tuple = (abs(rect_coords[1][0]-rect_coords[0][0]), abs(rect_coords[1][1]-rect_coords[0][1]))
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Wall/Wall_active.png', rf'{get_target("GameAssets.lnk")}/Wall/Wall_inactive.png'], size_tuple, 0, name=name, game=game)
        self.game=game
        self.check=self.rect_check
        self.player=self.game.player
        if not active:
            self.rect_check=lambda: None
            self.sprite_num=2

    def toggle(self):
        if self.rect_check()==None:
            self.sprite_num=1
            self.rect_check=self.check
        else:
            self.rect_check=lambda: None
            self.sprite_num=2


class Trigger(Interactive):
    def __init__(self, coords=(0, 0), size_tuple=(35, 35), sprite_num=1, name="someTrigger", game=chr(0), target_list=Wall(game=Game())):
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Trigger/trigger_up.png', rf'{get_target("GameAssets.lnk")}/Trigger/trigger_down.png'], size_tuple, 0, sprite_num, name=name)
        self.game=game
        self.player=self.game.player
        self.targets=listify(target_list)

    def collide(self):
        clunk = chanplay(*play(get_target("GameAssets.lnk")+"\Sounds\water_shot.wav")); clunk.set_volume(0.15)
        self.sprite_num=2
        for target in self.targets: target.toggle()
        self.collide=lambda: None


class Flip(Blocker):
    def __init__(self, coords, axis="x", name="flip", game=chr(0), cooldown=2):
        assert axis.lower() in ("x", "y"), ValueError(f'The given axis is {axis}, but the axis must be "x" or "y"')
        if axis=="y": self.axis="y"
        if axis=="x": self.axis="x"
        degrees_of_rotation=(0 if self.axis=="x" else 90)
        super().__init__(coords, [rf'{get_target("GameAssets.lnk")}/Flipper/flipper.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_half_used.png', rf'{get_target("GameAssets.lnk")}/Flipper/flipper_used.png'], (50, 50), degrees_of_rotation, game=game)
        self.name=name
        self.active=2
        self.game=game
        self.cooldown=cooldown
        try: self.player=self.game.player
        except: self.player = Player(); exit()
    
    def recharge(self):
        if self.a.time()>=self.cooldown/2 and self.active==0:
            self.active=1
            self.sprite_num=3-self.active
        if self.a.time()>=self.cooldown and self.active==1:
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
    trombone=play(get_target("GameAssets.lnk")+"\Sounds\lose_trombone.mp3")[1]; trombone.set_volume(0.15); trombone.stop()
    back_mus=chanplay(*(_:=play(get_target("GameAssets.lnk")+"\Sounds\Music\TitleMus.wav")))
    back_mus.set_endevent(69)
    print(back_mus.get_endevent())
    #sounds

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
