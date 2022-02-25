debug=0
#-------------------------modules-------------------------
import os, random, time, sys, math, pygame
x, y = (0, 30); os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
for i in os.getcwd().split(chr(92)): #makes a list of the steps in the directory
    try: a.append(i) #move onto the next step
    except: a=[i]
    try:
        if debug: print("/".join(a)+r"PyGameTemplate.py") #debug message to ensure the dir building is correct
        exec(open("/".join(a)+r"PyGameTemplate.py").read()) #attempt to locate template file at current dir level
        break #if the file is opened
    except:
        pass
screen = pygame.display.set_mode(display_size, pygame.RESIZABLE, pygame.SCALED)
#-----------------------function(s)-----------------------
found=lambda x: x in found_keys
def e(self):
    print("baaaa!")
Player.controls2=e
#-------------------------classes-------------------------


#--------------------------setup--------------------------
found_keys=[]
me=Player(coords=(0, 30), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(80, 80))
trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
fps=60

#------------------------main line------------------------
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit(); #sys.exit()

    me.controls(5, True)
    me.controls2()
    if me.time()>=0.15:
        me.anim()
        me.reset()
    pygame.display.flip()
    pygame.time.delay(int(1000/fps))
    screen.fill((132, 30, 95))

input("Press Enter to exit the script...")
pygame.quit()