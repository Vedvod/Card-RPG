debug=0 #debug is set to off
#-------------------------modules-------------------------
import os, pygame

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

#-----------------------function(s)-----------------------
def main_loop(sprite_list=[], colour_tuple = (55, 55, 55), background=Element(size_tuple=(1, 1), name="background")): #the main pygame loop
    fps=60
    while 1:
        screen.fill(colour_tuple)
        background.place()
        for i in sprite_list:
            i.place()
            if i.size[1]<150: i.rescale(1.002, 1.0105)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: print("Window was closed..."); pygame.quit(); sys.exit()
            if event.type == pygame.VIDEORESIZE:
                time.sleep(0.1)
                global display_size    
                prev_size=display_size
                display_size=pygame.display.get_surface().get_size()
                for i in sprite_list+[background]:
                    i.rescale((display_size[0])/(prev_size[0]), (display_size[1])/(prev_size[1]))
        pygame.display.flip()
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
    print(elements, bgcolour, background)

#------------------------main line------------------------
main_loop(elements, bgcolour, background)
input("Press Enter to exit the script...")
