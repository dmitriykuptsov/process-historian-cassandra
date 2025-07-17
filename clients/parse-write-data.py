from sys import argv

f=open(argv[1])
lines = f.readlines()

s = []
e = []
t = [] 

for l in lines:
	if l.strip() == "":
		continue
	p = l.strip().split(" ")
	s.append(float(p[1]))
	e.append(float(p[2]))
	t.append(float(p[3]))

min = 10000000000000000000000000
max = 0

for i in range(0, len(s)):
	if s[i] < min:
		min = s[i]
	if s[i] > max:
		max = s[i]
#print("Bin size")
#print(int((max - min) / 20))
bin = int((max - min) / 20)

ss = min
while ss <= max:
	accum = 0
	for i in range(0, len(s)):
		if ss < s[i] and ss + bin >= s[i]:
			diff = e[i] - s[i]
			if e[i] > ss + bin:
				diff2 = ss + bin - s[i]
			else:
				diff2 = e[i] - s[i]

			tp = t[i] * diff2
		elif ss < e[i] and ss + bin >= e[i]:
			diff = e[i] - s[i]
			diff2 = e[i] - ss
			tp = t[i] * diff2
		elif ss > s[i] and ss + bin <= e[i]:
			diff2 = bin
			tp = t[i] * bin
		accum += tp
	print(accum / bin)
	ss += bin
			
