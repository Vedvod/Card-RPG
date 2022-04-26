import cmath, math
def sprite(self): 
    return self.base[self.sprite_num-1]
    "" #a convenient shorthand for the currently toggled display sprite.
    
def anim(self):
    if self.anim_timer.time()>=0.15:
        self.anim_timer.reset()
        self.sprite_num = (self.sprite_num+1 if self.sprite_num<len(self.base) else 1)
        self.reinit()

class Element:
    def __init__(self, coords, paths_to_assets=get_target("GameAssets.lnk")+r"/DefaultSprite.png", size_tuple=chr(0), degrees_of_rotation=0, name="generic", sprite_num=1):
        self.position = Position(coords, True)
        self.base_images=[pygame.image.load(x) for x in (paths_to_assets if type(paths_to_assets)!=str else [paths_to_assets])]
        self.sprite = lambda: self.base_images[self.sprite_num-1]
        self.size = (size_tuple if size_tuple!=chr(0) else self.sprite().get_size())
        self.true_size=self.size
        self.icon=lambda: pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(self.sprite(), self.size), self.rotation), self.flipped[0], self.flipped[1])
        self.flipped=Position(False, False)
        self.solid=False
        self.name=name
        self.velocity=Vector(0, 0)

    def rotate(self, degrees_to_rotate):
        self.rotation+=degrees_to_rotate
        self.rotation=self.rotation%360
        "" #a function that offsets the rotaton of the element, and then updates its icon.

    def set_angle(self, degrees_of_rotation):
        self.rotation=degrees_of_rotation
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
        "" #a function that changes the size attribute of the element, then updates its icon.

    def rescale(self, scaleX, scaleY=-100, true=True):
        if scaleY==-100 and scaleX>0: #if scaleY has not been specified 
            scaleY=scaleX #use common ratio to scale
        if scaleX>0: #if scaleY was specified
            self.resize((self.size[0]*scaleX, self.size[1]*scaleY), true_size=true)
        else: #if scaleX was invalid
            raise ValueError("Size must be positive!")
        "" #a function that changes the height and width of an element by a common ratio, then updates its icon.

    def anim(self):
        if self.anim_timer.time()>=0.15:
            self.anim_timer.reset()
            self.sprite_num = (self.sprite_num+1 if self.sprite_num<len(self.base) else 1)
            self.reinit()

    def rect(self):
        top_left = Position(self.position.x-self.size[0]/2, self.position.y-self.size[1]/2)
        bottom_right = Position(self.position.x+self.size[0]/2, self.position.y+self.size[1]/2)
        return top_left, bottom_right

    def show_hitbox(self):
        a, b = (self.rect()[0].x, self.rect()[0].y)
        c, d = (self.rect()[1].x, self.rect()[1].y)
        Element((a, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((c, b), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
        Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()

    def check_clicked(self):
        if pygame.mouse.get_pressed()[0] and self.click_timer.time()>1:
            self.click_timer.reset()
            mouse_coords=pygame.mouse.get_pos()
            #COMPLETE THIS TO ACTUALLY DO STUFF PLS

    def place(self, coords=chr(0), SURF=screen): 
        if coords==chr(0): #if coordinates not specified
            coords=self.position #use Element's stored coordinates
        if self.name in debug[3]: print(f"Name: {self.name}, CPos: {coords}, Pos: {cartesian(coords)}")
        SURF.blit(self.icon, coords.tup()) #place element using cartesian coordinates
        "" #a function to place Elements on the SURFace
    "" #the base class for all elements