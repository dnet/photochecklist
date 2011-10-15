from __future__ import with_statement, unicode_literals
from flask import Flask, render_template
import os
import re
import codecs

app = Flask(__name__)

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
			self.items = [row.strip() for row in f if len(row) > 2]


@app.route("/")
def cl_list():
	return render_template('cl_list.html', checklists=CheckList.get_lists())

@app.route("/<checklist>")
def checklist(checklist):
	return render_template('checklist.html', checklist=CheckList(checklist))

if __name__ == "__main__":
	app.run()
