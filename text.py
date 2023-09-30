import math
import random as rnd

v = 2 # version of the data to write
file = open(f"data{v}.txt", 'w')

def writePoint(x, y):
	file.write(f"p{x},{y},")
	
def writeLine(x1, y1, x2, y2):
	file.write(f"l{x1},{y1},{x2},{y2},")

def writeCircle(x, y, r):
	file.write(f"c{x},{y},{r},")

def writePolinomial(coeffs, interval, offset, scale):
	coeffsStr = ""
	for c in coeffs:
		coeffsStr += str(c) + ","
	
	file.write(
		f"f{len(coeffs)}"
		+ ",%s,%s,%s,%s" % (tuple(interval + offset))
		+ f",{str(scale).replace(',','.')}," 
		+ coeffsStr
		)

def writeEsquizoide():
	x1 = rnd.randint(0, 2048)
	y1 = rnd.randint(0, 2048)
	x2 = rnd.randint(0, 2048)
	y2 = rnd.randint(0, 2048)
	for i in range(30):
		writeLine(x1, y1, x2, y2)
		writeCircle(x1, y1, 8)
		x1 = x2
		y1 = y2
		x2 = rnd.randint(0, 2048)
		y2 = rnd.randint(0, 2048)

def writeTree(x, y, n, r):

	writeCircle(x, y, 5)
	writeLine(x,y, int(x - 512*r), y + 60)
	writeLine(x,y, int(x + 512*r), y + 60)

	if n <= 0:
		return

	writeTree(int(x - 512*r), y + 60, int(n/2), math.pow(r*0.75, 1.2))
	writeTree(int(x + 512*r), y + 60, int(n/3), math.pow(r*0.75, 1.2))

#writeTree(1024, 60, 64, 0.75)
writePolinomial([0, 1, -1, -2, 1], [0, 512], [1024, 1024], 0.005)

file.close()