import sys
import os
import isword

def words(l):
    state=False
    w=0
    for c in l:
        if state!=isword._(ord(c)):
            state=not(state)
            if state:
                w=w+1
    return w

class LS:

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self, path="."):
        l = os.listdir(path)
        l.sort()
        for f in l:
            st = os.stat("%s/%s" % (path, f))
            if st[0] & 0x4000:  # stat.S_IFDIR
                print("   <dir> %s" % f)
            else:
                print("% 8d %s" % (st[6], f))

class PWD:

    def __repr__(self):
        return os.getcwd()

    def __call__(self):
        return self.__repr__()

class CLEAR:
    def __repr__(self):
        return "\x1b[2J\x1b[H"

    def __call__(self):
        return self.__repr__()


pwd = PWD()
ls = LS()
clear = CLEAR()

cd = os.chdir
mkdir = os.mkdir
mv = os.rename
rm = os.remove
rmdir = os.rmdir

def head(f, n=10):
    with open(f) as f:
        for i in range(n):
            l = f.readline()
            if not l: break
            sys.stdout.write(l)

def tail(f, n=10):
    with open(f) as f:
        if n<=0: return
        a = [ "" for i in range(n) ]
        i = 0
        while True:
            l = f.readline()
            if not l: break
            a[i % n] = l
            i += 1
        if i>0 and i<n:
            for j in range(i+1):
                sys.stdout.write(a[j])
        else:
            for j in range(n):
                sys.stdout.write(a[(i%n)-n+j])

def wc(fn):
    with open(fn) as f:
        c=r=w=0
        while True:
            l = f.readline()
            if not l: break
            r=r+1
            c=c+len(bytes(l,'utf-8'))
            w=w+words(l)
    print(r,w,c,fn)

def cat(f):
    head(f, 1 << 30)

def newfile(path):
    print("Type file contents line by line, finish with EOF (Ctrl+D).")
    with open(path, "w") as f:
        while 1:
            try:
                l = input()
            except EOFError:
                break
            f.write(l)
            f.write("\n")

class Man():

    def __repr__(self):
        return("""
upysh is intended to be imported using:
from upysh import *

To see this help text again, type "man".

upysh commands:
pwd, cd("new_dir"), ls, ls(...), head(...), tail(...), wc(...), cat(...)
newfile(...), mv("old", "new"), rm(...), mkdir(...), rmdir(...),
clear
""")

man = Man()

print(man)
