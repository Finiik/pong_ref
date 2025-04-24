import pygame,random
pygame.init()
s=pygame.display.set_mode((380,420))
pygame.display.set_caption("Pacman???")
c=pygame.time.Clock()
m=[list("1111111111111111111"),list("1000001000001000001"),list("1011101011101011101"),list("1020000000000000201"),
list("1010111011101011101"),list("1000101000101000101"),list("1111101111101111101"),list("0000000000000000000"),
list("1111101111111111101"),list("1000001000001000001"),list("1011101011101011101"),list("1020000000000000201"),
list("1010111011101011101"),list("1000101000101000101"),list("1111101111101111101"),list("1000000002000000001"),
list("1011101011101011101"),list("1000001000001000001"),list("1011111111111111101"),list("1000000000000000001"),
list("1111111111111111111")]
w,h=19,21
cs=20
d={(x,y)for y in range(len(m))for x in range(len(m[y]))if m[y][x]=="0"or m[y][x]=="2"}
p=[9,15]
g=[[9,7],[1,1],[17,1]]
dir=[0,0]
r=True
while r:
 s.fill((0,0,0))
 for y in range(h):
  for x in range(w):
   if m[y][x]=="1":pygame.draw.rect(s,(0,0,255),(x*cs,y*cs,cs,cs))
   elif (x,y) in d:pygame.draw.circle(s,(255,255,255),(x*cs+cs//2,y*cs+cs//2),3)
 for e in pygame.event.get():
  if e.type==pygame.QUIT:r=False
  elif e.type==pygame.KEYDOWN:
   if e.key==pygame.K_LEFT:dir=[-1,0]
   if e.key==pygame.K_RIGHT:dir=[1,0]
   if e.key==pygame.K_UP:dir=[0,-1]
   if e.key==pygame.K_DOWN:dir=[0,1]
 nx,ny=p[0]+dir[0],p[1]+dir[1]
 if 0<=nx<w and 0<=ny<h and m[ny][nx]!="1":p=[nx,ny]
 d.discard(tuple(p))
 for i in range(len(g)):
  pos=g[i]
  mv=[]
  for dx,dy in[(-1,0),(1,0),(0,-1),(0,1)]:
   nx,ny=pos[0]+dx,pos[1]+dy
   if 0<=nx<w and 0<=ny<h and m[ny][nx]!="1":mv.append((dx,dy))
  if mv:
   ch=random.choice(mv)
   g[i][0]+=ch[0]
   g[i][1]+=ch[1]
 for i in g:
  if i==p:
   print("GAME OVER >_<")
   r=False
 pygame.draw.circle(s,(255,255,0),(p[0]*cs+cs//2,p[1]*cs+cs//2),cs//2)
 for i in g:pygame.draw.circle(s,(255,105,180),(i[0]*cs+cs//2,i[1]*cs+cs//2),cs//2)
 pygame.display.flip()
 c.tick(10)
pygame.quit()
