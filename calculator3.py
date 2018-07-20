mport sys
try:
    for arg in sys.argv[1:]:
        str_temp=arg.split(':')
	#calculate salary after tax  
        sd=int(str_temp[1])*(1-0.165)-3500  #salary after insurance and base
        sl=0 
        sk=0
        if sd<=0:
            sl=0
        elif sd<1500:
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
        tax=sd*sl-sk
        result=int(str_temp[1])*(1-0.165)-tax
        print(str_temp[0]+':'+format(result,".2f"))
except ValueError:
    print("Parameter Error")

