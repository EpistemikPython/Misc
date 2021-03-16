
def yconcat(a, b):
    for i in a:
        yield i
    for i in b:
        yield i

# Notice the use of the yield statement, instead of return. We can now use this something like

for i in yconcat(range(5), range(6, 13)):
    print(i)
