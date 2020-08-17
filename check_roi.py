#!/usr/bin/python3

try:
	from PIL import Image, ImageDraw
except ImportError:
	import Image
import pytesseract
from pytesseract import Output
import sys
import cv2
import numpy as np

if len(sys.argv) < 2:
	print('Usage: ./check_roi.py image_file')
	exit()

image_file = sys.argv[1]

# Simple image to string
img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
for i in range(n_boxes-1):
	(x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
	cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imwrite(image_file[:image_file.find('.')]+'_roi'+image_file[image_file.find('.'):], img)
