#!/bin/bash

python adv_attack.py \
--wm-method treeRing \
--wm-dir /scratch/vidit_a_mfs.iitr/watermark_robustness/Neurips24_ETI_BeigeBox_split/treering \
--org-dir ./images/imagenet/org \
--model-dir checkpoints/classifiers/treeRing_classifier.pt \


python adv_attack.py \
--wm-method stegaStamp \
--wm-dir /scratch/vidit_a_mfs.iitr/watermark_robustness/Neurips24_ETI_BeigeBox_split/stegastamp \
--org-dir ./images/imagenet/org \
--model-dir checkpoints/classifiers/stegaStamp_classifier.pt \

