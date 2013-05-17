import socket, threading, datetime, re, sys

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
		self.bindings = {}
		self.patterns = [] # store an ordered list of patterns.
		self.conditions = {}
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
	
	def bind(self,pattern,response):
		"Bind a matched regex to a response"
		self.patterns.append(pattern)
		self.bindings[pattern] = response
		return self

	def when(self,condition,response):
		"""
		Bind a predicate function to a response.

		The predicate automatically toggles a switch in the bot: by default, the
		toggle is off. When the predicate is true and the toggle is off, the toggle
		goes on and the response is fired. When the predicate is true and the
		toggle is on, then the response is not fired. When the predicate is false
		and the toggle is true, then the toggle goes false. When the predicate is
		false and the toggle, is off, nothing happens.

		This allows the bot to speak up for an event only once. For example, if the
		bot were to say 'Time to go!' when it's 5pm every day, we'd want that to
		fire only once, and not a million times during the time between 5:00:00 and
		5:00:59.
		"""
		self.conditions[condition] = response
		return self

	def __repr__(self):
		return str(self.state)

	def pong(self, data):
		pong = "PONG " + data.split()[1] + "\r\n"
		print('Ponging with: ' + pong)
		self.irc.send(pong)

	def respond(self,channel,response,*args):
		"""
		Send a response, which may be a function returning a string or just a string
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
		"Initialize the event loop thread."
		while True:
			data = self.irc.recv(4096)
			print(data)
			if data.find("PING") != -1:
				self.pong(data)
			# Respond to messages.
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
			# Check conditions.
			for condition, response in self.conditions.iteritems():
				if condition(): 
					self.respond(channel,response,messenger)
