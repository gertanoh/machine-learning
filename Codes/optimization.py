# Optimization problem
# find solution a flight issue




import time
import random
import math


people=[('Dago','BOS'),
		('Mayi','DAL'),
		('Ane','CAK'),
		('Salif','MIA'),
		('Ange','ORD'),
		('Henry','OMA')]

# We meetup in New York

destination='LGA'

# Load flights file

flights={}

for line in file('schedule.txt'):
	origin,dest,depart,arrive,price=line.strip().split(',')
	flights.setdefault((origin,dest),[])
	flights[(origin,dest)].append((depart,arrive,int(price)))

def getMinutes(t):
	x=time.strptime(t,'%H:%M')
	return x[3]*60+x[4]


def printSchedule(r):
	for d in range(len(r)/2):
		name=people[d][0]
		origin=people[d][1]
		out=flights[(origin,destination)][int(r[d])]
		ret=flights[(destination,origin)][int(r[d+1])]
		print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,out[0],out[1],out[2],	ret[0],ret[1],ret[2])
	
	
# Function that defines cost of a solution
# takes into account multiple parameters waiting times, price of flight,..

def scheduleCost(sol):
	totalPrice=0
	latestArrival=0
	earliestDep=24*60
	
	for d in range(len(sol)/2):
		# Get the inbound and outbound flight
		origin=people[d][1]
		outbound=flights[(origin,destination)][int(sol[d])]
		returnf=flights[(destination,origin)][int(sol[d+1])]
		
		# Total proce is the price
		totalPrice+=outbound[2]
		totalPrice+=returnf[2]
		
		# Track the latest arrival and earliest departure
		if latestArrival < getMinutes(outbound[1]): 
			latestArrival=getMinutes(outbound[1])
		if earliestDep > getMinutes(returnf[0]): 
			earliestDep=getMinutes(returnf[0])
	
	# Waiting time for the latest person to arrive for every person
	# They also must arrive at the same time and wait for the return flight
	totalWait=0
	for d in range(len(sol)/2):
		origin=people[d][1]
		outbound=flights[(origin,destination)][int(sol[d])]
		returnf=flights[(destination,origin)][int(sol[d+1])]
		totalWait+=latestArrival-getMinutes(outbound[1])
		totalWait+=getMinutes(returnf[0])-earliestDep
	
	# Extra car rental day?
	if latestArrival > earliestDep: totalPrice+=50
	
	return totalPrice+totalWait
	

# Looking for optimization functions

# random search

def randomOptimize(domain, costF):
	best=999999999
	bestR=None
	for i in range(1000):
		# Create a random solution
		r=[random.randint(domain[i][0],domain[i][1]) 
			for i in range(len(domain))]
		# Get the cost
		cost=costF(r)
		
		# Compare it
		if cost<best:
			best=cost
			bestR=r
	return bestR


def hillClimb(domain,costF):
	# Create a random solution
	sol=[random.randint(domain[i][0],domain[i][1]) 
			for i in range(len(domain))]
	# Main Loop
	while 1:
		# Create list of neighboring solutions
		neighbors=[]
		for j in range(len(domain)):
			# One away in each direction
			if sol[j] > domain[j][0]:
				neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
			if sol[j] < domain[j][1]:
				neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
		# See what best solution among the neighbors is
		current=costF(sol)
		best=current
		for j in range(len(neighbors)):
			cost=costF(neighbors[j])
			if cost < best:
				best=cost
				sol=neighbors[j]
			# if no more improvement we have reached the top
		if best == current:
			break
	
	return sol



# Formula p = e ((-highcost-lowcost)/Temperature)
def annealingOptimize(domain,costF,T=10000.0,cool=0.95,step=3):
	vec=[float(random.randint(domain[i][0],domain[i][1])) for i in range(len(domain))]
	
	while T > 0.1:
		# Choose on of the indices
		i=random.randint(0,len(domain)-1)
		
		# Choose a direction to change it
		dir=random.randint(-step,step)
		
		# Create a new list with one of the values changed
		vecb=list(vec)
		vecb[i]+=dir
		if vecb[i] < domain[i][0]: vecb[i]=domain[i][0]
		elif vecb[i] > domain[i][1]: vecb[i]=domain[i][1]
		
		# Calculate the current cost and the new cost
		ea=costF(vec)
		eb=costF(vecb)
		p=pow(math.e,(-eb-ea)/T)
		
		# Is it better or does random is lower than the probability
		if(eb < ea or random.random() < p):
			vec=vecb
			
		# Decrease the Temperature
		T=T*cool
	
	return vec



def geneticOptimize(domain,costF,popSize=50,step=1,mutProd=0.2,elite=0.2,maxiter=100):
	# Mutation Operation
	def mutate(vec):
		i=random.randint(0,len(domain)-1)
		if random.random() < 0.5 and vec[i] > domain[i][0]:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		elif vec[i] < domain[i][1]:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		else:
			return vec[0:i]+[vec[i]-step]+vec[i+1:]
		
	# Crossover Operation
	def crossover(r1,r2):
		i=random.randint(1,len(domain)-2)
		return r1[0:i]+r2[i:]
	
	# Build the initial population
	pop=[]
	for i in range(popSize):
		vec=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
		pop.append(vec)
		
	# How many good solutions from each generation
	topElite=int(elite*popSize)
	
	# Main Loop
	for i in range(maxiter):
		scores=[(costF(v),v) for v in pop]
		scores.sort()
		ranked=[v for (s,v) in scores]
		
		# Start with pure solutions
		pop=ranked[0:topElite]
		
		# Add mutated and bred forms of the winners
		while len(pop) < popSize:
			if random.random() < mutProd:
				# Mutation
				c=random.randint(0,topElite)
				pop.append(mutate(ranked[c]))
			else:
				# Crossover
				c1=random.randint(0,topElite)
				c2=random.randint(0,topElite)
				pop.append(crossover(ranked[c1],ranked[c2]))
		
		# Print current best scores
		print scores[0][0]
		
	
	return scores[0][1]