#!/bin/bash
# Synthetic fixtures, made fresh each run (nothing binary in git): a 12 s demo filmed "off the screen"
# and three 3.5 s openings, all ffmpeg test patterns at 1080 x 1920.
set -e
mkdir -p openings
ffmpeg -v error -y -f lavfi -i testsrc2=s=1080x1920:r=30:d=12 -c:v libx264 -pix_fmt yuv420p rip-demo.mp4
ffmpeg -v error -y -f lavfi -i mandelbrot=s=1080x1920:r=30 -t 3.5 -c:v libx264 -pix_fmt yuv420p openings/tired.mp4
ffmpeg -v error -y -f lavfi -i "cellauto=s=1080x1920:r=30:rule=110" -t 3.5 -c:v libx264 -pix_fmt yuv420p openings/shocked.mp4
ffmpeg -v error -y -f lavfi -i "smptehdbars=s=1080x1920:r=30" -t 3.5 -c:v libx264 -pix_fmt yuv420p openings/relieved.mp4
