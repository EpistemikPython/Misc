import sys


# import pydoc

def rconcat(a, b):
    """use 'return' in a loop"""
    for ia in a:
        print(ia)
    for ib in b:
        print(ib)
    return None


# for r in rconcat(range(5), range(9, 13)):
#     print(r)
print( rconcat(range(5), range(13)) )


def yconcat(a, b, c):
    """using 'yield' in a  loop"""
    for ia in range(a):
        yield ia
    for ib in range(b,c):
        yield ib
    # for xb in range(sys.maxsize):
    yield "END"


# Notice the use of the yield statement, instead of return. We can now use something like
# for y in yconcat(range(5), range(9, 13)):
#     print(y)

print('\n==============================================\n')

# create a generator
ytester = yconcat(5, 9, 13)
print(f"type(yconcat) = {type(yconcat)}")
print(f"type(ytester) = {type(ytester)}")

try:
    print(next(ytester))
    print('break')
    for r in range(13):
        print(f"{r}: {next(ytester)}")
except StopIteration:
    print('StopIteration')

print('\nbreak')
# restart the generator
ytester = yconcat(3,6,9)
for r in range(5):
    print(f"{r}: {next(ytester)}")


# help(yconcat)
# pydoc.writedoc('yield_test')

exit()
