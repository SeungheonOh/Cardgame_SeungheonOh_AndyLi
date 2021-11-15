import os
import random
import time
import pygame
from pygame.locals import *

import api

MULT = 1
CARDX, CARDY = int(226 * MULT), int(314 * MULT)
WINX, WINY = int(1500 * MULT), int(900 * MULT)

cardFile = lambda d: "resources/{}.png".format(d)
fmap = lambda a, b: list(map(a, b))
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K", "A"]
nextValid = lambda a, b: (lambda d: d[d.index(a)] == d[d.index(b)] or d[d.index(a)] == d[d.index(b)-1])(cards)
cc = lambda a: a[0]
varify = lambda a, b: nextValid(cc(a), cc(b))

def drawText(screen, s, x, y):
  if s == "" or s == None:
    return
  font = pygame.font.Font(None, 24)
  font_color = (255,255,255)
  font_background = (0,0,0)
  t = font.render(s, True, font_color, font_background)
  screen.blit(t, (x, y))

def drawCard(screen, card, x, y, w, h):
  pic = pygame.transform.scale(pygame.image.load(cardFile(card)), (w, h))
  screen.blit(pic, (x, y))

def card(screen, card):
  _, cen_x = int(WINY/2), int(WINX/2)
  drawCard(screen, card, cen_x - int(CARDX/2), 3, CARDX, CARDY)

def choices(screen, cards):
  start = 0 
  cards = cards
  if len(cards) < int(WINX/CARDX):
    start = 0
  if start > 0 and len(cards) - start < int(WINX/CARDX):
    start = len(cards) - int(WINX/CARDX)
  
  def draw():
    drawText(screen, "Cards Remaining {}".format(len(cards)), 0, WINY-CARDY-15)
    p = list(zip(range(0, len(cards)), cards[start:]))[:int((WINX-2)/CARDX)]
    fmap(lambda c: drawCard(screen, c[1], c[0]*CARDX + int((WINX-len(p) * CARDX)/2), WINY-CARDY, CARDX, CARDY), p)

  def scroll(d):
    nonlocal start
    if 0 <= start+d < len(cards) - int(WINX/CARDX) + 1:
      start = start + d

  def click(x, y):
    offset = int((WINX-len(cards[start:][:int((WINX-2)/CARDX)]) * CARDX)/2)
    rs = fmap(lambda c: (c, c*CARDX, (c+1)*CARDX), range(0, len(cards[start:])))
    l = list(filter(lambda c: c[1] <= x-offset <= c[2] and WINY-CARDY-2 <= y < WINY - 2, rs))
    return cards[l[0][0] + start] if len(l) != 0 else None

  def setCards(c):
    nonlocal cards, start
    cards = c 
    start = 0
    draw()
  
  def c():
    nonlocal cards
    return cards

  return draw, scroll, click, setCards, c

def computer(screen, d, curr, bsable):
  if bsable:
    if 0 < random.randint(0, 100) < 40:
      while True:
        screen.fill((0,100,0))
        drawText(screen, "You got caught BSing the computer, prepare to be exterminated", 150, WINY/2)
        pic = pygame.image.load(cardFile("rob"))
        pic = pygame.transform.scale(pic, (pic.get_width() * 0.6,pic.get_height()*0.6))
        screen.blit(pic, (int(WINX * 0.6), int(WINY * 0.4)))

        pygame.display.flip()
        for event in pygame.event.get():
          if event.type == QUIT:
              pygame.display.quit()
          elif event.type == KEYDOWN:
            if event.key == K_q:
              pygame.display.quit()

  deck = api.decks(d, ["P0", "P1"])[1]
  if 0 < random.randint(0, 100) < 70:
    pick = list(filter(lambda c: varify(curr, c), deck))
    if len(pick) == 0:
      pick = deck[0]
    else:
      pick = pick[0]
    api.api["return"](d, "P1", pick)
    return pick, not varify(curr, pick)
  else:
    pick = deck[random.randint(0, len(deck)-1)]
    api.api["return"](d, "P1", pick)
    return pick, not varify(curr, pick)

def win(screen):
  while True:
    screen.fill((0,100,0))
    drawText(screen, "You won", 150, WINY/2)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == QUIT:
          pygame.display.quit()
      elif event.type == KEYDOWN:
        if event.key == K_q:
          pygame.display.quit()

def main():
  deck_id, players = api.game_start(2)

  bullshitable = False
  bullshitcatchable = False
  pygame.init()
  screen = pygame.display.set_mode((WINX, WINY), HWSURFACE | DOUBLEBUF)

  current = "0H"
  dd, ds, dc, du, dgc = choices(screen, api.decks(deck_id, players)[0])

  while True:
    screen.fill((0,100,0))
    card(screen, current)
    dd()
    drawText(screen, "BS" if bullshitable else None, 10, 5)
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
        elif event.key == K_SPACE:
          if bullshitcatchable:
            win(screen)
      elif event.type == MOUSEBUTTONDOWN:
        if event.button == 4: ds(-1)
        elif event.button == 5: ds(1)
        if event.button == 1: 
          x, y = pygame.mouse.get_pos()
          cn = dc(x, y)
          if cn == None: 
            continue
          if not varify(current, cn):
            bullshitable = True
          else: 
            bullshitable = False
          drawText(screen, "Processing...", 10, 25)
          pygame.display.flip()
          current = cn
          api.api["return"](deck_id, "P0", current)
          du(api.decks(deck_id, players)[0])
          dd()
          pygame.display.flip()

          drawText(screen, "Computer Turn...", 10, 25)
          pygame.display.flip()
          current, bullshitcatchable = computer(screen, deck_id, current, bullshitable)
          

main()