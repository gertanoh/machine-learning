import random
import math


# The dorms, each of which has two available spaces
dorms=['Zeus','Athena','Bacchus','Hercules','Pluto']


# People, along with their first and second choices
prefs=[('Henry', ('Bacchus', 'Hercules')),
('Steve', ('Zeus', 'Pluto')),
('Salif', ('Athena', 'Zeus')),
('Dago', ('Zeus', 'Pluto')),
('Georges', ('Athena', 'Bacchus')),
('Lucien', ('Hercules', 'Pluto')),
('Ola', ('Pluto', 'Athena')),
('Mayi', ('Bacchus', 'Hercules')),
('Ange', ('Bacchus', 'Hercules')),
('Ane', ('Hercules', 'Athena'))]



domain=[(0,(len(dorms)*2)-i-1) for i in range(0,len(dorms)*2)]

def printsolution(vec):
    slots = slotlist(len(dorms))
    for i in range(len(vec)):
        x = vec[i]
        print prefs[i][0], dorms[slots[x]]
        del slots[x]


def slotlist(l):
    slots = []
    for i in range(l): 
        slots += [i, i]
    return slots


# Best solution when making a cost function is so that the perfect solution has a cost of 0

# In our case the perfect solution is impossible, therefore we are trying to be close to 0
 
# cost function
# comparaison between the final assignment and the student will
# total cost increased by 1 if second choice, 3 if not 1 or 2 choice otherwise 0

def dormcost(vec):
    cost = 0
    slots = slotlist(len(dorms))
    print vec
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        if pref[0] == dorm: cost += 0
        elif pref[1] == dorm: cost += 1
        else: cost += 3
        del slots[x]

    return cost