# Attacking Invisible Watermarks

This repository contains my experiments for "NeurIPS 2024 Competition Erasing the Invisible: A Stress-Test Challenge for Image Watermarks" where I ended up at the 6th position.

I found many basic perturbations to be much more effective than some of the recent attack methods. Flipping the image horizontally was found to be the most effective at breaking the watermark but it did have a relatively high loss in terms of changing the amount of image pixels. Many permutations of such perturbations and other attacks were tried during this competition.

We also experimented with clicking photos of the image using a laptop screen and a smartphone camera and surprisingly even this wasn't completely capable of removing the watermark without degrading image quality severely.

One particular attack which looked promising but which I wasn't able to tune further to improve performance was diffusion regeneration, it created images which were similar enough to the original image and didn't have the watermark.
