import pygame,random
pygame.init()
w,h=600,600
s=pygame.display.set_mode((w,h))
pygame.display.set_caption("spce")
c=pygame.time.Clock()
f=pygame.font.SysFont(None,48)
plr=pygame.Rect(w//2-25,h-60,50,30)
b=[]
e=[pygame.Rect(x*60+50,y*50+30,40,30)for y in range(3)for x in range(8)]
d=1
es=1
bs=-5
r=True
while r:
 c.tick(60)
 s.fill((0,0,0))
 for ev in pygame.event.get():
  if ev.type==pygame.QUIT:r=0
 k=pygame.key.get_pressed()
 if k[pygame.K_LEFT]and plr.left>0:plr.x-=5
 if k[pygame.K_RIGHT]and plr.right<w:plr.x+=5
 if k[pygame.K_SPACE]:
  if len(b)<5:b+=[pygame.Rect(plr.centerx-2,plr.y,5,10)]
 for x in b[:]:
  x.y+=bs
  if x.y<0:b.remove(x)
 md=False
 for en in e:en.x+=d*es
 for en in e:
  if en.right>=w or en.left<=0:md=True
 if md:
  d*=-1
  for en in e:en.y+=10
 for x in b[:]:
  for y in e[:]:
   if x.colliderect(y):b.remove(x);e.remove(y);break
 for en in e:
  if en.colliderect(plr)or en.bottom>h:
   s.blit(f.render("GAME OVER",1,(255,0,0)),(w//2-100,h//2));pygame.display.flip();pygame.time.delay(2000);r=0
 if not e:
  s.blit(f.render("YOU WIN!",1,(0,255,0)),(w//2-100,h//2));pygame.display.flip();pygame.time.delay(2000);r=0
 pygame.draw.rect(s,(0,255,0),plr)
 for x in b:pygame.draw.rect(s,(255,255,255),x)
 for x in e:pygame.draw.rect(s,(255,0,0),x)
 pygame.display.flip()
pygame.quit()
