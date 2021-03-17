###############################################################################################################################
# coding=utf-8
#
# problem_tavs.py
#
#  Copyright (c) 2021  Thomas Sattolo  <tsattolo@gmail.com>

# In 1969, Hans Freudenthal posed a puzzle that Martin Gardner would later call “The Impossible Problem”.
# Below is a 2000 version due to Erich Friedman.
#
# I have secretly chosen two nonzero digits and have separately told their sum to Sam and their product to Pam,
# both of whom are honest and logical.
#
# Pam says, “I don’t know the numbers”.
# Sam says, “I don’t know the numbers”.
# Pam says, “I don’t know the numbers”.
# Sam says, “I don’t know the numbers”.
# Pam says, “I don’t know the numbers”.
# Sam says, “I don’t know the numbers”.
# Pam says, “I don’t know the numbers”.
# Sam says, “I don’t know the numbers”.
# Pam says, “I know the numbers”.
# Sam says, “I know the numbers”.
#
# What are the numbers?

pairs = list(set((j,i) for i in range(1,10) for j in range(1,i+1)))
print(sorted(pairs))
print()

for _ in range(4):
    p = [a*b for a,b in pairs]
    print(p)
    for i,(a,b) in enumerate(pairs):
        if p.count(p[i]) == 1:
            del pairs[i]
    print(pairs)

    s = [a+b for a,b in pairs]
    for i,(a,b) in enumerate(pairs):
        if s.count(s[i]) == 1:
            del pairs[i]
    print(pairs)
    print()
