import torch
import torch.nn as nn
import torch.nn.functional as F

#Created/modified B-spline activation function from modification of files in github Repo of Kolmogorov-Arnold Networks
#Link: https://github.com/KindXiaoming/pykan/blob/master/kan/spline.py

class Bspline_segment_calc(nn.Module):
    def __init__(self,input_dim,device = "cpu"):
        super().__init__()
        self.device = device
        self.input_dim = input_dim
    #-----Make Grid-----#    
    def make_grid(self,grid = 10):
        grid_knots = torch.linspace(0,1,steps= grid + 1)
        grid_size  = torch.einsum('i,j->ij',torch.ones(self.input_dim,), grid_knots)
        return grid_size 
    
    #-----Extends grid for accuracy-----#    
    def extend_grid(self,grid,extend=True,k=3):
        if extend == True:
            #print(grid.shape)
            h = (grid[:,[-1]] - grid[:,[0]]) / (grid.shape[1] - 1)
            k_extend = k
            for i in range(k_extend):
                grid = torch.cat([grid[:,[0]] - h, grid],dim=1)
                grid = torch.cat([grid, grid[:,[-1]] + h],dim=1)
            grid = grid.to(self.device)
            return grid
        else:
            return grid
    
    #-----Calculate Bi in B-spline formula-----#    
    def Cox_deBoor(self,x,grid,k,extend):
        if extend == True:
            grids = self.make_grid(grid) # make grid
            grids = self.extend_grid(grids,True,k) # extend grid
            grids = grids.unsqueeze(dim=2).to(self.device)
        else:
            grids = grid.unsqueeze(dim=2).to(self.device)
        x = x.unsqueeze(dim=1).to(self.device)
        if k == 0:
            value = (x >= grids[:,:-1]) * (x < grids[:,1:])
        else:
            B_km1 = self.Cox_deBoor(x = x[:,0],grid = grids[:,:,0],k = k - 1,extend = False)
            value = (x - grids[:, :-(k + 1)]) / (grids[:, k:-1] - grids[:, :-(k + 1)]) * B_km1[:, :-1] + (
            grids[:, k + 1:] - x) / (grids[:, k + 1:] - grids[:, 1:(-k)]) * B_km1[:, 1:]
        return value
        
class spline_activation(nn.Module):
    def __init__(self,grid = 10,k = 3,extend = True,device = "cpu",input_dim = 5):
        super().__init__()
        self.grid = grid
        self.k = k
        self.extend = extend
        self.device = device
        self.input_dim = input_dim
        self.Bspline = Bspline_segment_calc(self.input_dim,device = self.device)
        self.size = grid + 1  + (k-1)
        self.coef = torch.nn.Parameter(torch.rand(self.size,self.input_dim))
        self.coefb = torch.nn.Parameter(torch.rand(self.input_dim,self.size))
    def forward(self,x):
        #x = F.normalize(x)
        x = x.T
        B = self.Bspline.Cox_deBoor(x,k=self.k,grid=self.grid,extend=self.extend)
        out = torch.einsum('ij,ijk->ik', self.coefb, B)
        return out.T
        
        
#bspline = spline_activation()
#grid = bspline.make_grid()
#grid = bspline.extend_grid(True,3,grid)
#print(grid)
#print(bspline(torch.normal(0,1,(2,5))).shape)