import sys

try:
    val = int(sys.argv[1])
    print(F"val = {val}")
    if val > 10:
        raise Exception("bad val")
    print("val NOT > 10")
except Exception as e:
    e_msg = repr(e)
    print(e_msg)
    tb = sys.exc_info()[2]
    print(F"type tb = {type(tb)}")
