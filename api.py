import requests

id      = lambda a: a
fmap    = lambda a, b: list(map(a, b))
zipdict = lambda a, b: dict(zip(a, b))
apply   = lambda a: lambda b: b(a)
comp    = lambda f, g: lambda *x: f(g(*x))
purge   = lambda l: list(filter(lambda a: a != None and a != [], l))
flatten = lambda l: [] if len(l) <= 0 else l[-1] + flatten(l[:-1])

apiURL = "https://deckofcardsapi.com/api"

getRec      = lambda r: lambda *a: requests.get((apiURL+r).format(*a))
mkEndpoints = lambda e: zipdict(list(e.keys()), fmap(lambda a: comp(a[1], getRec(a[0])), e.values()))

wrapFailure   = lambda p: lambda d: None if d.status_code != 200 else p(dict(d.json()))
defaultParser = lambda: wrapFailure(id)
newDeckParser = lambda d: None if d["success"] == False else d["deck_id"]
drawParser    = lambda d: d

apiDef = { 
  "new"    : ("/deck/new/shuffle/?deck_count={}", wrapFailure(newDeckParser))
, "random" : ("/deck/{}/draw/?count={}", wrapFailure(drawParser))
, "shuffle": ("/deck/{}/shuffle/?remainting={}", wrapFailure(id))
, "draw":   ("/deck/{}/pile/{}/draw/>?cards={}", wrapFailure(id))
, "add": ("/deck/{}/pile/{}/add/?cards={}", wrapFailure(id))
, "list":  ("/deck/{}/pile/{}/list", wrapFailure(id))
}

def get_code_list(dicta): 
  list1 = []
  for card in dicta['cards']:
    list1.append(card['code'])
  str1 = ""
  for card in list1:
    str1+=card+","
  str1 = str1[0:len(str1)-1]
  return str1

api = mkEndpoints(apiDef)
'''
deck_id = api["new"](1)
print(deck_id)

dicta = api["random"](deck_id, 5)
print(dicta)
print(api["add"](deck_id, "pileid", get_code_list(dicta)))
print(api["list"](deck_id, "pileid"))
'''

pile = lambda i: "player " + str(i)

def game_start(num_players):
  deck_id = api["new"](1)
  cnt = [0 for i in range(num_players)]
  
  for i in range (0, 52):
    cnt[i%num_players]+=1
  print(cnt)
  for i in range(0, num_players):
    code_list = get_code_list(api["random"](deck_id, cnt[i]))
    print(code_list)
    print(api["add"](deck_id, pile(i), code_list))
    #print(get_code_list(api["list"](deck_id, name(i))['piles'][name(i)]['cards']))
#print(api["add"](deck_id))

game_start(5)
'''
print(api["shuffle"](deck_id, True))
print(api["random"](deck_id, 1))
print(api["throw"](deck_id))
'''