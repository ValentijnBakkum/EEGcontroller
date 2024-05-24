import torch
import torch.nn as nn

#Created/modified B-spline activation function from modification of files in github Repo of Kolmogorov-Arnold Networks
#Link: https://github.com/KindXiaoming/pykan/blob/master/kan/spline.py

class Bspline_segment_calc(nn.Module):
    def __init__(self,grid = 10,k = 0,extend = True,device = "cpu"):
        super().__init__()
        
    #-----Make Grid-----#    
    def make_grid(self,grid = 10):
        grid_knots = torch.linspace(-1,1,steps= grid + 1)
        grid_size  = torch.einsum('i,j->ij',torch.ones(5,), grid_knots)
        return grid_size 
    
    #-----Extends grid for accuracy-----#    
    def extend_grid(self,grid,extend=True,k=3,device = "cpu"):
        if extend == True:
            h = (grid[:,[-1]] - grid[:,[0]]) / (grid.shape[1] - 1)
            k_extend = k
            for i in range(k_extend):
                grid = torch.cat([grid[:,[0]] - h, grid],dim=1)
                grid = torch.cat([grid, grid[:,[-1]] + h],dim=1)
            grid = grid.to(device)
            return grid
        else:
            return grid
    
    #-----Calculate Bi in B-spline formula-----#    
    def Cox_deBoor(self,x,grid,k,extend,device):
        if extend == True:
            grids = self.make_grid() # make grid
            grids = self.extend_grid(grids) # extend grid
            grids = grids.unsqueeze(dim=2).to(device)
        else:
            grids = grid.unsqueeze(dim=2).to(device)
        x = x.unsqueeze(dim=1).to(device)
        if k == 0:
            value = (x >= grids[:,:-1]) * (x < grids[:,1:])
        else:
            B_km1 = self.Cox_deBoor(x = x[:,0],grid = grids[:,:,0],k = k - 1,extend = False, device = device)
            value = (x - grids[:, :-(k + 1)]) / (grids[:, k:-1] - grids[:, :-(k + 1)]) * B_km1[:, :-1] + (
            grids[:, k + 1:] - x) / (grids[:, k + 1:] - grids[:, 1:(-k)]) * B_km1[:, 1:]
        return value
        
bspline = Bspline_segment_calc(grid = 10,k = 3, extend = True)
#grid = bspline.make_grid()
#grid = bspline.extend_grid(True,3,grid)
#print(grid)
print(bspline.Cox_deBoor(torch.rand((5,20)),10,3,True,"cpu").shape)