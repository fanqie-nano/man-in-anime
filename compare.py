# !usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import subprocess
from glob import glob
import json
import re
import numpy as np
from PIL import Image

# from Utils import color_dist

AnimeFaceCmd = 'ruby analysis.rb {filename}'
pColor = re.compile(r'red=(\d+?), green=(\d+?), blue=(\d+?),')

def execute_command(cmd, timeout = 30, log = None):
	args = None
	if isinstance(cmd, list):
		args = cmd
	elif isinstance(cmd, (str, unicode)):
		args = cmd.split()
	if args is not None:
		t_beginning = time.time()
		p = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False, close_fds = True)
		while True:
			if p.poll() is not None:
				break
			if timeout and (time.time() - t_beginning) > timeout:
				p.terminate()
				break
			if log:
				log(p.stdout.readline().strip())
			time.sleep(0.1)
		out, err = p.communicate()
		return out, p.returncode, err
	return None, None, None

def analysisColor(colorStr):
	m = pColor.search(colorStr)
	r = hex(int(m.group(1))).split('0x')[-1][-2::]
	g = hex(int(m.group(2))).split('0x')[-1][-2::]
	b = hex(int(m.group(3))).split('0x')[-1][-2::]
	r = int(r, 16)
	g = int(g, 16)
	b = int(b, 16)
	return (r, g, b)

def getMainEyeColor(source_colors, skin_color, hair_color):
	colors = []
	for color in source_colors:
		colors.append(analysisColor(color))
	result = {}
	for color in colors:
		result[color] = np.std(color)
	color = sorted(result.items(), key = lambda x: x[1])[-1][0]
	return color

'''
def getMainEyeColor(img, box):
	eye = img.crop(box)
	color, _ = get_dominant_color(eye)
	print color
	return color
'''
def sample(filename, num = 0):
	mainImage = Image.open(filename)
	out, code, err = execute_command(AnimeFaceCmd.format(filename = filename))
	faceData = json.loads(out)
	for face in faceData:
		num += 1
		face_img = mainImage.crop((face['face']['x'],
			face['face']['y'],
			face['face']['x'] + face['face']['width'],
			face['face']['y'] + face['face']['height']))
		face_img.save('sample/%s_face.jpg'%num)
		skin_color = analysisColor(face['skin_color'])
		hair_color = analysisColor(face['hair_color'])
		left_eye_color = getMainEyeColor(face['eyes']['left']['colors'] + face['eyes']['right']['colors'], skin_color, hair_color)
		skin_img = Image.new('RGB', (128, 128), color = skin_color)
		hair_img = Image.new('RGB', (128, 50), color = hair_color)
		left_eye_img = Image.new('RGB', (40, 40), color = left_eye_color)
		# right_eye_img = Image.new('RGB', (40, 40), color = right_eye_color)
		skin_img.paste(hair_img, (0, 0, 128, 50))
		skin_img.paste(left_eye_img, (10, 65, 50, 105))
		skin_img.paste(left_eye_img, (78, 65, 118, 105))
		skin_img.save('sample/%s_sample.jpg'%num)
	return num

if __name__ == '__main__':
	frameList = glob('frame/*.jpg')
	frameList.sort()
	# sample('46692022_p0.png')
	# sample('d833c895d143ad4b3f6e8a8587025aafa40f0637.jpg')
	# sample('timg.jpeg')
	num = 0
	for filename in frameList:
		num = sample(filename, num)