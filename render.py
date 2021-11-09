# -*- coding: UTF-8 -*-
import curses
CARDY, CARDX = 9, 15 

fmap = lambda a, b: list(map(a, b))
do = lambda a, b: (lambda _: b)(a)
noop = lambda: () 

def checkSize(scr):
  height, width = scr.getmaxyx()
  if height < CARDY*2: 
    return False
  return True
      
def card(scr, card):
  height, width = scr.getmaxyx()
  cen_y, cen_x = int(height/2), int(width/2)
  cb = scr.subwin(CARDY, CARDX, 3, cen_x - int(CARDX/2)-1)
  cb.box()
  cb.addstr(1, 1, card)
  cb.addstr(CARDY-2, CARDX-1-len(card), card)

def choices(scr, cards):
  start = 0
  height, width = scr.getmaxyx()
  if len(cards) < int(width/CARDX): 
    start = 0
  if len(cards) - start < int(width/CARDX):
    start = len(cards) - int(width/CARDX)

  def draw():
    nonlocal height, width
    height, width = scr.getmaxyx()
    deck = scr.subwin(CARDY+2, width-2, height-CARDY-3, 1)
    deck.box()
    deck.addstr(0, 1, "Cards remaining: {}  (Scroll - Arrow keys)".format(len(cards)))
    p = list(zip(range(0, len(cards)), cards[start:]))[:int((width-2)/CARDX)]
    boxes = fmap(lambda c: (c[0], c[1], scr.subwin(CARDY, CARDX, height-CARDY-2, c[0]*CARDX+2)), p)
    fmap(lambda b: do(b[2].box(), 
                   do(b[2].addstr(1,1,b[1]), 
                      b[2].addstr(CARDY-2,CARDX-1-len(b[1]),b[1])))
        , boxes)

  def scroll(d):
    nonlocal start
    if 0 <= start+d < len(cards) - int(width/CARDX) + 1:
      start = start + d

  def click(x, y):
    rs = fmap(lambda c: (c, c*CARDX, (c+1)*CARDX), range(0, len(cards[start:])))
    l = list(filter(lambda c: c[1] <= x <= c[2] and height-CARDY-2 <= y < height - 2, rs))
    return l[0][0] + start if len(l) != 0 else -1

  def setCards(c):
    nonlocal cards, start
    cards = c 
    start = 0
    draw()

  return draw, scroll, click, setCards

def drawDeck(scr, cards):
  height, width = scr.getmaxyx()
  cen_y, cen_x = int(height/2), int(width/2)
  d = 0
  def draw():
    nonlocal d
    d = scr.subwin(CARDY, CARDX, 3, width-CARDX-14)
    d.box()
    d.addstr(2, 1, "Draw")

  def click(x, y):
    nonlocal d
    if width - CARDX - 14 < x < width - 14 and 3 < y < 3 + CARDY:
      d.addstr(1, 1, "a")

  return draw, click

def eventLoop(scr):
  curses.mousemask(1)
  curses.curs_set(0)

  cards = ["Clover 1", "Clover 2", "Diamond 3", "Clover 4", "Diamond 5", "Diamond 6", "Diamond 7", "Clover 8", "Diamond 9", "Diamond 10", "Diamond 11"]
  top = "Clover 1"
  cd, cs, cc, sc = choices(scr, cards)
  #dd, dc = drawDeck(scr, [])
  event = 0
  while event != ord("q"):
    if not checkSize(scr):
      scr.clear()
      scr.addstr("Screen is too small")
      scr.refresh()
      event = scr.getch()
      continue

    scr.refresh()
    scr.clear()
    scr.border(0)

    if event == curses.KEY_LEFT:
      cs(-1)
    elif event == curses.KEY_RIGHT:
      cs(1)
    elif event == curses.KEY_MOUSE:
      _, mx, my, _, _ = curses.getmouse()
      #dc(mx, my)
      selected = cc(mx, my)
      if selected != -1:
        top = cards[selected]
        del cards[selected]
        sc(cards)

    cd()
    card(scr, top)
    #dd()
    scr.refresh()
    event = scr.getch()


curses.wrapper(eventLoop)