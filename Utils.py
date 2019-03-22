# !usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import colorsys
import numpy as np
from colorsys import rgb_to_hsv

def to_hsv(color): 
	""" converts color tuples to floats and then to hsv """
	return rgb_to_hsv(*[x / 255.0 for x in color]) #rgb_to_hsv wants floats!

def color_dist(c1, c2):
	""" returns the squared euklidian distance between two color vectors in hsv space """
	return sum((a - b) ** 2 for a, b in zip(to_hsv(c1), to_hsv(c2)))

def min_color_diff(color_to_match, colors):
	""" returns the `(distance, color_name)` with the minimal distance to `colors`"""
	return min([(color_dist(color_to_match, test), colors[test]) for test in colors])

def max_color_diff(color_to_match, colors):
	""" returns the `(distance, color_name)` with the minimal distance to `colors`"""
	return max([(color_dist(color_to_match, test), colors[test]) for test in colors])

def get_dominant_color(image, target):
	#颜色模式转换，以便输出rgb颜色值
	# resultDict = {}
	image = image.convert('RGBA')

	#生成缩略图，减少计算量，减小cpu压力
	image.thumbnail((200, 200))

	max_score = 0 # 原来的代码此处为None
	dominant_color = 0 # 原来的代码此处为None，但运行出错，改为0以后 运行成功，原因在于在下面的 score > max_score的比较中，max_score的初始格式不定

	for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
		# 跳过纯黑色
		if a == 0:
			continue

		saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

		y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

		y = (y - 16.0) / (235 - 16)

		# 忽略高亮色
		if y > 0.8 or y < 0.2:
			continue

		# Calculate the score, preferring highly saturated colors.
		# Add 0.1 to the saturation so we don't completely ignore grayscale
		# colors by multiplying the count by zero, but still give them a low
		# weight.
		score = (saturation + 0.1) * count
		resultDict[(r, g, b)] = (r, g, b, y, score)
	for color in target:
		print color, max_color_diff(color, resultDict)
		# resultList[(r, g, b)] = (score, (r, g, b), y)
		# print r, g, b, score
	# for color in target:
	# 	print min_color_diff(color, resultList)

	# 	if score > max_score:
	# 		max_score = score
	# 		dominant_color = (r, g, b, y)

	# return dominant_color, max_score

if __name__ == '__main__':
	from PIL import Image
	left = [
		(245, 218, 177),
		(105, 74, 45)
	]
	right = [
		(24, 14, 7),
		(37, 28, 23),
		(161, 114, 121),
		(245, 228, 237)
	]
	for c in right:
		print c, np.std(c)
	# get_dominant_color(Image.open('left.png'), left)