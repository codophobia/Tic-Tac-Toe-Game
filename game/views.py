from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from random import randint
from django.views.decorators.csrf import csrf_exempt
xpos = -1
ypos = -1
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
	if request.method == 'POST':
		board = request.POST.getlist('board[]')
		a = [[0 for x in range(3)] for x in range(3)]
		for i in range(3):
			for j in range(3):
				a[i][j] = int(board[3*i+j])
		s = score(a,1,2,2)
		if(s == -10):
			return JsonResponse({'val':0,'res':1,'winner':'player'})
		elif(checkdraw(a) == 1):
			return JsonResponse({'val':0,'res':1,'winner':'draw'})
		tictac(a,1,2,1,0)
		a[xpos][ypos] = 1
		s = score(a,1,2,1)
		if(s == 10):
			return JsonResponse({'val':xpos*3+ypos,'res':1,'winner':'comp'})
		elif(checkdraw(a) == 1):
			return JsonResponse({'val':xpos*3+ypos,'res':1,'winner':'draw'})
		return JsonResponse({'val':xpos*3+ypos,'res':0,'winner':'none'})
	else:
		return JsonResponse({'val':"error"})

@csrf_exempt
def home(request): #displaying the home page
	context = {}
	return render(request,"game/home.html",context)

