###############################################################################################################################
# coding=utf-8
#
# problem_tavs.py
#
#  original code Copyright (c) 2021  Thomas Sattolo  <tsattolo@gmail.com>
#  modifications Copyright (c) 2021  Mark Sattolo  <epistemik@gmail.com>

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

def run_rounds(pairs:list, num_rounds:int):
    # the rounds
    for nr in range(num_rounds):
        print(F"Round #{nr+1}.")
        p = [a*b for a,b in pairs]
        print(F"products = {repr(p)}")
        save_p = list()
        # find unique products
        for i,pz in enumerate(pairs):
            if p.count(p[i]) == 1:
                save_p.append(i)
        print(F"product indices to remove = {repr(save_p)}")
        # print(pairs[0])
        # get rid of unique products
        for ix in reversed(save_p):
            # print(ix)
            del pairs[ix]
        print(F"now pairs = {repr(pairs)}")

        s = [a+b for a,b in pairs]
        print(F"sums = {repr(s)}")
        save_s = list()
        # find unique sums
        for i,sz in enumerate(pairs):
            if s.count(s[i]) == 1:
                save_s.append(i)
        print(F"sum indices to remove = {repr(save_s)}")
        # get rid of unique sums
        for iy in reversed(save_s):
            del pairs[iy]
        print(F"now pairs = {repr(pairs)}\n")


def main_two_digits_problem(num_rounds:int):
    pairs = set( (j, i) for i in range(1, 10) for j in range(1, i + 1) )
    pairs = sorted( list(pairs) )
    print(F"initial pairs = {repr(pairs)}")
    print(F"number of pairs = {len(pairs)}\n")

    run_rounds(pairs, num_rounds)

    # unique product left gives the numbers
    print("Finished all rounds.")
    p1 = [a * b for a, b in pairs]
    print(F"remaining products = {repr(p1)}")
    for i,r in enumerate(pairs):
        if p1.count(p1[i]) == 1:
            print(F"unique remaining product = {p1[i]}\nnumbers are {repr(pairs[i])}")


if __name__ == '__main__':
    main_two_digits_problem(4)
    exit()
