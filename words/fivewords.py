#!/usr/bin/env python3

import itertools
import array

anagrams = False
firstletter = [{} for f in range(26)]
wordnames = {}

# TODO: find the proper balance between these two implementations
#
# def compress(word):
#  shift = (word ^ (word - 1)).bit_length()
#  return ((shift - 1) << 8) | ((word >> shift) & 255)
#
# def decompress(pack):
#  shift = pack >> 8
#  bits = pack & 255
#  return (bits * 2 + 1) << shift

def compress(pword):
    return (pword ^ (pword-1)).bit_length()-1

def decompress(ppack):
    return 1 << ppack

def letter_to_bit(ch):
    return 'aesiorunltycdhmpgkbwfvzjxq'.find(ch)
    # return ord(c) - ord('a')


with open('input/words_alpha.txt') as wordlist:
    for word in wordlist.read().split():
        if len(word) == 5:
            mask = 0
            word = word.lower()
            for c in word:
                i = letter_to_bit(c)
                if not (0 <= i < 26): break
                b = 1 << i
                if mask & b: break
                mask |= b
            else:
                mfirst = mask.bit_length()-1
                pack = compress(mask)
                wordnames.setdefault(mask, set()).add(word)
                firstletter[mfirst].setdefault(pack, set()).add(mask)

count = 0

def emit(progress):
    global count
    if anagrams:
        for s in itertools.product(*(wordnames[wd] for wd in progress)):
            print(*sorted(s))
            count += 1
    else:
        print(*sorted(next(iter(wordnames[wd])) for wd in progress))
        count += 1

def solve(alphabet, grace=1, progress=array.array('L', (0, 0, 0, 0, 0)), depth=0):
    for drop in range(grace+1):
        first = alphabet.bit_length()-1
        for fpack in firstletter[first]:
            required = decompress(fpack)
            if (alphabet & required) == required:
                for fmask in firstletter[first][fpack]:
                    if (fmask & alphabet) == fmask:
                        progress[depth] = fmask
                        if depth >= 4:
                            emit(progress)
                        else:
                            solve(alphabet & ~fmask, grace-drop, progress, depth+1)
        alphabet ^= 1 << first


solve( (1 << 26)-1 )
print(f'total: {count}')
exit()
