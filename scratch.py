import sys
import os
sys.path.append(os.getcwd())
import torch
from shared.model import CNN
import numpy as np

model = CNN()
params = [val.cpu().numpy() for _, val in model.state_dict().items()]
total_abs_weight = sum(np.sum(np.abs(p)) for p in params)
print(f"Normal Magnitude: {int(total_abs_weight * 100)}")

