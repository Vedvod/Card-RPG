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
pressed=lambda x: eval(f"pygame.key.get_pressed()[pygame.K_{x}]")
def e(self, speed=50):
    global pressed
    x, y = 0, 0
    if (pressed("LEFT") or pressed("a")) and found("A"):
        x-=speed
    if (pressed("RIGHT") or pressed("d")) and found("D"):
        x+=speed
    if (pressed("DOWN") or pressed("s")) and found("S"):
        y-=speed
    if (pressed("UP") or pressed("w")) and found("W"):
        y+=speed
    _=self.circle_movement((x, -y), speed)[1]
    if (x, y)!=(0, 0): self.move(_[0], _[1])

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
Player.controls=e
#-------------------------classes-------------------------


#--------------------------setup--------------------------
found_keys="AD"
me=Player(coords=(0, 30), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _))
trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
fps=60

#------------------------main line------------------------
def main_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit(); #sys.exit()

    me.controls(_/10)
    if me.time()>=0.15:
        me.anim()
        me.reset()
    pygame.display.flip()
    pygame.time.delay(int(1000/fps))
    screen.fill((132, 30, 95))

while 1:
    main_loop()

input("Press Enter to exit the script...")
pygame.quit()