#!/usr/bin/env python3

f = open("out")

def blk(d, n, j):
    i=0
    while n>0:
        n = n - 1
        i=i+1 
        if not(f.readline().startswith(d)):
            j=j+i
            return (None,j)[1:] if j==65535 else (None,j)[1:] + blk(chr(97-ord(d)), n, j)

import array

p0 = array.array('H', blk(f.readline()[0], 65536, -1))
p1 = array.array('H', blk('1', 65536, -1))


import sys


print("# generated by ./gen_blk_wc.py")
sys.stdout.write("# sys.getsizeof(_0)=")
print(sys.getsizeof(p0))
sys.stdout.write("# sys.getsizeof(_1)=")
print(sys.getsizeof(p1))
print("#")
print("""import sys, array

if sys.implementation.name=='micropython':
    import utime
    def ticks_ms():  return utime.ticks_ms()
else:
    import time
    def ticks_ms():  return 1000*time.time()
""")
sys.stdout.write("_0=array.")
print(p0)
sys.stdout.write("_1=array.")
print(p1)
print("""
def _s(arr, i):
    lft = 0
    rgt = len(arr)-1
    while lft+1 < rgt:
        mid = (lft + rgt) // 2
        if i <= arr[mid]:
            rgt = mid
        else:
            lft = mid
    return (lft % 2) if i<=arr[lft] else (rgt % 2)


def _w(i):
    if i>=0x030000:
        if (i<0x0e0000):
            return False
        elif i>=0x0f0000:
            return (i%65536)<0xfffe
        else:
            return (i==0x0e0001) | (0x0e0020<=i<=0x0e007f) | (0x0e0100<=i<=0x0e01ef)
    elif i>=0x020000:
        if i>=0x02f800:
            return i<0x02fa1e
        else:
            return i<0x02a6d7
    elif i>=0x010000:
        return 1 - _s(_1, i%65536) 
    else:
        return _s(_0, i) 
""")

print("""
def isword(str):
    for c in str:
        if not(_w(ord(c))):
            return False

    return True
""")

print("""
def tst(strt,len):
    start = ticks_ms()
    c=0
    for i in range(strt,strt+len,1):
        if isword(chr(i)):
            c=c+1
    return c
    end = ticks_ms()
    return (c, end-start, (end-start)/len)
""")

print("""
def tst_(strt,len):
    start = ticks_ms()
    c=0
    for i in range(strt,strt+len,1):
        if _w(i):
            c=c+1
    end = ticks_ms()
    return (c, end-start, (end-start)/len)
""")

print("""
def tstPlanes(fulltest=True):
    return tst_(0, 1+(0x10ffff if fulltest else 0x02ffff))

""")
