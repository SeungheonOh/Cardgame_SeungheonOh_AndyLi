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
, "draw"   : ("/deck/{}/draw/?count={}", wrapFailure(drawParser))
, "shuffle": ("/deck/{}/shuffle/?remainting={}", wrapFailure(id))
}

api = mkEndpoints(apiDef)

deck_id = api["new"](4)
print(deck_id)

print(api["draw"](deck_id, 5))
print(api["shuffle"](deck_id, True))