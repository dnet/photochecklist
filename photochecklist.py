#!/usr/bin/env python

from __future__ import with_statement, unicode_literals
from flask import Flask, render_template, request, redirect
from model import CheckList

app = Flask(__name__)

@app.route("/")
def cl_list():
	return render_template('cl_list.html', checklists=CheckList.get_lists())

@app.route("/<checklist>", methods=['GET', 'POST'])
def checklist_page(checklist):
	cl_obj = CheckList(checklist)
	if request.method == 'POST':
		if 'delete' in request.form:
			try:
				image = int(request.form['delete']) - 1
			except ValueError:
				pass
			else:
				cl_obj.delete_image(request.form['item'], image)
		else:
			cl_obj.save_image(request.form['item'], request.files['file'])
		return redirect(request.url)
	else:
		return render_template('checklist.html', checklist=cl_obj)

if __name__ == "__main__":
	app.run(debug=True)
