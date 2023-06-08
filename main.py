import pygame
import time
import random
pygame.font.init()

WIDTH,HEIGHT=600,400
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Ippolito Beach Simulator")
BG2=pygame.image.load("bg3.png")
BG2=pygame.transform.scale(BG2,(WIDTH,HEIGHT))
CHAR=pygame.image.load("char.png")
CHAR2=pygame.image.load("char2.png")
PLAYER_WIDTH=40
PLAYER_HEIGHT=60
t1=0
t2=0
PLAYER_VEL=5
STAR_WIDTH=10
STAR_HEIGHT=20
STAR_VEL=3
CD=False
cdtime=0
invincible=False
FONT=pygame.font.SysFont("Arial",30)
def draw(player,elapsed_time,stars):
  WIN.blit(BG2,(0,0))

  time_text=FONT.render(f"Time:{round(elapsed_time)}s",1,"white")
  WIN.blit(time_text,(10,10))
  cool_text=FONT.render(f"Shield: ",1,"white")
  WIN.blit(cool_text,(10,50))


  
  #draw player
  if invincible:
    WIN.blit(CHAR2,(player))
  else:
    WIN.blit(CHAR,(player))
  #pygame.draw.rect(WIN,"blue",player)
  #pygame.draw.rect(WIN,"black",player)
  if CD:
    pygame.draw.rect(WIN,"red", (110,55,30,30))
  elif not(CD):
    pygame.draw.rect(WIN,"green",(110,55,30,30))

  for star in stars:
    pygame.draw.rect(WIN,"white",star)
  pygame.display.update()
def main():
  global invincible
  global cdtime
  global CD
  run=True

  player=pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER_HEIGHT)

  clock=pygame.time.Clock()

  start_time=time.time()
  elapsed_time=0
  
  star_add_increment=1000
  star_count=0
  stars=[]
  hit=False
  while run:
    star_count+=clock.tick(60)
    elapsed_time=time.time()-start_time
    t2=pygame.time.get_ticks()

    if cdtime-t2<=0:
      CD=False
    elif cdtime-t2>=0:
      CD=True
    if invincible and t2-t1>1500:
      invincible=False
    
    if star_count>star_add_increment:
      c=random.randint(1,4)
      for _ in range(c):
        star_x=random.randint(0,WIDTH-STAR_WIDTH)
        star=pygame.Rect(star_x,-STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT)
        stars.append(star)
      star_add_increment=max(200,star_add_increment-20)
      star_count=0
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        run=False
        break

    keys=pygame.key.get_pressed()
    if keys[pygame.K_a] and player.x-PLAYER_VEL>=0:
      player.x-=PLAYER_VEL 
    if keys[pygame.K_d]and player.x+PLAYER_VEL+PLAYER_WIDTH<=WIDTH:
      player.x+=PLAYER_VEL 
    if keys[pygame.K_f]:
      if not(CD):
        invincible=True
        t1=pygame.time.get_ticks()
        cdtime=pygame.time.get_ticks()+10000
    for star in stars[:]:
      star.y+=STAR_VEL
      if star.y>HEIGHT:
        stars.remove(star)
      if invincible==False:
        if star.y + star.height >= player.y and star.colliderect(player):
          stars.remove(star)
          hit=True
          break
      if invincible:
        if star.colliderect(player):
          stars.remove(star)
    
    if hit:
      lost_text=FONT.render("You Lost!",1,"white")
      WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
      pygame.display.update()
      pygame.time.wait(1000)
      pygame.quit()
    draw(player,elapsed_time,stars) 

if __name__=="__main__":
  main()