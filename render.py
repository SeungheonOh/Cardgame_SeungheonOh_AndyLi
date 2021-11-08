import curses
from curses.textpad import Textbox, rectangle

def card(scr):
  card = "Clover 5"
  cardy, cardx = 22, 30 
  scr.border(0)
  height, width = scr.getmaxyx()
  cen_y, cen_x = int(height/2), int(width/2)
  box1 = scr.subwin(cardy, cardx, 5, cen_x - int(cardx/2))
  box1.box()
  ch, cw = box1.getmaxyx()
  box1.addstr(1, 1, card)
  box1.addstr(cardy-2, cardx-1-len(card), card)

def eventLoop(scr):
  k = 0
  while k != ord("q"):
    scr.clear()

    card(scr)
    scr.refresh()
    k = scr.getch()

curses.wrapper(eventLoop)