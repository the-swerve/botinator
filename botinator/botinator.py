import socket, threading, re, sys

from datetime import datetime

class Bot:
	def __init__(self, server_name, port=6667):
		"""
		Pass the server_name (eg. irc.freenode.net), and the port (optional;
		defaults to 6667)
		"""
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_name = server_name
		self.port = port
		self.irc.connect((server_name, int(port)))
		self.bindings = {} # message patterns and responses
		self.patterns = [] # store an ordered list of patterns.
		self.crons = {} # crons responses
		self.time_toggles = {} # toggles for crons
		self.state = {}

	def join(self,chan):
		self.chan = chan
		self.irc.send ('JOIN ' + chan + '\r\n')
		return self

	def nick(self,n):
		self.nick = n
		self.irc.send('NICK ' + n + '\r\n')
	
	def user_and_ircname(self,u='',n=''):
		self.user = u
		self.ircname = n
		self.irc.send('USER ' + ((u + ' ')*3) + ':' + n + '\r\n')
	
	def listen(self, pattern, response):
		""" Bind certain received patterns to responses.  """
		self.patterns.append(pattern)
		self.bindings[pattern] = response
		return self

	def cron(self, time_tuple, response, channel):
		"""
		Have the bot broadcast a message at certain times.  Inspired by crontabs --
		fields may be asterisks, which always stands for 'first-last'.

		time_tuple must be (minute, hour, date, month, weekday)
		"""
		# Each time-based response is paired with a toggle so that we only do the response once in a row.
		self.crons[time_tuple] = (response, channel)
		self.time_toggles[time_tuple] = False
		return self
	
	def check_time(self, time_tuple):
		# Convert each in time_tuple to a pair representing range
		t = datetime.now()
		current_time = (t.minute, t.hour, t.day, t.month, t.weekday())
		for test, match in zip(time_tuple, current_time):
			if test is not None and test is not match:
				return False
		return True

	def __repr__(self):
		return str(self.state)

	def pong(self, data):
		pong = "PONG " + data.split()[1] + "\r\n"
		print('Ponging with: ' + pong)
		self.irc.send(pong)

	def respond(self, channel, response, *args):
		"""
		Send a response, which may be a function returning a string or just a string.
		Response function must have two parameters: list of regex matches and the
		messenger nick.
		"""
		if hasattr(response, '__call__'): # response is a callback function
			try:
				res = response(*args)
			except:
				print('Reponse callback threw exception: ', sys.exc_info()[0], 'line' + str(sys.exc_info()[2].tb_lineno))
				return
		else:
			res = response
		print('Responding: ' + res)
		self.irc.send('PRIVMSG '+ channel + ' :' + res + '\r\n')

	def live(self):
		""" Initialize the event loop thread. """
		while True:
			data = self.irc.recv(4096)
			print(data)
			self.check_messages(data)
			self.check_crons()


	def check_messages(self, data):
		if data.find("PING") != -1:
			self.pong(data)
		elif data.find('PRIVMSG') != -1:
			pieces = data.split()
			channel = pieces[2]
			messenger = re.search(':(.*)!', pieces[0]).group(1)
			if channel == self.nick: # querying
				channel = messenger
			for p in self.patterns:
				matches = re.findall(p, data)
				if matches:
					print("\nFound match: " + str(p))
					self.respond(channel,self.bindings[p],matches,messenger)
					break

	def check_crons(self):
		for time_tuple, (response, channel) in self.crons.iteritems():
			cron_active = self.check_time(time_tuple)
			# When time is current time and toggle is False, respond and set toggle to True.
			# When time is not current time and toggle is True, set toggle to False.
			if cron_active and not self.time_toggles[time_tuple]:
				self.respond(channel,response)
				print(self.time_toggles[time_tuple])
				self.time_toggles[time_tuple] = True
			elif not cron_active and self.time_toggles[time_tuple]:
				print(self.time_toggles[time_tuple])
				self.time_toggles[time_tuple] = False
