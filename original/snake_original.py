import pygame, random, sys
pygame.init()
w,h=600,400
s=pygame.display.set_mode((w,h))
c=pygame.time.Clock()
f=20
x,y=100,100
dx,dy=20,0
b=[(x,y)]
l=5
fx,fy=random.randrange(0,w,f),random.randrange(0,h,f)
while 1:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:sys.exit()
        elif e.type==pygame.KEYDOWN:
            if e.key==pygame.K_UP and dy==0:dx,dy=0,-f
            elif e.key==pygame.K_DOWN and dy==0:dx,dy=0,f
            elif e.key==pygame.K_LEFT and dx==0:dx,dy=-f,0
            elif e.key==pygame.K_RIGHT and dx==0:dx,dy=f,0
    x+=dx
    y+=dy
    if x<0 or x>=w or y<0 or y>=h or (x,y) in b:break
    b.append((x,y))
    if len(b)>l:b.pop(0)
    if x==fx and y==fy:
        l+=1
        while (fx,fy) in b:
            fx,fy=random.randrange(0,w,f),random.randrange(0,h,f)
    s.fill((0,0,0))
    for p in b:pygame.draw.rect(s,(0,255,0),pygame.Rect(p[0],p[1],f,f))
    pygame.draw.rect(s,(255,0,0),pygame.Rect(fx,fy,f,f))
    pygame.display.flip()
    c.tick(10)
