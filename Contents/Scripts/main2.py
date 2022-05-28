debug=[
 0, #show frame start/end
 0, #print rect coords
 0, #display hitboxes
 [""], #place()
 0] #player position

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

def con(self): #temporary controls function, almost same as template one
    if debug[4]: print(self.position)
    if debug[2]: #shows hitboxes
        a, b = (self.rect()[0][0], self.rect()[1][0])
        c, d = (self.rect()[0][-1], self.rect()[1][-1])
        Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
    speed=self.speed
    if self.blocked[0]:
        x, y = -self.last[0], -self.last[1]
        try:
            if self.blocked[1].name.startswith("flip") and self.blocked[1].active==2:
                self.flipped[0]=not self.flipped[0]
        except:
            pass
        self.blocked=False, 0
        _=self.circle_movement((x, -y), speed)[1] #use the circle_movement function to create a vector with constant magnitude in direction of above
        self.move(_[0], _[1])
        return
    x, y = 0, 0 #zero vector
    if pressed("LEFT") and found("A"):
        x-=speed
    if pressed("RIGHT") and found("D"):
        x+=speed
    if pressed("DOWN") and found("S"):
        y-=speed
    if pressed("UP") and found("W"):
        y+=speed
    x*=(-1)**self.flipped[0]
    y*=(-1)**self.flipped[1]
    #all above creates the vector in x and y
    _=self.circle_movement((x, -y), speed)[1] #use the circle_movement function to create a vector with constant magnitude in direction of above
    if self.game.block_check((self.rect()[0]+_[0], self.rect()[1]+_[1])): print("g")
    if (x, y)!=(0, 0): self.move(_[0], _[1]) #if zero vector (nothing pressed), do nothing
    #wraps by default
    w, h = pygame.display.get_surface().get_size() #screen size
    if self.position[0]<-w/2: #if at left side of screen
        self.move((w+1), 0) #move to right side
    elif self.position[0]>w/2: #if at right side
        self.move((-w+1), 0) #move to left side
    if self.position[1]<-h/2: #if at top of screen
        self.move(0, (h-1)) #move to bottom
    elif self.position[1]>h/2: #if at bottom
        self.move(0, (-h+1)) #move to top
    self.place() #place the player
    self.last=(x, y)

Player.controls=con #override default controls with new ones