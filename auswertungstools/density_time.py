#!/usr/bin/env python2.7
from scipy import *
from sys import argv
from operator import add

def updateDensity(z,sp,density):
	if(sp == "C"):
		density[0][index(z)] += 1
	else:
		density[1][index(z)] += 1

def index(z):
	return int(floor(z/binheight))

stepsize = int(argv[1])
datei = argv[2]
densities = []
density = array([])
height = 250
width = 100
binheight = 1
N = 0
steps = 0
state = "readnum"

dateistream = open(datei,"r")
for zeile in dateistream:
	if(state == "readnum"):
		N = int(zeile)
		if(steps == 0):
			density = [zeros(height/binheight),zeros(height/binheight)]
		state = "skipline"
	elif(state == "skipline"):
		state = "readpos"
	elif(state == "readpos"):
		pos = zeile.split("\t")
		sp = pos[0]
		z = float(pos[2])
		updateDensity(z,sp,density)
		N -= 1
		if N == 0:
			steps += 1
			state = "readnum"
			if(steps == stepsize):
				densities.append(density)
				print(str(len(densities))+" profile done.")
				steps = 0
	if(state == "end"):
		break;

if(steps != stepsize):
	density2 = densities[len(densities)-1]
	density2[0] = array(map(add,density2[0],density[0]))
	density2[1] = array(map(add,density2[1],density[1]))
	densities[len(densities)-1] = density2
	
for i,dens in enumerate(densities[:len(densities)-1]):
	dens[0] = array([float(elem)/float(binheight*width*stepsize) for elem in dens[0]])
	dens[1] = array([float(elem)/float(binheight*width*stepsize) for elem in dens[1]])
	densities[i]=dens

dens = densities[len(densities)-1]
dens[0] = array([float(elem)/float(binheight*width*(stepsize+steps)) for elem in dens[0]])
dens[1] = array([float(elem)/float(binheight*width*(stepsize+steps)) for elem in dens[1]])
densities[len(densities)-1] = dens

for i,dens in enumerate(densities):
	savetxt("sp0-{index}.dat".format(index=i),dens[0])
	savetxt("sp1-{index}.dat".format(index=i),dens[1])
