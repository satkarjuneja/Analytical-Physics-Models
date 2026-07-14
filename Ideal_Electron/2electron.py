import numpy as np
import matplotlib.pyplot as plt
import random

location1_data = [0]
step_data1 = [0]
position1 = 0
location2_data = [0]
step_data2 = [0]
position2 = 0
Num = 1000
plt.ion()
plt.figure()
plt.title("Drunkard")
plt.xlabel("Steps")
plt.ylabel("Location")
plt.grid(True)
for i in range(0, 1000):
    step1 = random.choice([1, -1])
    step2 = random.choice([1, -1])
    position1 += step1
    position2 += step2
    step_data1.append(i)
    location1_data.append(position1)
    step_data2.append(i)
    location2_data.append(position2)
    plt.clf
    plt.plot(step_data1, location1_data, color="black", linestyle="-", marker="o")
    plt.plot(step_data2, location2_data, color="red", linestyle="-", marker="o")

    plt.pause(0.05)
plt.ioff()
plt.show()
