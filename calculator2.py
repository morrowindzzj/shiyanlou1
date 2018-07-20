#!/usr/bin/env python3
import sys
try:
    sd=int(sys.argv[1])-3500
    sl=0
    sk=0
    if sd<1500 and sd>=0:
        sl=0.03
    elif sd<4500:
        sl=0.1
        sk=105
    elif sd<9000:
        sl=0.2
        sk=555
    elif sd<35000:
        sl=0.25
        sk=1005 
    elif sd<55000:
        sl=0.3
        sk=2755 
    elif sd<80000:
        sl=0.35
        sk=5505 
    elif sd>=80000:
        sl=0.45
        sk=13505 
    else:
        raise ValueError()
    result=sd*sl-sk
    print(format(result,".2f"))
except:
    print("Parameter Error")
