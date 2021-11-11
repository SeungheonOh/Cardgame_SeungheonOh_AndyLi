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

codes = lambda di: fmap(lambda d: d["code"], di["cards"])
fullName = lambda s: fn2(s[1]) + " " + fn1(s[0])
fn1 = lambda s: (lambda n: s if n == None else n)(
                { "A" : "Ace" 
                , "J" : "Jack"
                , "Q" : "Queen"
                , "K" : "King"
                , "0" : "10"
                }.get(s))
fn2 = lambda s: (lambda n: s if n == None else n)(
                { "H" : "Heart" 
                , "D" : "Diamond"
                , "S" : "Spade"
                , "C" : "Clover"
                }.get(s))

decks = lambda deck_id, players: fmap(lambda p: codes(api["list"](deck_id, p)["piles"][p]), players)

api = mkEndpoints(apiDef)

def game_start(num_players):
  temp = []
  deck_id = api["new"](1)
  cnt = [0 for i in range(num_players)]
  for i in range (0, 52):
    cnt[i%num_players]+=1

  for i in range(0, num_players):
    code_list = codes(api["random"](deck_id, cnt[i]))
    api["add"](deck_id, "P{}".format(i), ",".join(code_list))
    temp.append("P{}".format(i))
  return deck_id, temp

#deck_id, players = game_start(5)