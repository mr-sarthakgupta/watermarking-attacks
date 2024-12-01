import torch

print("PyTorch version:", torch.__version__)
print("CUDA version:", torch.version.cuda)
print(torch.cuda.is_available())