#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback
import time
import paramiko
from pydoc import describe

import dbconnector
from paramiko.py3compat import b, u, decodebytes
import shutil
from time import gmtime, strftime
from sftpserver.stub_sftp import StubServer, StubSFTPServer


host_key = paramiko.RSAKey(filename='/home/serv/.rsa/rsaserv.key')
isrunning = False;
loggeduser = ""
loggedpass = ""
stop = False
stopruning = False

class Server (paramiko.ServerInterface):
	# 'data' is the output of base64.b64encode(key)
	# (using the "user_rsa_key" files)
	data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
			b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
			b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
			b'UWT10hcuO4Ks8=')
	good_pub_key = paramiko.RSAKey(data=decodebytes(data))

	def __init__(self):
		self.event = threading.Event()

	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, password):
	# with open('/home/serv/Desktop/REQUEST-DIR/authenitcation') as f:
	# 	content = f.readlines()
	# content = [x.strip().split(',') for x in content]
	#    for j in range(len(content)):
	#       if (username == content[j][0]) and (password == content[j][1]):
		if(dbconnector.authenticateuer(username,password)):
			 print "Success!"
			 return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

	def check_auth_publickey(self, username, key):
		print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
		if (username == 'robey') and (key == self.good_pub_key):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

	def check_auth_gssapi_with_mic(self, username,
								   gss_authenticated=paramiko.AUTH_FAILED,
								   cc_file=None):
		"""
		.. note::
			We are just checking in `AuthHandler` that the given user is a
			valid krb5 principal! We don't check if the krb5 principal is
			allowed to log in on the server, because there is no way to do that
			in python. So if you develop your own SSH server with paramiko for
			a certain platform like Linux, you should call ``krb5_kuserok()`` in
			your local kerberos library to make sure that the krb5_principal
			has an account on the server and is allowed to log in as a user.
		.. seealso::
			`krb5_kuserok() man page
			<http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
		"""
		if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

	def check_auth_gssapi_keyex(self, username,
								gss_authenticated=paramiko.AUTH_FAILED,
								cc_file=None):
		if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

	def enable_auth_gssapi(self):
		return True

	def get_allowed_auths(self, username):
		return 'gssapi-keyex,gssapi-with-mic,password,publickey'

	def check_channel_shell_request(self, channel):
		self.event.set()
		return True

	def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
								  pixelheight, modes):
		return True

BACKLOG = 10
DoGSSAPIKeyExchange = True
class ConnHandlerThd(threading.Thread):
	def __init__(self, conn, sock):
		threading.Thread.__init__(self)
		self._conn = conn
		self._sock = sock
	def run(self):
		try:
			t = paramiko.Transport(self._conn, gss_kex=DoGSSAPIKeyExchange)
			t.set_gss_host(socket.getfqdn(""))
			try:
				t.load_server_moduli()
			except:
				print('(Failed to load moduli -- gex will be unsupported.)')
				raise
			t.add_server_key(host_key)
			t.set_subsystem_handler(
				'sftp', paramiko.SFTPServer, StubSFTPServer)
			server = Server()
			try:
				t.start_server(server=server)
			except paramiko.SSHException as e:
				print e
				print('*** SSH negotiation failed.')
				sys.exit(1)
			channel = t.accept()
		 #   channel.exec_command("cd /home/serv/test")
			global stopruning
			while t.is_active():
				if(stopruning):
					t.close()
					self._conn.close()
					stopruning=False
					break;
				time.sleep(1)
	# wait for auth
 #   chan = t.accept(20)
 #   if chan is None:
 #       print('*** No channel.')
 #       sys.exit(1)
 #   print('Authenticated!')

   #server.event.wait(10)
   # if not server.event.is_set():
   #     print('*** Client never asked for a shell.')
   #     sys.exit(1)

#    chan.send('\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n')
#    chan.send('We are on fire all the time!  Hooray!  Candy corn for everyone!\r\n')
#    chan.send('Happy birthday to Robot Dave!\r\n\r\n')
#    chan.send('Username: ')
#    f = chan.makefile('rU')
#    username = f.readline().strip('\r\n')
#    chan.send('\r\nI don\'t like you, ' + username + '.\r\n')
#    chan.close()

   

		except Exception as e:
			print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
			traceback.print_exc()
			try:
				t.close()
			except:
				pass
# now connect
def running():
	return isrunning;
def startserver(name,password):
# setup logging
	global loggeduser
	global loggedpass
	loggedpass = password
	loggeduser = name
	paramiko.util.log_to_file('/home/serv/.rsa/demo_server.log')
	global isrunning
	isrunning = True;
	#host_key = paramiko.DSSKey(filename='test_dss.key'
	print('Read key: ' + u(hexlify(host_key.get_fingerprint())))
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		sock.bind(('', 2200))
	except Exception as e:
		print('*** Bind failed: ' + str(e))
		traceback.print_exc()
		sys.exit(1)

	try:
		sock.listen(100)
		print('Listening for connection ...')
	except Exception as e:
		print('*** Listen/accept failed: ' + str(e))
		traceback.print_exc()
		sys.exit(1)
	thread = threading.Thread(target=shutdown, args=(3600,))
	thread.daemon = True
	thread.start()
	sock.setblocking(0)
	global stop
	while True:
		try:
			if not stop:
				conn, addr = sock.accept()
				srv_thd = ConnHandlerThd(conn,sock)
				srv_thd.setDaemon(True)
				srv_thd.start()
			else:
				stop = False
				sock.close()
			time.sleep(1)
		except Exception as e:
			test = e;
def movedata():
	currenttime = strftime("%Y-%m-%d-%H", gmtime())
	destination = "/home/serv/Desktop/DATA/"+currenttime
	if not os.path.isdir(destination):
		os.makedirs(destination)
	for path, subdirs, files in os.walk("/home/serv/test"):
		for name in files:
			shutil.move(os.path.join(path, name), os.path.join(destination, name))
def shutdown(aftertime):
	time.sleep(aftertime)
	global isrunning
	print "SFTP Sever Shutting Down"
	global loggedpass
	global loggeduser
	global stopruning
	print(loggeduser+"~ Time Finished! and he had the password: "+loggedpass)
	if(dbconnector.removeauth(loggeduser,loggedpass)):
		global stop
		stop = True
		stopruning = True
		movedata()
		isrunning = False
