import torch
import torch.nn as nn
#from torch.nn.modules.distance import PairwiseDistance
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TripletLoss(nn.Module):
    def __init__(self,alpha = 1, p = 2):
        super(TripletLoss, self).__init__()
        self.alpha = alpha
        self.p = p
        self.pd = nn.PairwiseDistance(p = 2)
    def forward(self,anchor,positive,negative):
        alpha = self.alpha
        ap = self.pd(anchor,positive)
        an = self.pd(anchor,negative)
        Loss = torch.clamp(alpha + torch.pow(ap,2) - torch.pow(an,2), min=0.0)
        return Loss