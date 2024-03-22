#!/usr/bin/env python 3.7

__author__      = "Emerson Andrade"
__version__   = "1.0.0"
__date__   = "2024"

import numpy as np
import matplotlib.pyplot as plt
import csv

class Fish():
    def __init__(self, frames, x_coords, y_coords):
        self.t = frames
        self.x = x_coords
        self.y = y_coords

class GroundTruth():

    def __init__(self):
        
        self.fish_list = self.read_csv('ground_truth.csv')

        self.fish1 = Fish(self.fish_list[:,0], self.fish_list[:,1], self.fish_list[:,2])
        self.fish2 = Fish(self.fish_list[:,0], self.fish_list[:,3], self.fish_list[:,4])
        self.fish3 = Fish(self.fish_list[:,0], self.fish_list[:,5], self.fish_list[:,6])
        self.fish4 = Fish(self.fish_list[:,0], self.fish_list[:,7], self.fish_list[:,8])
        self.fish5 = Fish(self.fish_list[:,0], self.fish_list[:,9], self.fish_list[:,10])
    
    def read_csv(self, filename):
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            result = np.asarray(list(reader)[0:])
            result = result.astype('float64')

        return result

    def plot_xy(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.plot(self.fish1.x, self.fish1.y, label='fish 1')
        ax.plot(self.fish2.x, self.fish2.y, label='fish 2')
        ax.plot(self.fish3.x, self.fish3.y, label='fish 3')
        ax.plot(self.fish4.x, self.fish4.y, label='fish 4')
        ax.plot(self.fish5.x, self.fish5.y, label='fish 5')

        ax.set_aspect('equal')
        ax.grid()
        plt.legend()
        plt.show()
        plt.close()
