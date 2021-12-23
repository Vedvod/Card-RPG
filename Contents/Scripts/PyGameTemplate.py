#-------------------------modules-------------------------
import os, random, time, sys, math, cmath, pygame
pygame.init(); os.system("cls"); print("pygame 2.6.9 (SDL 2.0.22, Python 3.11.5)")
display_size=list(pygame.display.get_desktop_sizes()[0])
display_size[1]-=70
#screen = pygame.display.set_mode(display_size)

#-----------------------function(s)-----------------------
def getTarget(lnk_file):
    lnk_file = open(lnk_file, "rb").read()
    cont, track, final=1, 0, ""
    for n, i in enumerate(lnk_file):
        if not cont:
            break
        if i in range(65, 91):
            if chr(lnk_file[n+1])==":":
                track=1
        if track==1:
            if i==0:
                cont=0
            else:
                final+=chr(i)
    return final

def play(location):
    import os
    global os
    from playsound import playsound
    import threading
    def thread_funct(locate):
        playsound(locate)
    x = threading.Thread(target=thread_funct, args=(location,), daemon=True)
    x.start()

def scalar(vector):
    x, y = vector[1][0]-vector[0][0], vector[1][1]-vector[0][1]
    return math.sqrt(x**2 + y**2)

def project(vector_1, vector_2):
    magnitude = scalar(vector_2)
    #print(f"Projecting a vector of length {magnitude} onto the vector between {vector_1[0]} and {vector_1[1]}:")
    x, angle = cmath.polar(complex(vector_1[1][0], vector_1[1][1])-complex(vector_1[0][0], vector_1[0][1]))
    projection=(vector_1[0][0]+magnitude*math.cos(angle), vector_1[0][1]+magnitude*math.sin(angle))
    return ((0, 0), projection)

def cartesian(coords):
    w, h = pygame.display.get_surface().get_size()
    return (coords[0]+w/2, coords[1]+h/2)

#-------------------------classes-------------------------
class Element(pygame.sprite.Sprite):
    def __init__(self, coords=(0, 0), paths_to_assets=[r"GameAssets/DefaultSprite.png"], size_tuple="", degrees_of_rotation=0, sprite_num=1):
        self.position=coords
        self.base=[pygame.image.load(x) for x in paths_to_assets]
        self.size=size_tuple
        self.rotation=degrees_of_rotation
        self.sprite_num=sprite_num
        if size_tuple=="":
            self.size=self.base[sprite_num-1].get_size()
        self.icon=pygame.transform.rotate(pygame.transform.scale(self.base[self.sprite_num-1], self.size), self.rotation)
        screen.blit(self.icon, self.position)
        "" #a function that is essential to the class, defining initial attributes.

    def place(self, coords="much too late"):
        if coords=="much too late":
            coords=cartesian(self.position)
        screen.blit(self.icon, (coords[0]-pygame.Surface.get_size(self.icon)[0]/2, coords[1]-pygame.Surface.get_size(self.icon)[1]/2))
        "" #a function that takes a cartesian coordinate input (i.e. (0, 0) is centering object on center of screen), then converts it to pygame coordinates.

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
        if relative:
            if (self.size[0]+new_size[0])>0 and (self.size[1]+new_size[1])>0:
                self.size=self.size[0]+new_size[0], self.size[1]+new_size[1]
            else:
                raise ValueError("Size must be positive!")
        elif new_size[1]>0 and new_size[0]>0:
            self.size=new_size
        else:
            raise ValueError("Size must be positive!")
        self.reinit()
        "" #a function that changes the size attribute of the element, then updates its icon.

    def rescale(self, scaleX, scaleY=-100):
        if scaleY==-100 and scaleX>0:
            scaleY=scaleX #use common ratio
        if scaleX>0:
            self.size=self.size[0]*scaleX, self.size[1]*scaleY
            self.reinit()
        else:
            raise ValueError("Size must be positive!")
        "" #a function that changes the height and width of an element by a common ratio, then updates its icon.

if os.path.basename(__file__)=="PyGameTemplate.py":
    input("Press Enter to exit the script...")
