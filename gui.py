import os
import pygame
from pygame.locals import *

MULT = 1
CARDX, CARDY = int(226 * MULT), int(314 * MULT)
WINX, WINY = int(1500 * MULT), int(900 * MULT)

cardFile = lambda d: "resources/{}.png".format(d)
fmap = lambda a, b: list(map(a, b))
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A"]
nextValid = lambda a, b: (lambda d: d[d.index(a)] == d[d.index(b)] or d[d.index(a)] == d[d.index(b)-1])(cards)
cc = lambda a: a[0]
varify = lambda a, b: nextValid(cc(a), cc(b))

def drawCard(screen, card, x, y, w, h):
  pic = pygame.transform.scale(pygame.image.load(cardFile(card)), (w, h))
  screen.blit(pic, (x, y))

def card(screen, card):
  cen_y, cen_x = int(WINY/2), int(WINX/2)
  drawCard(screen, card, cen_x - int(CARDX/2), 3, CARDX, CARDY)

def choices(screen, cards):
  start = 0 
  cards = cards
  if len(cards) < int(WINX/CARDX):
    start = 0
  if start > 0 and len(cards) - start < int(WINX/CARDX):
    start = len(cards) - int(WINX/CARDX)
  
  def draw():
    p = list(zip(range(0, len(cards)), cards[start:]))[:int((WINX-2)/CARDX)]
    fmap(lambda c: drawCard(screen, 
                            c[1], 
                            c[0]*CARDX + int((WINX-len(p) * CARDX)/2), 
                            WINY-CARDY,
                            CARDX, 
                            CARDY), 
        p)

  def scroll(d):
    nonlocal start
    if 0 <= start+d < len(cards) - int(WINX/CARDX) + 1:
      start = start + d

  def click(x, y):
    offset = int((WINX-len(cards[start:][:int((WINX-2)/CARDX)]) * CARDX)/2)
    rs = fmap(lambda c: (c, c*CARDX, (c+1)*CARDX), range(0, len(cards[start:])))
    l = list(filter(lambda c: c[1] <= x-offset <= c[2] and WINY-CARDY-2 <= y < WINY - 2, rs))
    return l[0][0] + start if len(l) != 0 else None

  def setCards(c):
    nonlocal cards, start
    cards = c 
    start = 0
    draw()

  return draw, scroll, click, setCards

def main():
  pygame.init()
  screen = pygame.display.set_mode((WINX, WINY), HWSURFACE | DOUBLEBUF)

  current = "0H"
  cards = ("JH QD KS AH JH QD KS JH QD KS 2S 3D 4C 5C 6H 7S 8D 9S 0C AH 2S 3D 4C 5C 6H 7S 8D 9S 0C AH 2S 3D 4C 5C 6H 7S 8D 9S 0C".split(" "))
  dd, ds, dc, du = choices(screen, cards)

  while True:
    screen.fill((0,100,0))
    card(screen, current)
    dd()
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == QUIT:
          pygame.display.quit()
      elif event.type == KEYDOWN:
        if event.key == K_q:
          pygame.display.quit()
        elif event.key == K_LEFT:
          ds(-1)
        elif event.key == K_RIGHT:
          ds(1)
      elif event.type == MOUSEBUTTONDOWN:
        if event.button == 4: ds(-1)
        elif event.button == 5: ds(1)
        if event.button == 1: 
          x, y = pygame.mouse.get_pos()
          cn = dc(x, y)
          if cn == None: 
            continue
          if not varify(current, cards[cn]):
            print("not vaild card")
            continue
          current = cards[cn]
          del cards[cn]
          du(cards)

main()
