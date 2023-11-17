##############################################################################################################################
# coding=utf-8
#
# bit_test.py -- test bitwise operations and see how python interprets and displays numbers,
#                especially if it does twos-complement
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-11-16"
__updated__ = "2023-11-16"


def dsp(a:int, nm:str="num"):
    print("{:>20}".format(nm) + f" = {hex(a)}; {a}; {bin(a)}")

# test ~ vs ^ for 32-bit
d = 0xffffffff
dsp(d, "d 32-bit")
nd = ~d
dsp(nd, "not-d")
tcnd = nd + 1
dsp(tcnd, "2c with not-d")
rtcnd = (~tcnd) + 1
dsp(rtcnd, "rev 2c with not-d")

xd = d ^ 0xffffffff
dsp(xd, "xor-d")
tcxd = xd + 1
dsp(tcxd, "2c with xor-d")
rtcxd = (tcxd ^ 0xffffffff) + 1
dsp(rtcxd, "rev 2c with xor-d")
print('')


# test ~ vs ^ for 16-bit
s = 0xfffe
dsp(s, "s 16-bit")
ns = ~s
dsp(ns, "not-s")
tcns = ns + 1
dsp(tcns, "2c with not-s")

xs = s ^ 0xffff
dsp(xs, "xor-s")
tcxs = xs + 1
dsp(tcxs, "2c with xor-s")
print('')


# test ~ vs ^ for negative number
n = -1
dsp(n, "n negative")
nn = ~n
dsp(nn, "not-n")
tcnn = nn + 1
dsp(tcnn, "2c with not-n")

xn = n ^ 0xffffffff
dsp(xn, "xor-n")
tcxn = xn + 1
dsp(tcxn, "2c with xor-n")
print('')


# test div and mod for negative numbers
m = -2
dsp(m, "m negative")
ndm = n // m
dsp(ndm, "-1 // -2")
nmm = n % m
dsp(nmm, "-1 % -2")
