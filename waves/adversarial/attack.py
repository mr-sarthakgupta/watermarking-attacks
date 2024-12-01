import torch
from surrogate import adv_surrogate_model_attack

# data_path = "/scratch/vidit_a_mfs.iitr/waves/adversarial/Neurips24_ETI_BeigeBox/treering"
# model_path = "surrogate_models/adv_cls_wm1_wm2_tree_ring.pth"
# output_path = "/scratch/vidit_a_mfs.iitr/waves/adversarial/output_treering"

data_path = "/scratch/vidit_a_mfs.iitr/waves/adversarial/Neurips24_ETI_BeigeBox/stegastamp"
model_path = "surrogate_models/adv_cls_wm1_wm2_tree_ring.pth"
output_path = "/scratch/vidit_a_mfs.iitr/waves/adversarial/output_stegastamp"

strengths = [1/255, 2/255, 4/255, 6/255, 64/255]
target_label = 1

adv_surrogate_model_attack(
    data_path,
    model_path,
    strengths[4],
    output_path,
    target_label,
    warmup=True,
    device=torch.device("cuda:0"),
)

