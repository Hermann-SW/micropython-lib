import sys
import os
import re

import io

class _DUP(io.IOBase):

    def __init__(self, s):
        self.s = s

    def write(self, data):
        self.s += data
        return len(data)

    def readinto(self, data):
        return 0

class _Pipe(object):
    def __init__(self, val):
        if type(val) == Man:
            self.val = io.StringIO(val.__repr__())
        elif type(val) == type(lambda: x):
            s = bytearray()
            prev = os.dupterm(_DUP(s))
            val()
            os.dupterm(prev)
            self.val = io.StringIO(s)
        else:
            self.val = open(val)

    def __or__(self, fn):
        if fn == done:
            if type(self.val) == io.TextIOWrapper:
                print("".join(self.val.readlines()),end="")
                return
            elif type(self.val) == io.StringIO:
                print(self.val.getvalue(),end="")
                return
            else:
                return self.val
        elif type(fn) == type( (0,) ):
            if fn[0] == done:
                return
            self.val = fn[0]( * (self.val,) + fn[1:] )
        else:
            self.val = fn(self.val)
        return self

def pipe(arg):
    return _Pipe(arg)

def done(val, out=True):
    return


def _open(f):
    if type(f) == io.TextIOWrapper or type(f) == io.StringIO:
        return f 
    else:
        return open(f)


def grep(f, r, o=""):     # "i" "v"
    out = sys.stdout if type(f) == str else io.StringIO('')

    i="i" in o
    v="v" in o

    with _open(f) as f:
        r=".*"+r
        if i:
            r=r.lower()
        while True:
            l = f.readline()[:-1]
            if not l: break
            if bool(re.match(r, l.lower() if i else l)) != v:
                out.write(l+'\n')

    if out != sys.stdout:
        out.seek(0,0)
        return out


def od(f, o=""):    # "c"
    out = sys.stdout if type(f) == str else io.StringIO('')

    c="c" in o
    with _open(f) as f:
        a = 0
        while True:
            l = f.read(0x10)
            out.write("{0:0{1}x}".format(a,6))
            if not l: out.write('\n'); break
            a=a+len(l)
            if c:
                for b in l:
                    B=ord(b)
                    if 0 < B < 7 or 13 < B < 32 or B > 126:
                        out.write(" ")
                        out.write("{0:0{1}o}".format(B,3))
                    elif B > 31:
                        out.write("   ")
                        out.write(b)
                    else:
                        out.write("  \\"+"0......abtnvfr"[B])
                out.write("\n      ")
            for b in l:
                out.write("  ")
                out.write("{0:0{1}x}".format(ord(b),2))
            out.write("\n")

    if out != sys.stdout:
        out.seek(0,0)
        return out


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
    out = sys.stdout if type(f) == str else io.StringIO('')

    with _open(f) as f:
        for i in range(n):
            l = f.readline()
            if not l: break
            out.write(l)

    if out != sys.stdout:
        out.seek(0,0)
        return out

def cp(s, t):
    with _open(s) as s:
        with open(t, "w") as t:
            while True:
                l = s.readline()
                if not l: break
                t.write(l)

def tee(s, t, m="w"):       # "a"
    with open(t, m) as t:
        while True:
            l = s.readline()
            if not l: break
            t.write(l)

    s.seek(0,0)
    return s

def tail(f, n=10):
    out = sys.stdout if type(f) == str else io.StringIO('')

    with _open(f) as f:
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
                out.write(a[j])
        else:
            for j in range(n):
                out.write(a[(i%n)-n+j])

    if out != sys.stdout:
        out.seek(0,0)
        return out

wloaded = False

def wc(fn):  # ,dummy=""):
    global wloaded
    if not(wloaded):
        print("import words")
        import words
        wloaded = words

    out = sys.stdout if type(fn) == str else io.StringIO('')

    c=r=w=0
    with _open(fn) as f:
        while True:
            l = f.readline()
            if not l: break
            r=r+1
            c=c+len(bytes(l,'utf-8'))
            w=w+wloaded.words(l)

    f = fn if type(fn) == str else "(pipe)"  
    out.write("{0:d} {1:d} {2:d} {3:s}\n".format(r,w,c,f))

    if out != sys.stdout:
        out.seek(0,0)
        return out

def cat(f):
    return head(f, 1 << 30)

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
upysh_ is intended to be imported using:
[import words  (on systems with very small RAM)]
from upysh_ import *

To see this help text again, type "man".

Most upysh_ commands allow for "producer|consumer" pipeing:
  >>> pipe("tst.txt") | (head,3) | (tee,"3.txt") | (grep,'t','i') | done
  first
  ThirD
  >>> pipe(lambda: micropython.qstr_info(1)) | (head,2) | done
  qstr pool: n_pool=1, n_qstr=69, n_str_data_bytes=525, n_total_bytes=2141
  Q(webrepl_cfg.py)
  >>>

producer only:  man, ls, ls()[, pipe(filename)]
         both:  head(), tail(), cat(), grep(), od(), tee()[, wc(), cp()]
consumer only:  [done]

upysh_ commands:
pwd, cd(new_dir), ls, ls(...), head(...), tail(...), wc(...), cat(...), clear
newfile(...), mv(old, new), cp(src, tgt), tee(src, tgt [, opt]), rm(...)
grep(file, regex [, opt]), od(file [, opt]), mkdir(...), rmdir(...)
""")

man = Man()

print(man)
