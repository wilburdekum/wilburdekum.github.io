"""Wilbur Dekum sketch icon generator. Deterministic wobble per icon name.
Run: python3 generate_icons.py  (writes SVGs into the current directory)"""
import math, random

def wob(pts, amp=0.65, seg=3.5, rng=None):
    out=[]
    for i in range(len(pts)-1):
        (x0,y0),(x1,y1)=pts[i],pts[i+1]
        dx,dy=x1-x0,y1-y0
        L=math.hypot(dx,dy)
        n=max(2,int(L/seg))
        px,py=(-dy/L, dx/L) if L else (0,0)
        off=0.0
        for k in range(n+1):
            t=k/n
            off += rng.uniform(-amp,amp)*0.6
            off *= 0.85
            pin = min(min(t,1-t)*2*2.2, 1.0)
            o=off*pin
            out.append((x0+dx*t+px*o, y0+dy*t+py*o))
    return out

def path_from(pts):
    return "M%.2f %.2f "%pts[0] + " ".join("L%.2f %.2f"%p for p in pts[1:])

def line(*pts, amp=0.65, rng=None):
    return path_from(wob(list(pts), amp=amp, rng=rng))

def arc(cx,cy,rx,ry,a0,a1,amp=0.55,rng=None,steps=None):
    a0,a1=math.radians(a0),math.radians(a1)
    n=steps or max(10,int(abs(a1-a0)*max(rx,ry)/3))
    pts=[]; off=0.0
    for k in range(n+1):
        t=k/n; a=a0+(a1-a0)*t
        off+=rng.uniform(-amp,amp)*0.5; off*=0.85
        pts.append((cx+(rx+off)*math.cos(a), cy+(ry+off)*math.sin(a)))
    return path_from(pts)

def circle(cx,cy,r,amp=0.5,rng=None):
    s=rng.uniform(0,360)
    return arc(cx,cy,r,r,s,s+368,amp=amp,rng=rng)

def dot(cx,cy,r=1.5,rng=None):
    return circle(cx,cy,r,amp=0.25,rng=rng)

ICONS={}
def icon(name):
    def deco(fn): ICONS[name]=fn; return fn
    return deco

@icon('bar-chart')
def _(r):
    p=[line((7,41),(41,41),rng=r)]
    for x,h in ((11,13),(20,24),(29,18)):
        p+=[line((x,41),(x,41-h),rng=r), line((x,41-h),(x+7,41-h),rng=r), line((x+7,41-h),(x+7,41),rng=r)]
    return p

@icon('line-chart')
def _(r):
    return [line((9,7),(9,41),rng=r), line((9,41),(43,41),rng=r),
            line((12,34),(20,25),(27,30),(40,13),amp=0.5,rng=r),
            line((35,13),(40,13),(40,18),rng=r)]

@icon('pie-chart')
def _(r):
    return [circle(24,24,16,rng=r), line((24,24),(24,8),rng=r), line((24,24),(39,30),rng=r)]

@icon('scatter-plot')
def _(r):
    p=[line((9,7),(9,41),rng=r), line((9,41),(43,41),rng=r)]
    for x,y in ((15,33),(20,27),(25,31),(28,21),(33,24),(38,14),(17,18)):
        p.append(dot(x,y,1.7,rng=r))
    return p

@icon('database')
def _(r):
    return [arc(24,12,14,5,0,360,rng=r), line((10,12),(10,36),rng=r), line((38,12),(38,36),rng=r),
            arc(24,36,14,5,0,180,rng=r), arc(24,24,14,5,10,170,rng=r)]

@icon('server-stack')
def _(r):
    p=[]
    for y in (8,21,34):
        p+=[line((8,y),(40,y),(40,y+8),(8,y+8),(8,y),rng=r), dot(13,y+4,1.2,rng=r), line((30,y+4),(36,y+4),rng=r)]
    return p

@icon('pipeline')
def _(r):
    return [line((5,20),(43,20),rng=r), line((5,28),(43,28),rng=r),
            line((15,17),(15,31),rng=r), line((31,17),(31,31),rng=r),
            dot(10,24,1.4,rng=r), dot(23,24,1.4,rng=r), dot(37,24,1.4,rng=r)]

@icon('table')
def _(r):
    return [line((8,10),(40,10),(40,38),(8,38),(8,10),rng=r),
            line((8,19),(40,19),rng=r), line((8,28),(40,28),rng=r), line((22,10),(22,38),rng=r)]

@icon('dashboard')
def _(r):
    p=[line((6,8),(42,8),(42,40),(6,40),(6,8),rng=r), line((6,15),(42,15),rng=r),
       dot(10,11.5,1.0,rng=r), dot(14.5,11.5,1.0,rng=r)]
    p+=[line((11,35),(11,29),rng=r), line((16,35),(16,24),rng=r), line((21,35),(21,31),rng=r)]
    p+=[line((28,33),(32,26),(35,29),(39,21),amp=0.45,rng=r)]
    return p

@icon('gauge')
def _(r):
    return [arc(24,34,15,15,180,360,rng=r), line((9,34),(12,34),rng=r), line((36,34),(39,34),rng=r),
            line((24,34),(32,22),rng=r), dot(24,34,1.8,rng=r)]

@icon('funnel')
def _(r):
    return [line((8,9),(40,9),rng=r), line((8,9),(21,25),(21,38),rng=r), line((40,9),(27,25),(27,38),rng=r),
            dot(24,43,1.2,rng=r)]

@icon('flow-dag')
def _(r):
    return [circle(11,12,4.5,rng=r), circle(11,36,4.5,rng=r), circle(37,24,4.5,rng=r),
            line((15,14.5),(32.5,22),rng=r), line((15,33.5),(32.5,26),rng=r)]

@icon('insight-lens')
def _(r):
    return [circle(20,20,12.5,rng=r), line((29.5,29.5),(41,41),rng=r),
            line((15,26),(15,21),rng=r), line((20,26),(20,15),rng=r), line((25,26),(25,23),rng=r)]

@icon('report')
def _(r):
    return [line((14,6),(30,6),rng=r), line((30,6),(30,13),(37,13),rng=r), line((30,6),(37,13),rng=r),
            line((37,13),(37,42),(14,42),(14,6),rng=r),
            line((19,20),(32,20),rng=r), line((19,25),(32,25),rng=r),
            line((20,37),(20,32),rng=r), line((25,37),(25,29),rng=r), line((30,37),(30,34),rng=r)]

@icon('cloud-data')
def _(r):
    return [arc(17,26,7,7,90,270,rng=r), arc(23,19,8,8,150,380,rng=r), arc(33,27,6,6,270,450,rng=r),
            line((17,33),(33,33),rng=r),
            line((17,38),(17,41),rng=r), line((24,38),(24,42),rng=r), line((31,38),(31,41),rng=r)]

@icon('compass')
def _(r):
    return [circle(24,24,15.5,rng=r),
            line((24,12),(28.5,24),(24,36),(19.5,24),(24,12),rng=r), dot(24,24,1.4,rng=r)]

@icon('team')
def _(r):
    return [circle(16,16,5,rng=r), circle(32,16,5,rng=r),
            arc(16,36,8.5,10,180,360,rng=r), arc(32,36,8.5,10,180,360,rng=r)]

@icon('target')
def _(r):
    return [circle(24,24,15,rng=r), circle(24,24,8,rng=r), dot(24,24,1.8,rng=r)]

HEAD=('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" '
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')

if __name__ == '__main__':
    for name,fn in ICONS.items():
        rng=random.Random(name)
        body="".join('<path d="%s"/>'%d for d in fn(rng))
        open(f'{name}.svg','w').write(HEAD+body+'</svg>')
    print(len(ICONS), 'icons written')
