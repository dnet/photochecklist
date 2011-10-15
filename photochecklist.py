#!/usr/bin/env python

from __future__ import with_statement, unicode_literals
from flask import Flask, render_template, request, redirect
from binascii import hexlify, unhexlify
import os
import re
import codecs

app = Flask(__name__)


def safe_dir(unsafe):
	return '_{0}_'.format(hexlify(unsafe.group(0)))

class CheckListItem(object):
	UNSAFE_RE = re.compile(r'[^a-zA-Z\-\.0-9]+')

	def __init__(self, text):
		self.text = text

	def __unicode__(self):
		return self.text

	def get_dirname(self):
		return self.UNSAFE_RE.sub(safe_dir, self.text)

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
		with codecs.open(os.path.join(self.DIR, dirname, self.FILE), 'r', 'utf-8') as f:
			self.title = f.readline().strip()
			self.items = [CheckListItem(row.strip()) for row in f if len(row) > 2]

	def save_image(self, itemtext, image):
		if itemtext not in (unicode(i) for i in self.items):
			raise RuntimeError('Invalid item text')
		subdir = CheckListItem(itemtext).get_dirname()
		imgdir = os.path.join(self.DIR, self.dirname, subdir)
		if not os.path.exists(imgdir):
			os.mkdir(imgdir)
		try:
			filename = '{0}.jpg'.format(max(int(fn[:-4]) for fn in os.listdir(imgdir)) + 1)
		except ValueError:
			filename = '1.jpg'
		image.save(os.path.join(imgdir, filename))

@app.route("/")
def cl_list():
	return render_template('cl_list.html', checklists=CheckList.get_lists())

@app.route("/<checklist>", methods=['GET', 'POST'])
def checklist(checklist):
	cl_obj = CheckList(checklist)
	if request.method == 'POST':
		cl_obj.save_image(request.form['item'], request.files['file'])
		return redirect(request.url)
	else:
		return render_template('checklist.html', checklist=cl_obj)

if __name__ == "__main__":
	app.run()
