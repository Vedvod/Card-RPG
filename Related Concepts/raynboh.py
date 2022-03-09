max_val=137
def space(x, l=3):
    while len(str(x))<l:
        x=str(x)+" "
    return x

class N:
    def __init__(self, val, tick):
        self.val=val
        self.tick=tick
a, b, c = N(max_val, max_val), N(0, max_val*2), N(0, max_val*3)
fps=50
def rainbow(a, b, c):
    for i in [a, b, c]:
        if i.tick>=max_val*3:
            i.tick=0
        if i.tick<max_val:
            i.val+=1
        elif i.tick<max_val*2:
            i.val-=1
        i.tick+=1
    print(space(a.val), space(b.val), space(c.val))
    return a, b, c
while 1:
    a, b, c = rainbow(a, b, c)
