
# ~~~~BOTINATOR~~~~

## Super easy irc bot api

## Create your bot:

Pass server, port, nick, username, ircname, and channel.

	from botinator import *
	bot = Bot('irc.freenode.net','6667', 'imabot', 'bot', 'Winston Churchill', '#your_awesome_channel')

## Basic behavior:
Bind a pattern to a response:

	bot.bind('hello bot', 'well hi there')
	bot.bind('do you like cheese?', 'decidedly so')

The pattern can be a regex:

	bot.bind(r.'[(hello)|(hi)|(hey)]', 'well hi there')

Regex syntax: http://docs.python.org/2/library/re.html#regular-expression-syntax

## More complex behavior:
Map your regexes to callback functions that take the matched strings
from your regex and return an irc command.

	def get_time(matches, messenger):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

	bot.bind('wat time', get_time)

The 'matches' parameter passed into your callback functions will be a list of successfuly matched strings from your regex.

	bot.bind(r'yo bot: \d+ \+ \d+' : add_yr_numbers)

	def add_yr_numbers(matches, messenger):
		try:
			left = int(matches[0])
			right = int(matches[1])
			return str(left + right)
		except: return 'wat'

You must also declare the 'messenger' for your callback functions, which is just the message author's name.

Exceptions in your callback functions won't kill your bot if you don't catch em, but will just be printed. He's a toughy.

## Event responses

Sometimes you want behavior that's not based on messages. You can bind a
predicate function to a specific response:

	def is_420: return time.strftime("%I%M") == "0420"
	bot.when(is_420,'420')

## Supports chaining

	bot.when(something,'say something').bind(r'(.*) pie(\.*)',eat_pie).when(happy,clap)

## Start your bot when you're done binding stuff

	bot.live()

### todo

* Extract channel and then respond to that specific channel
* Extract messenger name and pass to response function
* Dynamically update bot while running event loop?
