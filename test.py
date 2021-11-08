do = lambda a, b: (lambda _: b)(a)
loop = lambda _, a: loop(a, a)

loop(None, print("test"))