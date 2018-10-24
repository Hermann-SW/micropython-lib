#!/usr/bin/env python3

f = open("out")

def blk():
    i=0
    be=True
    bf=True
    for j in range(256):
        if f.readline().startswith("1"):
            i |= 1<<j
            be=False
        else:
            bf=False
    if be or bf:
        return bf
    else:
        return i

a = [blk() for p in range(0x00000, 0x30000, 256)]


import sys
def stat():
    e=f=b=0

    for i in range(0x300):
        if type(a[i])==type(True):
            if a[i]:
                f=f+1
            else:
                e=e+1
        else:
           b=b+1
    return (e, f, b)


print("# generated by ./gen_blk_wc.py")
sys.stdout.write("# sys.getsizeof(ISWORD)=")
print(sys.getsizeof(a))
sys.stdout.write("# empty/full/other blocks: ")
print(stat())
print("#")
print("""import sys

if sys.implementation.name=='micropython':
    import utime
    def ticks_ms():  return utime.ticks_ms()
else:
    import time
    def ticks_ms():  return 1000*time.time()
""")
sys.stdout.write("ISWORD=")
print(a)
print("""
def _(i):
    if i>=0x030000:
        if (i<0x0e0000):
            return False
        elif i>=0x0f0000:
            return (i%65536)<0xfffe
        else:
            return (i==0x0e0001) | (0x0e0020<=i<=0x0e007f) | (0x0e0100<=i<=0x0e01ef)
    else:
        b = i//256
        if type(ISWORD[b])==type(True):
            return ISWORD[b]
        else:
            return ISWORD[b] & (1<<(i%256)) != 0
""")

print("""
def isword(str):
    for c in str:
        if not(_(ord(c))):
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
        if _(i):
            c=c+1
    end = ticks_ms()
    return (c, end-start, (end-start)/len)
""")

print("""
def tstPlanes(fulltest=True):
    return tst_(0, 1+(0x10ffff if fulltest else 0x02ffff))

""")
