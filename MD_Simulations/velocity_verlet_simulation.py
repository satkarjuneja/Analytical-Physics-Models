import numpy as np
import matplotlib.pyplot as plt

sigma=1
epsilon=1

def leonard_jones(r):
    return 4*epsilon*(((sigma)/r)**12-((sigma)/r)**6)