
import pydoc

def rconcat(a, b):
    """use 'return' in a loop"""
    for ia in a:
        return ia
    for ib in b:
        return ib

def yconcat(a, b):
    """using 'yield' in a  loop"""
    for ia in a:
        yield ia
    for ib in b:
        yield ib


# for r in rconcat(range(5), range(9, 13)):
#     print(r)
print( rconcat(range(5), range(13)) )

print('break')

# Notice the use of the yield statement, instead of return. We can now use something like
for y in yconcat(range(5), range(9, 13)):
    print(y)

# help(yconcat)
pydoc.writedoc('yield_test')
