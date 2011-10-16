Photo Checklist
===============

[![Flattr Button](http://api.flattr.com/button/button-static-50x60.png "Flattr This!")](https://flattr.com/thing/416722/Photo-Checklist "Flattr")

Usage
-----

At first, the web application displays a list of checklists. Selecting a checklist displays the list of photographs to take. Those items that are already done have a checked box left to them and the photos are displayed below the title. To add or delete a photo, a simple panel can be shown/hidden by clicking on the title.

Setup and install
-----------------

1. Install the dependencies if necessary (see below).
2. Create a new checklist (see below)
3. You can now test it by running `python photochecklist.py` and opening the URL seen in the output (usually http://127.0.0.1:5000).

License
-------

The whole project is licensed under MIT license.

Checklist format
----------------

Checklists are stored in the `checklist/name_of_checklist/` directory. This directory *must* contain a `checklist.txt` file, which can be created with the editor of your choice. In case non-ASCII characters are used, the application presumes UTF-8. The first line of the file is the title, which will be displayed on the web interface, every other non-empty line will be treated as a checklist item.

Dependencies
------------

 - Python 2.6 or 2.7
 - Flask (Debian/Ubuntu package: `python-flask`)
 - pgmagick (Debian/Ubuntu package: `python-pgmagick`)

