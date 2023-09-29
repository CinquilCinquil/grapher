from PIL import Image
import math
import os
import random as rnd

# --- initial variables ---
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [BLACK, RED, GREEN, BLUE]

v = 1 #version of the data to read 
img = Image.open("canvas.png")
w, h = img.size

file = open(f"data{v}.txt")
data = file.read()
file.close()

# --- functions ---
def sign(v):
	if v < 0:
		return -1
	if v > 0:
		return 1
	return 0

def inBounds(pos):
	return (0 <= pos[0] < w and 0 <= pos[1] < h)

def drawPoint(pos, color):
	if (inBounds(pos)):
		img.putpixel(pos, color)
	
def drawCircle(pos, r, color):
	pi2 = 2*math.pi
	p = round(r*pi2)
	
	for i in range(p): # looping around the perimeter of the circle
		x = round(pos[0] + r*math.cos((pi2)*i/p))
		y = round(pos[1] + r*math.sin((pi2)*i/p))
		
		if (inBounds((x, y))):
			img.putpixel((x, y), color)
	
def drawLine(pos, color):

	dx = pos[2] - pos[0] # x1 - x0
	dy = pos[3] - pos[1] # y1 - y0
	
	dz = max(abs(dx), abs(dy))
	dw = min(abs(dx), abs(dy))
	
	s = (dz == abs(dx)) # variable for whether dx > dy or dy > dx
	dxy = [sign(dx), sign(dy)] # in wich direction the point will be drawn towards
							   # ex: [0, -1] means the point wont move in x and will go up in y
	
	ratioWZ = dw/dz if dz != 0 else 0 # ratio between the smallest and the greatest coordinate distance
	
	xy = pos[0:2] # the coordinates of the point that is going to be drawn
	r = 0
	
	for i in range(dz):		
		if (inBounds(xy)): # just in case a point happens to be outisde of the image
			img.putpixel(xy, color)
			
		# calculating where the next point will be
			
		r += ratioWZ
		
		if r >= 1: # moving the coordinate with the smallest difference only after ratioWZ moves of the other coordinate
				   # ex: dx = 10 & dy = 5, then ratioWZ = 0.5 and only after x is increased twice y will be increased
			xy[s] += dxy[s]
			r -= 1 # preserves decimal values
		
		xy[not s] += dxy[not s] # moving the coordinate with the greatest difference
		

def readNTuple(i, data, n = 2):
	s = ""
	v = []
	k = 0
	# reading from data beginning in i
	for j in range(len(data)):
		if data[i + j + 1] != ',':
			s += data[i + j + 1]
		
		else: # reached the end of a number
			v.append(int(s))
			k += 1
			s = ""
		if k == n: # after k values have been read, return the ntuple
			return ["", v, j + 1]
			
def printProgress(i, l):
	# prints the progress once in a while (only useful for larger drawings)
	if rnd.randint(0, 100000) == 0:
		per = 100*(i/l)
		print(int(per*10)/10)

# --- reading data & drawing the image ---
s = ""
i = 0
l = len(data)
while True:
	printProgress(i, l)
	
	s += data[i]
	if s == "p": # point
		s, ntuple, j = readNTuple(i, data)
		i += j
		drawPoint(ntuple, BLACK)

	if s == "l": # line
		s, ntuple, j = readNTuple(i, data, 4)
		i += j
		drawLine(ntuple, colors[rnd.randint(0, 3)])
		
	if s == "c": # circle
		s, ntuple, j = readNTuple(i, data, 3)
		i += j
		drawCircle(ntuple[0:2], ntuple[2], BLACK)
	
	i += 1
	if i >= len(data): 
		print("\n --- Drawing Complete ---")
		break

# --- saving file ---
n = 0
while os.path.exists(f"output/save{n}.png"):
	n += 1

img.save(f"output/save{n}.png")
img.close()