import rpyc
conn = rpyc.classic.connect("localhost")

conn.execute('import math') 
x = conn.eval('2*math.pi')
print(x)




