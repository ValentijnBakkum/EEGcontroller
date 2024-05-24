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
                print(timestamp)
                h = 0
                for i in range(10):
                    #print(h)
                    begin1 = timestamp + (h * self.fs) #+ (1 * self.fs)
                    
                    end1 = timestamp + (h * self.fs) + (256)
                    #print(begin1,end1)
                    g = self.data["s"][int(begin1):int(end1)]
                    g = np.delete(g,(4,6,8,10,13,14,16,23,24),1)
                    #print(g.shape)
                    if g.shape[0] == 256:
                        samplelist.append(g)
                        idlist.append(_ - 769)
                    else: 
                        print("issue")
                        print(g)
                    h = h + 0.1
        return samplelist, idlist
'''
a = DataReader()
print(a.load_data())
'''

        