#-------------------------modules-------------------------
import os, random, time, sys, math, cmath, pygame
pygame.init(); os.system("cls"); print("pygame 2.6.9 (SDL 2.0.22, Python 3.11.5)")
display_size=list(pygame.display.get_desktop_sizes()[0])
display_size[1]-=70
#screen = pygame.display.set_mode(display_size)

#-----------------------function(s)-----------------------
def getTarget(lnk_file):
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
    from playsound import playsound #
    import threading
    def thread_funct(locate):
        playsound(locate)
    x = threading.Thread(target=thread_funct, args=(location,), daemon=True)
    x.start()
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

def cartesian(coords):
    w, h = pygame.display.get_surface().get_size() #find the size of the screen
    return (coords[0]+w/2, coords[1]+h/2) #use width/2 and height/2 as the origin, rather than the top left
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

class Element(pygame.sprite.Sprite):
    def __init__(self, coords=(0, 0), paths_to_assets=getTarget("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple="", degrees_of_rotation=0, sprite_num=1):
        super().__init__()
        self.position=coords
        self.base=[pygame.image.load(x) for x in list(paths_to_assets)]
        self.size=size_tuple
        self.rotation=degrees_of_rotation
        self.sprite_num=sprite_num
        if size_tuple=="":
            self.size=self.base[sprite_num-1].get_size()
        self.icon=pygame.transform.rotate(pygame.transform.scale(self.base[self.sprite_num-1], self.size), self.rotation)
        screen.blit(self.icon, cartesian(self.position))
        "" #a function that is essential to the class, defining initial attributes.

    def place(self, coords="much too late"): 
        if coords=="much too late": #if coordinates not specified
            coords=Position(self.position).cartesian() #use Element's stored coordinates
        screen.blit(self.icon, (coords.x-pygame.Surface.get_size(self.icon)[0]/2, coords.y-pygame.Surface.get_size(self.icon)[1]/2)) #place element using cartesian coordinates
        "" #a function that takes a cartesian coordinate input (i.e. (0, 0) is centering object on center of screen), then converts it to pygame coordinates.
    
    def move(self, x_shift=0, y_shift=0): 
        self.position=self.position[0]+x_shift, self.position[1]+y_shift #add each shift
        "" #a function to move the element

    def sprite(self): 
        return self.base[self.sprite_num-1]
        "" #a convenient shorthand for the currently toggled display sprite.

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

    def resize(self, new_size=(75, 75), relative=False):
        if relative: #if size change is based on current size
            if (self.size[0]+new_size[0])>0 and (self.size[1]+new_size[1])>0: #if both new sizes are valid
                self.size=self.size[0]+new_size[0], self.size[1]+new_size[1] #change sizes
            else: #if at least one size is invalid (negative)
                raise ValueError("Size must be positive!") #error
        elif new_size[1]>0 and new_size[0]>0: #if not relative, and both sizes are valid
            self.size=new_size #change sizes
        else:
            raise ValueError("Size must be positive!")
        self.reinit()
        "" #a function that changes the size attribute of the element, then updates its icon.

    def rescale(self, scaleX, scaleY=-100):
        if scaleY==-100 and scaleX>0: #if scaleY has not been specified 
            scaleY=scaleX #use common ratio to scale
        if scaleX>0: #if scaleY was specified 
            self.size=self.size[0]*scaleX, self.size[1]*scaleY
            self.reinit()
        else: #if scaleX was invalid
            raise ValueError("Size must be positive!")
        "" #a function that changes the height and width of an element by a common ratio, then updates its icon.
    "" #the base class for all elements

class Timer:
    def __init__(self):
        self.start_time=time.time()
    def time(self):
        return time.time()-self.start_time
    def reset(self):
        self.start_time=time.time()

class Player(Element, Timer):
    def __init__(self, coords=(0, 0), paths_to_assets=getTarget("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple="", degrees_of_rotation=0, sprite_num=1):
        super().__init__(coords, paths_to_assets, size_tuple, degrees_of_rotation, sprite_num)

    def controls(self, speed=50):
        inital_pos=Position(self.coords)
        xi, yi = self.coords
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
        self.go_to((x+xi, y+yi), speed)
        self.place()

#print(base_change(, 2))
if os.path.basename(__file__)=="PyGameTemplate.py":
    input("Press Enter to exit the script...")
