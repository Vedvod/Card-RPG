debug=0
#-------------------------modules-------------------------
import os, pygame
if debug: print(os.cwd())
for i in os.getcwd().split(chr(92)):
    try: a.append(i)
    except: a=[i]
    try:
        if debug: print("/".join(a)+r"PyGameTemplate.py")
        exec(open("/".join(a)+r"PyGameTemplate.py").read())
        break
    except:
        pass

#-----------------------function(s)-----------------------
def main_loop(sprite_list=[]):
    fps=60
    colour_tuple = 55, 55, 55
    while 1:
        screen.fill(colour_tuple)
        for i in sprite_list:
            i.place()
            i.move(x_shift=3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        pygame.display.flip()
        pygame.time.delay(int(1000/fps))
#-------------------------classes-------------------------

#--------------------------setup--------------------------
screen = pygame.display.set_mode(display_size)

#------------------------main line------------------------
main_loop([])
input("Press Enter to exit the script...")
