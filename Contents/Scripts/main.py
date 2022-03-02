debug=0
show_hitbox=0
#-------------------------modules-------------------------
import os, random, time, sys, math, pygame
x, y = (0, 30); os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) #sets the position of the screen
for i in os.getcwd().split(chr(92)): #makes a list of the steps in the directory
    try: a.append(i) #move onto the next step
    except: a=[i] #if i is first step
    try:
        if debug: print("/".join(a)+r"PyGameTemplate.py") #debug message to ensure the dir building is correct
        exec(open("/".join(a)+r"PyGameTemplate.py").read()) #attempt to locate template file at current dir level
        break #if the file is opened
    except:
        pass #function to load template from anywhere on directory path
s=1.5
screen = pygame.display.set_mode((int(display_size[0]/s), int(display_size[1]/s)), pygame.RESIZABLE, pygame.SCALED) #set the pygame screen

#-----------------------function(s)-----------------------
found=lambda x: x in found_keys #shorthand for brevity
pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]") #check if key pressed

def con(self, speed=50): #temporary controls function, almost same as template one
    global pressed
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
        self.move(w-1, 0) #move to right side
    elif self.position[0]>w/2: #if at right side
        self.move(-w+1, 0) #move to left side
    if self.position[1]<-h/2: #if at top of screen
        self.move(0, h-1) #move to bottom
    elif self.position[1]>h/2: #if at bottom
        self.move(0, -h+1) #move to top
    self.place() #place the player
    if show_hitbox:
        a, b = (self.rect()[0][0], self.rect()[1][0])
        c, d = (self.rect()[0][-1], self.rect()[1][-1])
        Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()

Player.controls=con
#-------------------------classes-------------------------
class Key(Element, pygame.sprite.Sprite):
    def __init__(self, player=Player(), coords=(0, 0), key_name="base", size_tuple=(20, 20), degrees_of_rotation=0, name=""):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/key_{key_name}.png', size_tuple, degrees_of_rotation)
        self.player=player
        self.name=name
        self.key=key_name.upper()
    
    def kill(self):
        global elements
        elements.remove(self)

    def collide(self):
        if debug: print("collided")
        global found_keys
        found_keys+=self.key
        self.kill()
        
    def rect_check(self):
        if show_hitbox:
            a, b = (self.rect()[0][0], self.rect()[1][0])
            c, d = (self.rect()[0][-1], self.rect()[1][-1])
            Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
            Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        if set(self.rect()[0])&set(self.player.rect()[0]) and set(self.rect()[1])&set(self.player.rect()[1]): self.collide()

#--------------------------setup--------------------------
found_keys="A"
the_player=Player(coords=(0, 0), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _), name="player")
W=Key(the_player, coords=(100, 300), key_name="w", name="w_key")
D=Key(the_player, coords=(0, 153), key_name="d", name="d_key")
S=Key(the_player, coords=(-253, 0), key_name="s", name="s_key")
trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
fps=60

#------------------------main line------------------------
def anim_loop():
    pass

def main_loop(list_of_elements, i):
    #print(f"frame {i}")
    screen.fill((132, 30, 95))
    for a in list_of_elements:
        #print(a.name)
        a.place()
        a.rect_check()
    #print("player")
    the_player.check_clicked()
    the_player.controls(the_player.size[0]/10)
    the_player.anim()
    pygame.display.flip()
    #print(f"frame {i} end\n")
    pygame.time.delay(int(1000/fps))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit(); return True

ended=False
elements=[W, D, S]
i=0
while not ended:
    ended=main_loop(elements, i)
    i+=1
trombone.play()
time.sleep(3)
input("Press Enter to exit the script...")
pygame.quit()
