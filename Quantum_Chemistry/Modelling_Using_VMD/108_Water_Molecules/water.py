import numpy as np
import matplotlib.pyplot as plt
import random


def R(x1,y1,z1,x2,y2,z2):
    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5


x_data=[]
y_data=[]
z_data=[]
h1x=[]
h1y=[]
h1z=[]
h2x=[]
h2y=[]
h2z=[]
num=108
size=50
radius=1.7
length=0
while(length<108):
    x=random.uniform(-size,size)
    y=random.uniform(-size,size)
    z=random.uniform(-size,size)
    flag=0
    for i in range(0,length):
        if(R(x,y,z,x_data[i],y_data[i],z_data[i])<3):
            flag=1
        else:
            continue
    
    if (flag==0):
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)
        h1x.append(x+0.96)
        h1y.append(y)
        h1z.append(z)
        h2x.append(x-0.24)
        h2y.append(y+0.92)
        h2z.append(z)
        length+=1

for i in range(0,108):
    th=random.uniform(-1,1)
    theta=th*(np.pi)
    t=h1x[i]
    tt=h2x[i]
    # h1x[i]=x_data[i]+(x_data[i]-h1x[i])*(np.cos(theta))-(y_data[i]-h1y[i])*(np.sin(theta))
    # h1y[i]=y_data[i]+(x_data[i]-t)*(np.cos(theta))-(y_data[i]-h1y[i])*(np.sin(theta))
    # h2x[i]=x_data[i]+(x_data[i]-h2x[i])*(np.cos(theta))-(y_data[i]-h2y[i])*(np.sin(theta))
    # h2y[i]=y_data[i]+(x_data[i]-tt)*(np.cos(theta))-(y_data[i]-h2y[i])*(np.sin(theta))
    dx1 = h1x[i] - x_data[i]
    dy1 = h1y[i] - y_data[i]
    h1x[i] = x_data[i] + dx1*np.cos(theta) - dy1*np.sin(theta)
    h1y[i] = y_data[i] + dx1*np.sin(theta) + dy1*np.cos(theta)


    dx2 = h2x[i] - x_data[i]
    dy2 = h2y[i] - y_data[i]
    h2x[i] = x_data[i] + dx2*np.cos(theta) - dy2*np.sin(theta)
    h2y[i] = y_data[i] + dx2*np.sin(theta) + dy2*np.cos(theta)

    a=random.uniform(-1,1)
    b=random.uniform(-1,1)
    c=random.uniform(-1,1)
    x_data[i]+=a
    y_data[i]+=b
    z_data[i]+=c
    h1x[i]+=a
    h1y[i]+=b
    h1z[i]+=c
    h2x[i]+=a
    h2y[i]+=b
    h2z[i]+=c
for i in range(0,num):
    print("o ",x_data[i],y_data[i],z_data[i])
    print("h ",h1x[i],h1y[i],h1z[i])
    print("h ",h2x[i],h2y[i],h2z[i])



