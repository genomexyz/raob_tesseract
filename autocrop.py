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

#setting
trop_lvl_file = 'trop_lvl.jpg'
#trop_lvl_file = 'cekini.jpeg'
frzg_lvl_file = 'frzg_lvl.jpg'
extended_width = 163

def extract_index(img_target, img_sample):
	res = cv2.matchTemplate(img_target, img_sample, cv2.TM_CCOEFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#	print('shape', np.shape(trop_lvl_img))
	h, w, dim = np.shape(trop_lvl_img)
	top_left = max_loc
	bottom_right = (top_left[0] + w, top_left[1] + h)
	cropped = img_target[top_left[1]:top_left[1]+h-1, top_left[0]:top_left[0]+w-1]
#	cropped = 255-cropped
	
	cv2.imwrite('contoh.jpg', cropped)
	
	return pytesseract.image_to_string(cropped)
#	return pytesseract.image_to_string(cropped, output_type=Output.DICT)

if len(sys.argv) < 2:
	print('Usage: ./autocrop.py image_file')
	exit()

image_file = sys.argv[1]
img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)

trop_lvl_img = cv2.imread(trop_lvl_file, cv2.IMREAD_GRAYSCALE)
frzg_lvl_img = cv2.imread(frzg_lvl_file, cv2.IMREAD_GRAYSCALE)

#print(extract_index(img, trop_lvl_img))

# Apply template Matching
res = cv2.matchTemplate(img, trop_lvl_img, cv2.TM_CCOEFF)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

h, w = np.shape(trop_lvl_img)
top_left = max_loc
bottom_right = (top_left[0] + w + extended_width, top_left[1] + h)

cropped = img[top_left[1]:top_left[1]+h-1, top_left[0]:top_left[0]+w-1+extended_width]

#improve crop image with dilation
#kernel = np.ones((2,2), np.uint8)
#cropped_dilation = cv2.dilate(cropped, kernel, iterations=1) 


#additional step
white_canvas = np.zeros((400,400), dtype=np.uint8)
white_canvas.fill(255)
white_canvas[50:50+len(cropped), 50:50+len(cropped[0])] = cropped

#white_canvas = 255 - white_canvas

print(np.shape(white_canvas), len(cropped), len(cropped[0]), np.shape(cropped))
print(pytesseract.image_to_string(white_canvas))
cv2.imwrite('white_canvas.jpg', white_canvas)

#cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#cv2.rectangle(img,top_left, bottom_right, 0, 2)
#cv2.imwrite(image_file[:image_file.find('.')]+'_crop_extend'+image_file[image_file.find('.'):], img)

#print(bottom_right, top_left)
#cropped = img[y:y+len(trop_lvl_img), x:x+len(trop_lvl_img[0])+extended_width]

#cv2.imwrite(image_file[:image_file.find('.')]+'_crop'+image_file[image_file.find('.'):], cropped)
