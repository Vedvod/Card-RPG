    
    def circle_movement(self, direction, speed):
        return project(((0, 0), direction), ((0, 0), (0, speed)))

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
        self.blocker=False



        
Element((a, d), get_target("GameAssets.lnk")+r"\marker.png", (2, 2)).place()
    "" #the base class for all elements