from sys import argv

f=open(argv[1])
lines = f.readlines()

d = []
t = [] 

for l in lines:
	p = l.strip().split(" ")
	print(float(p[1])/float(p[0]))

