import sys


# import pydoc

def rconcat(a, b):
    """use 'return' in a loop"""
    for ia in a:
        print(ia)
    for ib in b:
        print(ib)
    return None


def yconcat(a, b, c):
    """using 'yield' in a  loop"""
    try:
        for ia in range(a):
            yield ia
        for ib in range(b,c):
            yield ib
        # for xb in range(sys.maxsize):
        yield "END"
    except ValueError:
        print("V-FINISHED!")
    except OverflowError:
        print("O-FINISHED!")
    except Exception:
        print("E-FINISHED!")


# for r in rconcat(range(5), range(9, 13)):
#     print(r)
print( rconcat(range(5), range(13)) )

print('==============================================')

# Notice the use of the yield statement, instead of return. We can now use something like:
ytester = yconcat(5, 9, 13)
print(f"type(yconcat) = {type(yconcat)}")
print(f"type(ytester) = {type(ytester)}")

print(next(ytester))
print('break')
for r in range(13):
    # print(ytester.send(7))
    print(next(ytester))
print('break')
print(ytester.send((3,6,9)))

# Notice the use of the yield statement, instead of return. We can now use something like
# for y in yconcat(range(5), range(9, 13)):
#     print(y)

# help(yconcat)
# pydoc.writedoc('yield_test')

exit()
