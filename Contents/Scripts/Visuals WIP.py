debug=0 #debug is set to off
#-------------------------modules-------------------------
import os, pygame, random
x, y = (0, 30); os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#--------------------------setup--------------------------
if debug: print(os.cwd()) #debug message to ensure correct working directory
for i in os.getcwd().split(chr(92)): #makes a list of the steps in the directory
    try: a.append(i) #move onto the next step
    except: a=[i]
    try:
        if debug: print("/".join(a)+r"PyGameTemplate.py") #debug message to ensure the dir building is correct
        exec(open("/".join(a)+r"PyGameTemplate.py").read()) #attempt to locate template file at current dir level
        break #if the file is opened
    except:
        pass
original_size=display_size
screen = pygame.display.set_mode(display_size, pygame.RESIZABLE, pygame.SCALED)
print(display_size)
prev_size=display_size

#-----------------------function(s)-----------------------
def main_loop(sprite_list=[], colour_tuple = (55, 55, 55), background=Element(size_tuple=(1, 1), name="background")): #the main pygame loop
    fps=60
    fake=screen.copy()
    global first, display_size, prev_size
    while 1:
        fake.fill(colour_tuple)
        background.place(SURF=fake)
        for i in sprite_list:
            i.place(SURF=fake)
            if i.name=="marker":
                i.place()
            elif i.size[1]<150: i.rescale(1.002, 1.0105)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: print("Window was closed..."); pygame.quit(); sys.exit()
            if event.type == pygame.VIDEORESIZE and not first:
                time.sleep(0.1)
                print(screen.get_rect().size)
            if pygame.mouse.get_pressed()[0]:
                print(cartesian(pygame.mouse.get_pos()))

        pygame.display.flip()
        if first:
            first=False
        prev_size=display_size; display_size=screen.get_rect().size
        screen.blit(pygame.transform.scale(fake, display_size), (160, 0))
        pygame.time.delay(int(1000/fps))
        
#--------------------------setup--------------------------
elements, bgcolour, background=0, (55, 55, 55), Element(size_tuple=(0, 0))
try:
    elements=(_:=eval((g:=open(r"level.cfg")).read()))["elements"] #unpack and assign level configurations
    bgcolour=_["bgcolour"]
    background=_["background"]
except:
    pass
finally:
    g.close()
    if debug: print(elements, bgcolour, background)

#------------------------main line------------------------
pygame.display.flip()
first=1
main_loop(elements, bgcolour, background)
input("Press Enter to exit the script...")
