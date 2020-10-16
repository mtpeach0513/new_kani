#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np

img = cv2.imread(sys.argv[1])
if img is None:
    print(f"Failed to load image. {os.path.abspath(sys.argv[1])}")
img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = np.zeros(img.shape, dtype=np.uint8)

cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

cv2.fillPoly(mask, cnts, [255,255,255])
mask = 255 - mask
img = cv2.bitwise_or(img, mask)

kernel = np.ones((1,1), np.uint8)
img = cv2.dilate(img, kernel, iterations=1)
img = cv2.erode(img, kernel, iterations=1)

gamma = 0.5
imax = img.max()
img = imax * (img / imax)**(1/gamma)

#dst = cv2.medianBlur(img, ksize=3)

#cv2.imshow("mask", mask)
#cv2.imshow("gray", dst)
new_img_name = "gray"+sys.argv[1]
cv2.imwrite(new_img_name, img)
cv2.waitKey()
cv2.destroyAllWindows()
