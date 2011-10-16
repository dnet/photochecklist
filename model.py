#!/usr/bin/env python

from __future__ import with_statement, unicode_literals
from binascii import hexlify, unhexlify
import os
import re
import codecs

def safe_dir(unsafe):
	return '_{0}_'.format(hexlify(unsafe.group(0)))

def get_last_file_in(directory):
	try:
		return max(int(fn[:-4]) for fn in os.listdir(directory))
	except ValueError:
		return 0

class CheckListItem(object):
	UNSAFE_RE = re.compile(r'[^a-zA-Z\-\.0-9]+')

	def __init__(self, checklist, text):
		self.text = text
		self.checklist = checklist

	def __unicode__(self):
		return self.text

	def get_dirname(self):
		return self.UNSAFE_RE.sub(safe_dir, self.text)

	def save_image(self, image):
		imgdir = os.path.join(self.checklist.full_dir, self.get_dirname())
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
		return (CheckList(dirname) for dirname in sorted(os.listdir(cls.DIR)))
	
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
