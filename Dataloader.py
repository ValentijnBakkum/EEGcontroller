import numpy as np
import pandas as pd
import multiprocessing as mp

class DataReader():
    def __init__(self,dataset = "C:\\Users\\Gebruiker\\Desktop\\Bap\\Data\\A01T.npz"):
        self.fs = 250
        self.data = np.load(dataset)
        self.rawdata = self.data["s"]
        self.events = self.data["etyp"]
        self.pos = self.data["epos"]
        self.time = self.data["edur"]
    def load_data(self):
        events = [769,770,771,772]
        samplelist = []
        idlist = []
        for _ in events:
            a, b = np.where(self.data["etyp"] == _)
            print(_)
            #print(self.pos)
            for x in a:
                timestamp = self.pos[x].astype(int).item()
                #print(timestamp)
                i = 0
                for i in range(10):
                    #print(i)
                    begin1 = timestamp + (i * self.fs) + (4 * self.fs)
                    end1 = timestamp + (i * self.fs) + (5 * self.fs)
                    g = self.data["s"][begin1:end1]
                    g = np.delete(g,(0,7,9,11,13,19,22,23,24),1)
                    #print(g.shape)
                    if g.shape[0] == 250:
                        samplelist.append(g)
                        idlist.append(_ - 769)
                    else: 
                        print("issue")
                    i = i + 0.1
        return samplelist, idlist




        