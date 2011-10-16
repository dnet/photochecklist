#!/usr/bin/env python

from hashlib import sha1
from pgmagick import Image
import os

PARTS = ('static', 'cache')
DIR = os.path.join(*PARTS)

def get_sized_image(filename, size):
	if not os.path.exists(DIR):
		os.mkdir(DIR)
	cache_hash = sha1('{0}\0{1}'.format(filename, size)).hexdigest() + '.jpg'
	cache_path = os.path.join(DIR, cache_hash)
	if not os.path.exists(cache_path):
		im = Image(filename.encode('utf-8'))
		im.sample(size)
		im.write(cache_path)
	return '/'.join(PARTS + (cache_hash,))
