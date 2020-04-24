#!/usr/bin/env python3

# birthday paradox

def bday(n) -> float:
    """WRITE n birthday percentages"""
    if n == 1:
        print(F"{n:>4} {100:>11.4f}")
        return 1.0

    prev = bday(n-1)

    val = prev * ( (366-n) / 365 )
    print(F"{n:>4} {(val*100.0):>11.4f}")
    return val

if __name__ == "__main__":
    import sys
    bday( int(sys.argv[1]) )
