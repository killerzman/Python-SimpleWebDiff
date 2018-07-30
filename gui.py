from appJar import gui
import subprocess
import sys

def open_cmd(args):

	if sys.platform == 'win32':
		command = 'start cmd /k'
		for arg in args:
			command += " " + arg
		subprocess.call(command, shell = True)

def parse_complete():

	pass

def parse_checker():

	args = ['python', '-u', 'web_diff.py']

	link = app.getEntry('Website')
	if(link):
		args.append(link)
	if(app.getCheckBox('-r')):
		args.append('-r')
	if(app.getCheckBox('-o')):
		args.append('-o')
	if(app.getCheckBox('-t')):
		args.append('-t')
	time_nr = app.getEntry('Time')
	if(time_nr):
		args.append(time_nr)
	if(app.getCheckBox('-w')):
		args.append('-w')
	if(app.getCheckBox('-v')):
		args.append('-v')

	open_cmd(args)

def parse_check(button):

	app.threadCallback(parse_checker, parse_complete)
        
app = gui("web_diff gui", "500x500")
app.setLocation("CENTER")
app.setBg("SteelBlue")
app.setFont(15)
app.setResizable(False)

app.addLabelEntry("Website",0,0,4)
app.addCheckBox("-r",1,0)
app.addCheckBox("-o",1,1)
app.addCheckBox("-t",1,2)
app.addLabelEntry("Time",1,3)
app.setEntryDefault("Time", 60)
app.addCheckBox("-w",2,0)
app.addCheckBox("-v",2,1)

app.addButton("Check", parse_check, 3,1)

app.setFocus("Website")

app.go()