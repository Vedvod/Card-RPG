#-------------------------modules-------------------------
import os, random, time, sys, math, cmath, pygame, numpy as np
pygame.init(); os.system("cls"); print("pygame 2.6.9 (SDL 2.0.22, Python 3.11.5)")
display_size=list(pygame.display.get_desktop_sizes()[0])
display_size[1]=round(display_size[1]*0.927083333)
screen = pygame.display.set_mode((50, 50))

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

def play(location): #MAYBE REPLACE WITH PYGAME.MIXER???
    pygame.mixer.init()
    x=pygame.mixer.Sound(location)
    x.play()
    return x
    "" #play a sound from file

def scalar(vector):
    x, y = vector[1][0]-vector[0][0], vector[1][1]-vector[0][1] #gets the differences in x and y coordinates
    return math.sqrt(x**2 + y**2) #uses pythagorus to find hypotenuse (shortest distance) length
    "" #find the modulus of a vector

def project(vector_1, vector_2):
    magnitude = scalar(vector_2) #find modulus of the second vector
    _, angle = cmath.polar(complex(vector_1[1][0], vector_1[1][1])-complex(vector_1[0][0], vector_1[0][1])) #find the polar coordinates angle of vector 1 shifted to (0, 0)
    projection=(0, 0),(vector_1[0][0]+magnitude*math.cos(angle), vector_1[0][1]+magnitude*math.sin(angle)) #make a vector in the direction of vector 1 with the same length as vector 2
    return projection
    "" #a basic vector projection function

def cartesian(coords, reverse=False):
    w, h = pygame.display.get_surface().get_size() #find the size of the screen
    if reverse: 
        return coords[0]+w/2, h/2-coords[1]
    return coords[0]-w/2, h/2-coords[1] #use width/2 and height/2 as the origin, rather than the top left
    "" #a function to move the origin to the middle of the screen

#-------------------------classes-------------------------
class Position:
    def __init__(self, coordinates=(0, 0)):
        self.coords=coordinates
        self.x, self.y=self.coords

    def cartesian(self):
        w, h = pygame.display.get_surface().get_size() #find the size of the screen
        return Position((self.x+w/2, self.y+h/2)) #use width/2 and height/2 as the origin, rather than the top left
        "" #a function to move the origin to the middle of the screen

class Timer:
    def __init__(self):
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time
    def reset(self):
        self.start_time=time.time()

class Element(pygame.sprite.Sprite, Timer):
    def __init__(self, coords=(0, 0), paths_to_assets=get_target("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple="", degrees_of_rotation=0, name="generic", sprite_num=1):
        super().__init__()
        Timer.__init__(self)
        self.name=name
        self.position=coords
        self.base=[pygame.image.load(x) for x in (paths_to_assets if type(paths_to_assets)!=str else [paths_to_assets])]
        self.rotation=degrees_of_rotation
        self.sprite_num=sprite_num
        self.size=size_tuple
        if size_tuple=="":
            self.size=self.base[sprite_num-1].get_size()
        self.true_size=self.size
        self.icon=pygame.transform.rotate(pygame.transform.scale(self.base[self.sprite_num-1], self.size), self.rotation)
        screen.blit(self.icon, cartesian(self.position))
        "" #a function that is essential to the class, defining initial attributes.

    def place(self, coords="much too late", SURF=screen): 
        if coords=="much too late": #if coordinates not specified
            coords=Position(self.position).cartesian() #use Element's stored coordinates
        SURF.blit(self.icon, (coords.x-pygame.Surface.get_size(self.icon)[0]/2, coords.y-pygame.Surface.get_size(self.icon)[1]/2)) #place element using cartesian coordinates
        "" #a function that takes a cartesian coordinate input (i.e. (0, 0) is centering object on center of screen), then converts it to pygame coordinates.
    
    def rect(self):
        a, b = cartesian((self.position[0]-self.size[0]/2, self.position[1]+self.size[1]/2), True)
        c, d = cartesian((self.position[0]+self.size[0]/2, self.position[1]-self.size[1]/2), True)
        a, b, c, d = [int(x) for x in (a, b, c, d)]
        if debug: print(a, b, c, d)
        return np.linspace(a, c, 5*(c-a)+1), np.linspace(b, d, 5*(d-b)+1)

    def move(self, x_shift=0, y_shift=0): 
        self.position=self.position[0]+x_shift, self.position[1]+y_shift #add each shift
        "" #a function to move the element

    def circle_movement(self, direction, speed):
        return project(((0, 0), direction), ((0, 0), (0, speed)))

    def sprite(self): 
        return self.base[self.sprite_num-1]
        "" #a convenient shorthand for the currently toggled display sprite.

    def anim(self):
        self.sprite_num = (self.sprite_num+1 if self.sprite_num<len(self.base) else 1)
        self.reinit()

    def reinit(self):
        self.icon=pygame.transform.rotate(pygame.transform.scale(self.sprite(), self.size), self.rotation)
        "" #a function that updates the element's icon to match changes in attributes. Generally called by other function.

    def rotate(self, degrees_to_rotate):
        self.rotation+=degrees_to_rotate
        self.rotation=self.rotation%360
        self.reinit()
        "" #a function that offsets the rotaton of the element, and then updates its icon.

    def set_angle(self, degrees_of_rotation):
        self.rotation=degrees_of_rotation
        self.reinit()
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
        self.reinit()
        "" #a function that changes the size attribute of the element, then updates its icon.

    def rescale(self, scaleX, scaleY=-100, true=True):
        if scaleY==-100 and scaleX>0: #if scaleY has not been specified 
            scaleY=scaleX #use common ratio to scale
        if scaleX>0: #if scaleY was specified
            self.resize((self.size[0]*scaleX, self.size[1]*scaleY), true_size=true)
            self.reinit()
        else: #if scaleX was invalid
            raise ValueError("Size must be positive!")
        "" #a function that changes the height and width of an element by a common ratio, then updates its icon.
    "" #the base class for all elements

class Player(Element):
    def __init__(self, coords=(0, 0), paths_to_assets=get_target("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple="", degrees_of_rotation=0, sprite_num=1):
        super().__init__(coords, paths_to_assets, size_tuple, degrees_of_rotation, sprite_num)
        self.time=Timer()

    def controls(self, speed=50, wrap=False):
        xi, yi = self.position
        x, y = 0, 0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            x-=speed
        if pressed[pygame.K_RIGHT]:
            x+=speed
        if pressed[pygame.K_DOWN]:
            y-=speed
        if pressed[pygame.K_UP]:
            y+=speed
        _=self.circle_movement((x, -y), speed)[1]
        if (x, y)!=(0, 0): self.move(_[0], _[1])
        if wrap:
            w, h = pygame.display.get_surface().get_size()
            if me.position[0]<-w/2:
                me.move(w-1, 0)
            elif me.position[0]>w/2:
                me.move(-w+1, 0)
            if me.position[1]<-h/2:
                me.move(0, h-1)
            elif me.position[1]>h/2:
                me.move(0, -h+1)
        self.place()

if os.path.basename(__file__)=="PyGameTemplate.py":
    me=Player(coords=(0, 30), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _))
    trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
    pygame.quit()
    print("Success")
    input("Press Enter to exit the script...")
