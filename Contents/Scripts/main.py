debug=[
 0, #show frame start/end
 0, #print rect coords
 0, #display hitboxes
 0, #player position
 0]

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


#-----------------------function(s)-----------------------
found=lambda x: x in found_keys #shorthand for brevity
pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]") #check if key pressed
def con(self, speed=50): #temporary controls function, almost same as template one
    x, y = 0, 0
    if (pressed("LEFT") or pressed("a")) and found("A"):
        x-=speed
    if (pressed("RIGHT") or pressed("d")) and found("D"):
        x+=speed
    if (pressed("DOWN") or pressed("s")) and found("S"):
        y-=speed
    if (pressed("UP") or pressed("w")) and found("W"):
        y+=speed
    #all above creates the vector in x and y
    _=self.circle_movement((x, -y), speed)[1] #use the circle_movement function to create a vector with constant magnitude in direction of above
    if (x, y)!=(0, 0): self.move(_[0], _[1]) #if zero vector (nothing pressed), do nothing
    #wraps by default
    w, h = pygame.display.get_surface().get_size() #screen size
    if self.position[0]<-w/2: #if at left side of screen
        self.move((-1)**self.flipped[0]*(w+1), 0) #move to right side
    elif self.position[0]>w/2: #if at right side
        self.move((-1)**self.flipped[0]*(-w+1), 0) #move to left side
    if self.position[1]<-h/2: #if at top of screen
        self.move(0, h-1) #move to bottom
    elif self.position[1]>h/2: #if at bottom
        self.move(0, -h+1) #move to top
    self.place() #place the player
    if debug[4]: print(self.position)
    if debug[2]: #shows hitboxes
        a, b = (self.rect()[0][0], self.rect()[1][0])
        c, d = (self.rect()[0][-1], self.rect()[1][-1])
        Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()

Player.controls=con #override default controls with new ones

#--------------------------loops--------------------------

def changColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

#-------------------------classes-------------------------
class Key(Element):
    def __init__(self, coords=(0, 0), key_name="base", size_tuple=(20, 20), degrees_of_rotation=0, name=""):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/key_{key_name}.png', size_tuple, degrees_of_rotation)
        self.name=key_name
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
        a, b = (self.rect()[0][0], self.rect()[1][0])
        c, d = (self.rect()[0][-1], self.rect()[1][-1])
        if debug[2]:
            Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        if set(self.rect()[0])&set(self.player.rect()[0]) and set(self.rect()[1])&set(self.player.rect()[1]): self.collide(); return True

class PressShow(Element):
    pass

class Flip(Element):
    def __init__(self, coords, axis="x", name=""):
        assert axis.lower() in ("x", "y"), ValueError(f'The given axis is {axis}, but the axis must be "x" or "y"')
        if axis=="y": self.axis=1
        if axis=="x": self.axis=0
        degrees_of_rotation=self.axis*90
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/flipper.png', (50, 50), degrees_of_rotation)
        self.name=name
        self.player=Player()
        self.game=Game()
    
    def kill(self):
        game.elements.remove(self)

    def collide(self):
        if debug[0]: print("collided")
        self.player.flipped[self.axis]=not self.player.flipped[self.axis]
        self.kill()
        
    def rect_check(self):
        a, b = (self.rect()[0][0], self.rect()[1][0])
        c, d = (self.rect()[0][-1], self.rect()[1][-1])
        if debug[2]:
            Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        if set(self.rect()[0])&set(self.player.rect()[0]) and set(self.rect()[1])&set(self.player.rect()[1]): self.collide(); return True
            
class Game:
    def __init__(self, elements=list(), player=Player()):
        self.elements=elements
        for i in elements:
            i.player=player
            i.game=self
        self.player=player

    def base_loop_start(self, list_of_elements, i, colour): #ALWAYS DO t=base_loop_start
        if debug[0]: print(f"frame {i}")
        t=Timer()
        screen.fill(colour.out())
        for a in list_of_elements:
            if debug[1]: print(a.name)
            a.place()
        return t
    def base_loop_end(self, t, i): #ALWAYS DO return base_loop_end
        self.player.anim()
        self.player.place()
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
        #print(i/frames*100)
        self.player.rescale(1.5**(1/frames))
        return self.base_loop_end(t, i)


    def rainbow(self, colour):
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

    def main_loop(self, list_of_elements, i, colour, act):
        t=self.base_loop_start(list_of_elements, c, colour)
        collect_1=[]
        for i in list_of_elements:
            if type(i)==Key: collect_1.append(i.rect_check())
            else: i.rect_check()
        act[1]=True in collect_1
        if debug[0]: print("player")
        self.player.check_clicked()
        self.player.controls(self.player.size[0]/10)
        return act, self.base_loop_end(t, c)

    def wrapper(self):
        loop=(self.main_loop, self.anim_loop)
        act = [0, 0, 0, 0]
        ended=0
        c=0
        while not ended==True:
            elements=self.elements
            act, ended=loop[0](elements, c, colour, act)
            c+=1
            if True in act:
                for n, i in enumerate(act):
                    if i:
                        act[i]=0
                        if n==1:
                            for e in range(frames:=150):
                                if not ended and loop[1](elements, i, colour, frames, 5):
                                        ended=1

#--------------------------setup--------------------------
for i in [1]:
    found_keys="WSDA" #the keys the player can use
    #the_player=Player(coords=(0, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _), name="player") #player
    W=Key(coords=(100, 300), key_name="w", name="w_key") 
    D=Key(coords=(0, 153), key_name="d", name="d_key")
    S=Key(coords=(-253, 0), key_name="s", name="s_key")
    F=Flip((-50, 150), "x")
    #collectable keys
    trombone=play(get_target("GameAssets.lnk")+"\sounds\lose_trombone.mp3"); trombone.set_volume(0.50); trombone.stop()
    back_mus=play(get_target("GameAssets.lnk")+"\sounds\quieter.wav"); back_mus.stop(); back_mus.play(-1)
    #sounds
    fps=60 #framerate

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
game=Game([W, D, S, F], Player(coords=(0, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _), name="player"))
game.wrapper()
back_mus.stop()
trombone.play(3)
pygame.display.quit()
time.sleep(3.5)
input("Press Enter to exit the script...")
pygame.quit()
