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

#-----------------------function(s)-----------------------
def main_loop(sprite_list=[]): #the main pygame loop
    fps=60; colour_tuple = 55, 55, 55
    while 1:
        screen.fill(colour_tuple)
        for i in sprite_list:
            i.place()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.display.flip()
        pygame.time.delay(int(1000/fps))
#-------------------------classes-------------------------

#--------------------------setup--------------------------
screen = pygame.display.set_mode(display_size) #make the pygame screen

#------------------------main line------------------------
main_loop() 
input("Press Enter to exit the script...")
