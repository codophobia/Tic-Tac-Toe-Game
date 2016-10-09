from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from random import randint
from django.views.decorators.csrf import csrf_exempt
xpos = -1
ypos = -1
start = 0
a = [[0 for x in range(3)] for x in range(3)]
temp = {}
temp[0,0] = 1
temp[0,1] = 2
temp[0,2] = 3
temp[1,0] = 4
temp[1,1] = 5
temp[1,2] = 6
temp[2,0] = 7
temp[2,1] = 8
temp[2,2] = 9
def score(b,comp,p,turn): #checks if a player has won or not
	flag = 0
	for i in range(3):
		count = 0
		for j in range(3):
			if(b[i][j] == turn):
				count = count+1
		if(count == 3):
			flag = 1

	for i in range(3):
		count = 0
		for j in range(3):
			if(b[j][i] == turn):
				count = count+1
		if(count == 3):
			flag = 1

	if(b[0][0] == turn and b[1][1] == turn and b[2][2] == turn):
		flag = 1
	if(b[0][2] == turn and b[1][1] == turn and b[2][0] == turn):
		flag = 1
	if(flag == 1):
		if(turn == comp):
			return 10
		else:
			return -10
	return 0
def checkdraw(b): #checks for draw
	for i in range(3):
		for j in range(3):
			if(b[i][j] == 0):
				return 0
	return 1

def tictac(b,comp,p,turn,g): #min-max algorithm for tic-tac toe
	curr = comp
	global xpos
	global ypos
	mx = -1000
	mn = 1000
	if(turn == comp):
		curr = p
	check = score(b,comp,p,curr)
	if(check == 10):
		return 10 - g
	elif(check == -10):
		return -10 + g
	elif(checkdraw(b)):
		return 0

	if(turn == comp):
		for i in range(3):
			for j in range(3):
				if(b[i][j] == 0):
					b[i][j] = comp
					x = tictac(b,comp,p,p,g+1)
					#print x
					if(x > mx):
						mx = x
						if(g == 0):
							xpos = i
							ypos = j
							#print g,xpos,ypos
					b[i][j] = 0
		return mx
	elif(turn == p):
		for i in range(3):
			for j in range(3):
				if(b[i][j] == 0):
					b[i][j] = p
					y = tictac(b,comp,p,comp,g+1)
					if(y < mn):
						mn = y
						if(g == 0):
							xpos = i
							ypos = j
					b[i][j] = 0
		return mn
@csrf_exempt
def index(request): #when the user submits his choice
	global a
	if request.method == 'POST':
		pos = int(request.POST['pos'])
		x = -1
		y = -1
		if(pos == 1):
			x = 0
			y = 0
		elif(pos == 2):
			x = 0
			y = 1
		elif(pos == 3):
			x = 0
			y = 2
		elif(pos == 4):
			x = 1
			y = 0
		elif(pos == 5):
			x = 1
			y = 1
		elif(pos == 6):
			x = 1
			y = 2
		elif(pos == 7):
			x = 2
			y = 0
		elif(pos == 8):
			x = 2
			y = 1
		elif(pos == 9):
			x = 2
			y = 2
		a[x][y] = 2
		c = a
		s = score(c,1,2,2)
		if(s == -10):
			return JsonResponse({'val':0,'res':1,'winner':'player'})
		elif(checkdraw(c) == 1):
			return JsonResponse({'val':0,'res':1,'winner':'draw'})
		tictac(c,1,2,1,0)
		a[xpos][ypos] = 1
		s = score(a,1,2,1)
		if(s == 10):
			return JsonResponse({'val':temp[xpos,ypos],'res':1,'winner':'comp'})
		elif(checkdraw(a) == 1):
			return JsonResponse({'val':temp[xpos,ypos],'res':1,'winner':'draw'})
		return JsonResponse({'val':temp[xpos,ypos],'res':0,'winner':'none'})
	else:
		return JsonResponse({'val':"error"})

@csrf_exempt
def home(request): #displaying the home page
	context = {}
	return render(request,"game/home.html",context)

@csrf_exempt
def chance(request): #selecting who plays first
	global start
	if request.method == 'POST':
		start = int(request.POST['chance'])
		for i in range(3):
				for j in range(3):
					a[i][j] = 0
		if(start == 1):
			x = randint(0,2)
			y = randint(0,2)
			a[x][y] = 1
			return JsonResponse({'val':temp[x,y]})
		else:
			return JsonResponse({'val':"start"})
