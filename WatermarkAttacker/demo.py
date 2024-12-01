import sys
import torch
import os
import glob
import numpy as np

from regen_pipe import ReSDPipeline

from utils import eval_psnr_ssim_msssim, bytearray_to_bits
from watermarker import InvisibleWatermarker
from wmattacker import DiffWMAttacker, VAEWMAttacker, JPEGAttacker

wm_text = 'test'
device = 'cuda:0'
ori_path = 'Neurips24_ETI_BeigeBox'
output_path = 'attacked_images'
print_width = 50

os.makedirs(output_path, exist_ok=True)
ori_img_paths = glob.glob(os.path.join(ori_path, '*.*'))
ori_img_paths = sorted([path for path in ori_img_paths if path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))])
print(ori_img_paths)

wmarkers = {
    'DwtDct': InvisibleWatermarker(wm_text, 'dwtDct'),
    'DwtDctSvd': InvisibleWatermarker(wm_text, 'dwtDctSvd'),
    'RivaGAN': InvisibleWatermarker(wm_text, 'rivaGan'),
}

pipe = ReSDPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16, revision="fp16")
pipe.set_progress_bar_config(disable=True)
pipe.to(device)
print('Finished loading model')

attackers = {
    'diff_attacker_60': DiffWMAttacker(pipe, batch_size=5, noise_step=60, captions={}),
    'cheng2020-anchor_3': VAEWMAttacker('cheng2020-anchor', quality=3, metric='mse', device=device),
    'bmshj2018-factorized_3': VAEWMAttacker('bmshj2018-factorized', quality=3, metric='mse', device=device),
    'jpeg_attacker_50': JPEGAttacker(quality=50),
}

def add_watermark(wmarker_name, wmarker):
    print('*' * print_width)
    print(f'Watermarking with {wmarker_name}')
    os.makedirs(os.path.join(output_path, wmarker_name + '/noatt'), exist_ok=True)
    for ori_img_path in ori_img_paths:
        img_name = os.path.basename(ori_img_path)
        wmarker.encode(ori_img_path, os.path.join(output_path, wmarker_name + '/noatt', img_name))

for wmarker_name, wmarker in wmarkers.items():
    add_watermark(wmarker_name, wmarker)
print('Finished watermarking')

for wmarker_name, wmarker in wmarkers.items():
    for attacker_name, attacker in attackers.items():
        print('*' * print_width)
        print(f'Attacking {wmarker_name} with {attacker_name}')
        wm_img_paths = []
        att_img_paths = []
        os.makedirs(os.path.join(output_path, wmarker_name, attacker_name), exist_ok=True)
        for ori_img_path in ori_img_paths:
            img_name = os.path.basename(ori_img_path)
            wm_img_paths.append(os.path.join(output_path, wmarker_name + '/noatt', img_name))
            att_img_paths.append(os.path.join(output_path, wmarker_name, attacker_name, img_name))
        attackers[attacker_name].attack(wm_img_paths, att_img_paths)

print('Finished attacking')

wm_results = {}
for wmarker_name, wmarker in wmarkers.items():
    print('*' * print_width)
    print(f'Watermark: {wmarker_name}')
    wm_successes = []
    wm_psnr_list = []
    wm_ssim_list = []
    wm_msssim_list = []
    for ori_img_path in ori_img_paths:
        img_name = os.path.basename(ori_img_path)
        wm_img_path = os.path.join(output_path, wmarker_name+'/noatt', img_name)
        wm_psnr, wm_ssim, wm_msssim = eval_psnr_ssim_msssim(ori_img_path, wm_img_path)
        wm_psnr_list.append(wm_psnr)
        wm_ssim_list.append(wm_ssim)
        wm_msssim_list.append(wm_msssim)
    wm_results[wmarker_name] = {}
    wm_results[wmarker_name]['wm_psnr'] = np.array(wm_psnr_list).mean()
    wm_results[wmarker_name]['wm_ssim'] = np.array(wm_ssim_list).mean()
    wm_results[wmarker_name]['wm_msssim'] = np.array(wm_msssim_list).mean()

print('Finished evaluating watermarking')