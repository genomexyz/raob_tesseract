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
extended_width = 163
extended_width2 = 100
index_str = [['trop_lvl', 'trop_lvl.jpg'],
['frzg_lvl', 'frzg_lvl.jpg'],
['cclEL_hgt', 'cclEL_hgt.jpg'],
['lfcEL_hgt', 'lfcEL_hgt.jpg'],
['lfc_hgt', 'lfc_hgt.jpg'],
['ccl_hgt', 'ccl_hgt.jpg'],
['lcl_hgt', 'lcl_hgt.jpg'],
['water', 'water.jpg'],
['hail', 'hail.jpg'],
['t2gust', 't2gust.jpg'],
['windex', 'windex.jpg'],
['sweat', 'sweat.jpg'],
['cap', 'cap.jpg'],
['boyden', 'boyden.jpg'],
['stt', 'stt.jpg'],
['KO', 'ko.jpg'],
['LI', 'li.jpg'],
['TT', 'tt.jpg'],
['KI', 'ki.jpg'],
['Tc', 'tc.jpg'],
['Storm', 'storm.jpg']]

index_str2 = [['CAPE Only', 'cape_only.jpg'],
['CAPE 0-3 km', 'cape03.jpg'],
['CIN Total', 'cin_total.jpg'],
['DCAPE 6km', 'dcape6km.jpg'],
['VGP 0-4km', 'vgp04km.jpg'],
['EHI 0-2km', 'ehi02km.jpg'],
['MVV', 'mvv.jpg'],
['BRN', 'brn.jpg']]

def extract_str(img_target, img_sample, ext_width):
	res = cv2.matchTemplate(img_target, img_sample, cv2.TM_CCOEFF)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

	h, w = np.shape(img_sample)
	top_left = max_loc
	#bottom_right = (top_left[0] + w + extended_width, top_left[1] + h)

	cropped = img[top_left[1]:top_left[1]+h-1, top_left[0]:top_left[0]+w-1+ext_width]
	
	#additional step
	white_canvas = np.zeros((400,400), dtype=np.uint8)
	white_canvas.fill(255)
	white_canvas[50:50+len(cropped), 50:50+len(cropped[0])] = cropped
	string = pytesseract.image_to_string(white_canvas)
	while '\n' in string:
		string = string.replace('\n', '')
	while '\t' in string:
		string = string.replace('\t', '')
	while '  ' in string:
		string = string.replace('  ', ' ')
	while '_' in string:
		string = string.replace('_', '')
	while '=' in string:
		string = string.replace('=', '-')
	return string

if len(sys.argv) < 2:
	print('Usage: ./extract_index.py image_file')
	exit()

image_file = sys.argv[1]
img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)

#read all index string image
index_img_arr = []
for i in range(len(index_str)):
	index_img_arr.append(cv2.imread(index_str[i][1], cv2.IMREAD_GRAYSCALE))

#read all index string image
index_img_arr2 = []
for i in range(len(index_str2)):
	index_img_arr2.append(cv2.imread(index_str2[i][1], cv2.IMREAD_GRAYSCALE))

for i in range(len(index_img_arr)):
	index = extract_str(img, index_img_arr[i], extended_width)[:-1]
	print(index)

for i in range(len(index_img_arr2)):
	index = extract_str(img, index_img_arr2[i], extended_width2)[:-1]
	print(index)
