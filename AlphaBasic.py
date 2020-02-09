import math
class Vector :
    """2d vector with x and y values"""
    def __init__ (self,x,y):
        self.x = x
        self.y = y
    def __add__ (self,other):
        return Vector(self.x+other.x,self.y+other.y)
    def __sub__ (self,other):
        return Vector(self.x-other.x,self.y-other.y)
    def __str__ (self):
        return f'x:{self.x}     y:{self.y}'
    def __div__ (self,other):
        return Vector (self.x/other.x,self.y/other.y)

def dist (a,b,distance = True,c =None):
    dists = Vector (abs(a.x-b.x),abs(a.y-b.y))
    if not (distance) and c == None:
        return dists
    else:
        dist = math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
        if distance and c == None:
            return dist
        elif c != None:
            if dist>c:
                return False
            else :
                return True
def vectorfinder (start,point):
    v = dist (start,point,False)
    if point.x < start.x:
        v.x*= -1
    if point.y < start.y :
        v.y*= -1
    return v
def pathfinder (start,point,step):
    if step == 0:
        return Vector(0,0)
    v = vectorfinder (start,point)
    d = dist (start,point,False)
    if d.x < step and d.y < step:
        return v
    if d.x >= d.y:
        t = d.x/step
        if v.x < 0:
            step *= -1
        return Vector(step,v.y/t)
    else :
        t = d.y/step
        if v.y < 0:
            step *= -1
        return Vector (v.x/t,step)
def closest (me,where,typ = tuple()):
    target = None
    for l in where:
        for en in l:
            if not str (en) in typ and len (typ) !=0 :
                continue
            if target == None:
                target = en
            else :
                if dist (me,en,True,dist(me,target)):
                    target = en
def closes (me,where,dis,typ = tuple (),exc = tuple ()):
    for w in where:
        for en in w:
            if dist (me,en.center,True,dis) and (type(en) in typ or len (typ) == 0) and not type (en) in exc:
                yield en
def collision  (pos,en):
    return en.coord.x <= pos.x and en.coord.x + en.w >= pos.x and en.coord.y <= pos.y and en.coord.y + en.hg >= pos.y
class Entity ():
    def __init__ (self,x,y,w,hg):
        self.x = x
        self.y = y
        self.w = w
        self.hg = hg
    def __str__ (self):
        return str (dict (self)).replace ('{','').replace ('}','')
