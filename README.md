fork-mission-statement
======================
This fork is only intended to add new commands to [upysh/upysh.py](upysh/upysh.py), like tail(), wc(), cp(), grep() and od() already. Since "upysh" module is already present on ESP32, this module needs to be renamed on upload:
~~~~
$ ~/webrepl/webrepl_cli.py -p abcd upysh.py 192.168.4.1:upysh_.py
op:put, host:192.168.4.1, port:8266, passwd:abcd.
upysh.py -> upysh_.py
Remote WebREPL version: (1, 9, 4)
Sent 10105 of 10105 bytes
$ 
$ webrepl_client.py -p abcd 192.168.4.1
Password: 
WebREPL connected
>>> 
>>> 
MicroPython v1.9.4-272-g46091b8a on 2018-07-18; ESP module with ESP8266
Type "help()" for more information.
>>> gc.collect(); m0=gc.mem_free()
>>> from upysh_ import *

upysh is intended to be imported using:
from upysh import *

To see this help text again, type "man".

upysh commands:
pwd, cd("new_dir"), ls, ls(...), head(...), tail(...), wc(...), cat(...),
newfile(...), mv("old", "new"), cp("src", "tgt"), rm(...),
grep("opt", "regex", "file"), od("opt", "file"), mkdir(...), rmdir(...), clear

>>> gc.collect(); m1=gc.mem_free()
>>> print(m0, m1, m0-m1)
28656 22288 6368
>>> tail("tst.txt",3)
second().
ThirD
  Fourth()
>>> cp("boot.py", "x")
>>> grep('', '\)$', 'tst.txt')
  Fourth()
>>> grep('', 't', 'tst.txt')
first
  Fourth()
>>> grep('i', 't', 'tst.txt')
first
ThirD
  Fourth()
>>> grep('iv', 'T', 'tst.txt')
second().
>>> od('', 'tst.txt')
000000  66  69  72  73  74  0a  73  65  63  6f  6e  64  28  29  2e  0a
000010  54  68  69  72  44  0a  20  20  46  6f  75  72  74  68  28  29
000020  0a
000021
>>> od('c', '256.dat')
000000  \0 001 002 003 004 005 006  \a  \b  \t  \n  \v  \f  \r 016 017
        00  01  02  03  04  05  06  07  08  09  0a  0b  0c  0d  0e  0f
000010 020 021 022 023 024 025 026 027 030 031 032 033 034 035 036 037
        10  11  12  13  14  15  16  17  18  19  1a  1b  1c  1d  1e  1f
000020       !   "   #   $   %   &   '   (   )   *   +   ,   -   .   /
        20  21  22  23  24  25  26  27  28  29  2a  2b  2c  2d  2e  2f
000030   0   1   2   3   4   5   6   7   8   9   :   ;   <   =   >   ?
        30  31  32  33  34  35  36  37  38  39  3a  3b  3c  3d  3e  3f
000040   @   A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
        40  41  42  43  44  45  46  47  48  49  4a  4b  4c  4d  4e  4f
000050   P   Q   R   S   T   U   V   W   X   Y   Z   [   \   ]   ^   _
        50  51  52  53  54  55  56  57  58  59  5a  5b  5c  5d  5e  5f
000060   `   a   b   c   d   e   f   g   h   i   j   k   l   m   n   o
        60  61  62  63  64  65  66  67  68  69  6a  6b  6c  6d  6e  6f
000070   p   q   r   s   t   u   v   w   x   y   z   {   |   }   ~ 177
        70  71  72  73  74  75  76  77  78  79  7a  7b  7c  7d  7e  7f
000080 200 201 202 203 204 205 206 207 210 211 212 213 214 215 216 217
        80  81  82  83  84  85  86  87  88  89  8a  8b  8c  8d  8e  8f
000090 220 221 222 223 224 225 226 227 230 231 232 233 234 235 236 237
        90  91  92  93  94  95  96  97  98  99  9a  9b  9c  9d  9e  9f
0000a0 240 241 242 243 244 245 246 247 250 251 252 253 254 255 256 257
        a0  a1  a2  a3  a4  a5  a6  a7  a8  a9  aa  ab  ac  ad  ae  af
0000b0 260 261 262 263 264 265 266 267 270 271 272 273 274 275 276 277
        b0  b1  b2  b3  b4  b5  b6  b7  b8  b9  ba  bb  bc  bd  be  bf
0000c0 300 301 302 303 304 305 306 307 310 311 312 313 314 315 316 317
        c0  c1  c2  c3  c4  c5  c6  c7  c8  c9  ca  cb  cc  cd  ce  cf
0000d0 320 321 322 323 324 325 326 327 330 331 332 333 334 335 336 337
        d0  d1  d2  d3  d4  d5  d6  d7  d8  d9  da  db  dc  dd  de  df
0000e0 340 341 342 343 344 345 346 347 350 351 352 353 354 355 356 357
        e0  e1  e2  e3  e4  e5  e6  e7  e8  e9  ea  eb  ec  ed  ee  ef
0000f0 360 361 362 363 364 365 366 367 370 371 372 373 374 375 376 377
        f0  f1  f2  f3  f4  f5  f6  f7  f8  f9  fa  fb  fc  fd  fe  ff
000100
>>> wc('upysh_.py')
214 1391 10120 upysh_.py
>>> exit
### closed ###
$ 
$ wc upysh.py
  214  1391 10120 upysh.py
$ 
~~~~


micropython-lib
===============
micropython-lib is a project to develop a non-monolothic standard library
for "advanced" MicroPython fork (https://github.com/pfalcon/micropython).
Each module or package is available as a separate distribution package from
PyPI. Each module comes from one of the following sources (and thus each
module has its own licensing terms):

* written from scratch specifically for MicroPython
* ported from CPython
* ported from some other Python implementation, e.g. PyPy
* some modules actually aren't implemented yet and are dummy

Note that the main target of micropython-lib is a "Unix" port of the
aforementioned fork of MicroPython. Actual system requirements vary per
module. Majority of modules are compatible with the upstream MicroPython,
though some may require additional functionality/optimizations present in
the "advanced" fork. Modules not related to I/O may also work without
problems on bare-metal ports, not just on "Unix" port (e.g. pyboard).


Usage
-----
micropython-lib packages are published on PyPI (Python Package Index),
the standard Python community package repository: https://pypi.org/ .
On PyPI, you can search for MicroPython related packages and read
additional package information. By convention, all micropython-lib package
names are prefixed with "micropython-" (the reverse is not true - some
package starting with "micropython-" aren't part of micropython-lib and
were released by 3rd parties).

Browse available packages [via this
URL](https://pypi.org/search/?q=&o=&c=Programming+Language+%3A%3A+Python+%3A%3A+Implementation+%3A%3A+MicroPython).

To install packages from PyPI for usage on your local system, use the
`upip` tool, which is MicroPython's native package manager, similar to
`pip`, which is used to install packages for CPython. `upip` is bundled
with MicroPython "Unix" port (i.e. if you build "Unix" port, you
automatically have `upip` tool). Following examples assume that
`micropython` binary is available on your `PATH`:

~~~~
$ micropython -m upip install micropython-pystone
...
$ micropython
>>> import pystone
>>> pystone.main()
Pystone(1.2) time for 50000 passes = 0.534
This machine benchmarks at 93633 pystones/second
~~~~

Run `micropython -m upip --help` for more information about `upip`.


Development
-----------
To install modules during development, use `make install`. By default, all
available packages will be installed. To install a specific module, add the
`MOD=<module>` parameter to the end of the `make install` command.


Links
-----
If you would like to trace evolution of MicroPython packaging support,
you may find following links useful (note that they may contain outdated
information):

 * https://github.com/micropython/micropython/issues/405
 * http://forum.micropython.org/viewtopic.php?f=5&t=70

Guidelines for packaging MicroPython modules for PyPI:

 * https://github.com/micropython/micropython/issues/413
