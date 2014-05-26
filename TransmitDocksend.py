import sublime
import sublime_plugin
import subprocess
import os.path

class TransmitDocksendCommand(sublime_plugin.TextCommand):
	def run(self, edit, connection=False):
		if connection == 'active':
			script = """
			on run
			tell application "Transmit"
				tell current tab of front document
					tell remote browser
						upload item at path "%s"
					end tell
				end tell
			end tell
			end run
			"""
		else:
			script = """
			on run
				ignoring application responses
					tell application "Transmit"
						open POSIX file "%s"
					end tell
				end ignoring
			end run
			"""

		# scss
		path = self.view.file_name()
		root, ext = os.path.splitext(path)
		basename = os.path.basename(path)

		if ext == '.scss' :
			if basename[0:1] == '_' :
				path = path.replace(basename, '')
				
			path = path.replace('scss', 'css')

		proc = subprocess.Popen(
			["osascript", "-e", script % path], 
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE, 
			stderr=subprocess.STDOUT
		)
