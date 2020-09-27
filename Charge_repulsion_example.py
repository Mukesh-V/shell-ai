import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
from numpy import random

p = np.zeros([100,100])

for n in range(20):
    p[random.randint(100)][random.randint(100)] = 1

repul_cons = 50 #to be tweaked (repulsion coefficient)

q = np.copy(p)

fig,ax = plt.subplots()
particles = plt.imshow(p)


def update(num):
    global p
    global q
    global repul_cons

    turb_pos = []
    for i in range(100):
        for j in range(100):
            if p[i][j] == 1:
                turb_pos.append([i,j])

    for x,y in turb_pos:
        if x!=0 or x!=99 or x==0 or x==99:
            if p[x][y] == 1:
                total_x = 0
                total_y = 0
                for i,j in turb_pos:
                    if i!=x and j!=y:
                        temp = math.sqrt(((x-i)**2) + ((y-j)**2))
                        if temp < 25:  # here 25 is the threshold distance between two points above which the points do not repel each other
                            potential_energy = repul_cons / temp
                            add_on_x = ((x-i)/temp)*potential_energy
                            add_on_y = ((y-j)/temp)*potential_energy
                            total_x += add_on_x
                            total_y += add_on_y
                if total_x > 0 : total_x = 1
                if total_x < 0 : total_x = -1
                if total_y > 0 : total_y = 1
                if total_y < 0 : total_y = -1
                total_x = int(total_x)
                total_y = int(total_y)
                q[x][y] = 0
                if (x+total_x) < 0:
                    total_x = -x
                if (y+total_y) < 0:
                    total_y = -y
                if (x+total_x) > 99:
                    total_x = 99 - x
                if (y+total_y) > 99:
                    total_y = 99 - y
                q[x + total_x][y + total_y] = 1

    p = np.copy(q)
    particles.set_data(p)
    return particles

ani = FuncAnimation(fig,update,frames=1000000)
plt.show()

for i in range(100):
    for j in range(100):
        if p[i][j] == 1:
            print(i,j)