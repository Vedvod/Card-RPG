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
def con(self, speed=50):
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
    if self.position[0]<-w/2:
        self.move(w-1, 0)
    elif self.position[0]>w/2:
        the_player.move(-w+1, 0)
    if self.position[1]<-h/2:
        self.move(0, h-1)
    elif self.position[1]>h/2:
        self.move(0, -h+1)
    self.place()
Player.controls=con
#-------------------------classes-------------------------
class Key(Element, pygame.sprite.Sprite):
    def __init__(self, player=Player(), coords=(0, 0), key_name="base_key", size_tuple="", degrees_of_rotation=0, ):
        super().__init__(coords, rf'{get_target("GameAssets.lnk")}/Keys/{key_name}.png', size_tuple, degrees_of_rotation)
        self.player=player

    def collide():
        pass

    def rect_check(self):
        print("A") if set(self.rect()[0])&set(self.player.rect()[0]) else 1

#--------------------------setup--------------------------
found_keys="ASD"
the_player=Player(coords=(0, 30), paths_to_assets=[f"""{get_target("GameAssets.lnk")}\Karl\{i}.png""" for i in ("karl1", "karl2")], size_tuple=(_:=40, _))
W=Key(the_player, coords=(100, 40), size_tuple=(20, 20), key_name="key_w")
trombone=play(get_target("GameAssets.lnk")+"\lose_trombone.mp3"); trombone.set_volume(0.15); trombone.stop()
fps=60

#------------------------main line------------------------
def main_loop():
    W.place()
    W.rect_check()

    the_player.controls(_/10)
    if the_player.time.time()>=0.15:
        the_player.anim()
        the_player.time.reset()
    pygame.display.flip()
    pygame.time.delay(int(1000/fps))
    screen.fill((132, 30, 95))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.display.quit(); return True

ended=False
while not ended:
    ended=main_loop()
trombone.play()
time.sleep(3)
input("Press Enter to exit the script...")
pygame.quit()