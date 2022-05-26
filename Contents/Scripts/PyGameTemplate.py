#-------------------------modules-------------------------
import os, random, time, sys, math, cmath, pygame, numpy as np
pygame.init(); os.system("cls"); print("pygame 2.6.9 (SDL 2.0.22, Python 3.11.5)")
display_size=list(pygame.display.get_desktop_sizes()[0])
display_size[1]=round(display_size[1]*0.927083333)
screen = pygame.display.set_mode((50, 50))
prev_size=display_size

#-----------------------function(s)-----------------------
def get_target(lnk_file):
    lnk_file = open(lnk_file, "rb").read() #open the file in byte read mode
    keepGoing, track, final=1, 0, ""
    for n, i in enumerate(lnk_file): #iterate through each byte
        if not keepGoing: #if the target was located
            break
        if i in range(65, 91): #if the byte is the ascii code for a letter
            if chr(lnk_file[n+1])==":": #if the letter after is a colon
                track=1 #start reading the string
        if track==1: #if reading
            if i==0: #if reading past the target string
                keepGoing=0 #stop reading
            else:
                final+=chr(i) #add to output string
    return final
    "" #finds the location that a shortcut file (.lnk) leads to

def play(location):
    pygame.mixer.init()
    x=pygame.mixer.Sound(location)
    x.play()
    return x
    "" #play a sound from file

#-------------------------classes-------------------------
class Position:
    def __init__(self, real_coords, cartesian=False):
        self.x = real_coords[0]
        self.y = real_coords[1]
        if cartesian: #flag for putting in incorrectly formatted coords
            w, h = pygame.display.get_surface().get_size()
            self.x+=w/2
            self.y=h/2-self.y
        "" 

    def cartesian(self):
        w, h = pygame.display.get_surface().get_size() #find the size of the screen
        return Position((self.x-w/2, h/2-self.y))  #use width/2 and height/2 as the origin, rather than the top left
        "" #returns a Position where the origin is shifted to the middle of the screen

    def tup(self):
        return self.x, self.y
        "" #returns the coords in form (x, y)
    "" #a class to track (SDL-formatted) positions


class Vector:
    def __init__(self, x=0, y=0, polar=False, name="vector"):
        self.name=name
        self.i=x
        self.j=y
        if polar:
            self.i, self.j = (_:=cmath.rect(x, y)).real, _.imag
        self.magnitude, self.angle = cmath.polar(complex(self.i, self.j))
        if self.name == "player": print(self.angle)
    
    def unit(self):
        print(f"angle is {self.angle*180/math.pi}")
        return Vector(math.cos(self.angle), math.sin(self.angle), name=self.name)
    
    def tup(self): 
        return self.i, self.j
    
    def movement(self, position):
        return Position((position.x+self.i, position.y+self.j))
    
    def __mul__(self, scalar):
        return Vector(self.i*scalar, self.j*scalar, name=self.name)
    
    def __add__(self, v2):
            return Vector(self.i+v2.i, self.j+v2.j, name=self.name)

    def __getitem__(self, axis):
        if axis.lower() in "xy":
            n = ("i" if axis.lower() == "x" else "j")
            return eval(f"""self.{n}""")
        else: raise ValueError


class Timer:
    def __init__(self): #initialise the time
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time
    def reset(self):
        self.start_time=time.time()


class Element:
    def __init__(self, coords=(0, 0), paths_to_assets=get_target("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple=chr(0), degrees_of_rotation=0, sprite_num=1, name="generic"):
        self.position = Position(coords, True)
        self.base_images=[pygame.image.load(x) for x in (paths_to_assets if type(paths_to_assets)!=str else [paths_to_assets])]
        self.sprite_num=sprite_num
        self.sprite = lambda: self.base_images[self.sprite_num-1]
        self.size = (size_tuple if size_tuple!=chr(0) else self.sprite().get_size())
        self.true_size=self.size
        self.flipped=Position((False, False))
        self.icon=lambda: pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(self.sprite(), self.size), self.rotation), self.flipped.x, self.flipped.y)
        self.solid=False
        self.name=name
        self.velocity=Vector(0, 0, name=self.name)
        self.rotation=degrees_of_rotation
        self.anim_timer=Timer()
        self.click_timer=Timer()

    def rotate(self, degrees_to_rotate):
        self.rotation+=degrees_to_rotate
        self.rotation=self.rotation%360
        "" #a function that offsets the rotaton of the element, and then updates its icon.

    def set_angle(self, degrees_of_rotation):
        self.rotation=degrees_of_rotation
        "" #a function that sets the rotation of the element, then updates its icon

    def resize(self, new_size=(75, 75), relative=False, true_size=False):
        if relative: #if size change is based on current size
            if (self.size[0]+new_size[0])>0 and (self.size[1]+new_size[1])>0: #if both new sizes are valid
                self.size=self.size[0]+new_size[0], self.size[1]+new_size[1] #change sizes
            else: #if at least one size is invalid (negative)
                raise ValueError("Size must be positive!") #error
        elif new_size[1]>0 and new_size[0]>0: #if not relative, and both sizes are valid
            self.size=new_size #change sizes
            if true_size: self.true_size=new_size
        else:
            raise ValueError("Size must be positive!")
        "" #a function that changes the size attribute of the element, then updates its icon.

    def rescale(self, scaleX, scaleY=-100, true=True):
        if scaleY==-100 and scaleX>0: #if scaleY has not been specified 
            scaleY=scaleX #use common ratio to scale
        if scaleX>0: #if scaleY was specified
            self.resize((self.size[0]*scaleX, self.size[1]*scaleY), true_size=true)
        else: #if scaleX was invalid
            raise ValueError("Size must be positive!")
        "" #a function that changes the height and width of an element by a common ratio, then updates its icon.

    def anim(self):
        if self.anim_timer.time()>=0.15:
            self.anim_timer.reset()
            self.sprite_num = (self.sprite_num+1 if self.sprite_num<len(self.base_images) else 1)

    def rect(self):
        top_left = Position((self.position.x-self.size[0]/2, self.position.y-self.size[1]/2))
        bottom_right = Position((self.position.x+self.size[0]/2, self.position.y+self.size[1]/2))
        return top_left, bottom_right
   
    def in_rect(self, to_check):
        a, b = self.rect() #unpack the self rect tuple such that a is top left, b is bottom right
        c, d = to_check.rect() #unpack the target rect tuple such that c is top left, d is bottom right
        print((a.tup(), b.tup()), self.name)
        print((c.tup(), d.tup()), to_check.name)
        return (((c.x <= a.x <= d.x) and (c.y <= a.y <= d.y)) or ((c.x <= b.x <= d.x) and (c.y <= b.y <= d.y))) or (((c.x <= a.x <= d.x) and (c.y <= b.y <= d.y)) or ((c.x <= b.x <= d.x) and (c.y <= a.y <= d.y)))
        #raise EOFError
        #return True or False

    def show_hitbox(self):
        a, b = self.rect() #unpack the self rect tuple such that a is top left, b is bottom right
        pygame.draw.line(screen, (150, 100, 50), a.tup(), (a.x, b.y), width=1)
        pygame.draw.line(screen, (150, 100, 50), a.tup(), (b.x, a.y), width=1)
        pygame.draw.line(screen, (150, 100, 50), b.tup(), (a.x, b.y), width=1)
        pygame.draw.line(screen, (150, 100, 50), b.tup(), (b.x, a.y), width=1)
        pass

    def check_clicked(self):
        if pygame.mouse.get_pressed()[0] and self.click_timer.time()>1:
            self.click_timer.reset()
            mouse_coords=pygame.mouse.get_pos()
            print("a")
            #COMPLETE THIS TO ACTUALLY DO STUFF PLS

    def move(self, vec=chr(0)):
        if vec==chr(0): vec = self.velocity
        self.position=vec.movement(self.position)

    def place(self, coords=chr(0), SURF=screen): 
        if coords==chr(0): #if coordinates not specified
            coords=self.position #use Element's stored coordinates
        #print(self.name)
        if self.name in debug[3]: print(f"Name: {self.name}, Pos: {coords.tup()}")
        SURF.blit(self.icon(), (coords.x-self.size[0]/2, coords.y-self.size[1]/2)) #place element using cartesian coordinates
        "" #a function to place Elements on the SURFace
    "" #the base class for all elements

class Player(Element):
    def __init__(self, coords=(0, 0), paths_to_assets=get_target("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple=chr(0), degrees_of_rotation=0, sprite_num=1, name="somePlayer", speed=10):
        super().__init__(coords, paths_to_assets, size_tuple, degrees_of_rotation, sprite_num, name)
        self.blocked=0, 0
        self.speed=speed

    pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]") #check if key pressed
    def controls(self, wrap=False): 
        speed=self.speed
        x, y = 0, 0 #zero vector
        if pressed("LEFT"):
            x-=speed
        if pressed("RIGHT"):
            x+=speed
        if pressed("DOWN"):
            y-=speed
        if pressed("UP"):
            y+=speed
        #all above creates the vector in x and y
        _=self.circle_movement((x, -y), speed)[1] #use the circle_movement function to create a vector with constant magnitude in direction of above
        if (x, y)!=(0, 0): self.move(_[0], _[1]) #if zero vector (nothing pressed), do nothing
        if wrap: #go around screen
            w, h = pygame.display.get_surface().get_size() #screen size
            if self.position[0]<-w/2: #if at left side of screen
                self.move(w-1, 0) #move to right side
            elif self.position[0]+self.size[0]/2>w/2: #if at right side
                self.move(-w+1, 0) #move to left side
            if self.position[1]<-h/2: #if at top of screen
                self.move(0, h-1) #move to bottom
            elif self.position[1]>h/2: #if at bottom
                self.move(0, -h+1) #move to top
        self.place() #place the player

    def block_check(self): ###########################################################################################################################################################
        block_list=[]
        for i in self.game.onscreen_elements:
            if isinstance(i, Flip):
                if self.in_rect(i): return True #checks if player is blocked by collision

    

if os.path.basename(__file__)=="PyGameTemplate.py":
    #me=Player(coords=(0, 30), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _))
    #trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
    pygame.quit()
    print("Success")
    input("Press Enter to exit the script...")
