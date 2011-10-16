#!/usr/bin/env python

from __future__ import with_statement, unicode_literals
from binascii import hexlify
from itertools import imap
from functools import partial
from cache import get_sized_image
import os
import re
import codecs

def safe_dir(unsafe):
	return '_{0}_'.format(hexlify(unsafe.group(0)))

def jpg2num(jpg):
	return int(jpg[:-4])

def get_last_file_in(directory):
	try:
		return max(imap(jpg2num, os.listdir(directory)))
	except ValueError:
		return 0

class CheckListImage(object):
	SMALL_SIZE = b'64x48'
	BIG_SIZE = b'640x480'

	def __init__(self, filename, item):
		self.filename = filename
		self.item = item

	def get_small_image(self):
		return get_sized_image(self.get_image_file_name(), self.SMALL_SIZE)

	def get_big_image(self):
		return get_sized_image(self.get_image_file_name(), self.BIG_SIZE)

	def get_image_file_name(self):
		return os.path.join(self.item.get_imgdir(), self.filename)

class CheckListItem(object):
	UNSAFE_RE = re.compile(r'[^a-zA-Z\-\.0-9]+')

	def __init__(self, checklist, text):
		self.text = text
		self.checklist = checklist

	def __unicode__(self):
		return self.text

	def get_dirname(self):
		return self.UNSAFE_RE.sub(safe_dir, self.text)

	def get_images(self):
		try:
			ls = os.listdir(self.get_imgdir())
		except OSError:
			return []
		return imap(partial(CheckListImage, item=self), sorted(ls, key=jpg2num))

	def get_imgdir(self):
		return os.path.join(self.checklist.full_dir, self.get_dirname())

	def save_image(self, image):
		imgdir = self.get_imgdir()
		if not os.path.exists(imgdir):
			os.mkdir(imgdir)
		filename = '{0}.jpg'.format(get_last_file_in(imgdir) + 1)
		image.save(os.path.join(imgdir, filename))

class CheckList(object):
	DIR = 'checklists'
	FILE = 'checklist.txt'
	DIR_RE = re.compile(r'^[a-zA-Z\-\._0-9]+$')

	@classmethod
	def get_lists(cls):
		return imap(CheckList, sorted(os.listdir(cls.DIR)))
	
	def __init__(self, dirname):
		if not self.DIR_RE.match(dirname):
			raise RuntimeError('Invalid directory name')
		self.dirname = dirname
		self.full_dir = os.path.join(self.DIR, dirname)
		with codecs.open(os.path.join(self.full_dir, self.FILE), 'r', 'utf-8') as f:
			self.title = f.readline().strip()
			self.items = [CheckListItem(self, row.strip()) for row in f if len(row) > 2]

	def get_item_by_text(self, text):
		for item in self.items:
			if item.text == text:
				return item
		raise RuntimeError('Invalid item text')

	def save_image(self, itemtext, image):
		item = self.get_item_by_text(itemtext)
		item.save_image(image)
