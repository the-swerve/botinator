
# Botinator

## Super declarative IRC bot API

## Install

  pip install botinator 

## Create your bot

Set up server, port, nick, username, ircname, and channel.

	from botinator import botinator
	bot = botinator.Bot('irc.freenode.net')
	bot.nick('bottymcbotterson')
	bot.user_and_ircname('bot', 'Winston Churchill')
	bot.join('#botparty')

## Basic behavior:

Bind a pattern to a response:

	bot.listen('hello bot', 'well hi there')
	bot.listen('do you like cheese?', 'decidedly so')

The pattern can be a regex:

	bot.listen(r'[(hello)|(hi)|(hey)]', 'well hi there')

## More complex behavior:

Instead of responding with a string, botinator can respond with a callback
function that allows more complex behavior.

The callback function looks like:

	def callback(matches, messenger, state):
		return response

Matches are the regex matches that the bot made, the messenger is the sender of
the matched message, and the state is a modifiable dictionary that can store
any ongoing data for the bot.

For example, a simple time printing callback:

	def get_time(matches, messenger, state):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

	bot.listen('hey bot!: wat time', get_time)

The 'matches' parameter passed into your callback functions will be a list of successfuly matched strings from your regex.

	bot.listen(r'yo bot: (\d+) \+ (\d+)', add_yr_numbers)

	def add_yr_numbers(matches, messenger):
		try:
			left = int(matches[0])
			right = int(matches[1])
			return str(left + right)
		except: return 'wat'

Exceptions in your callback functions won't kill your bot if you don't catch em, but will just be printed. She's a toughy.

## Time-based messages (cron party)

The bot has cron-like functionality using the cron() method. The cron() method is structured like:

  cron((minute, hour, date, month, weekday), response, channel)

It'll run at times that match the tuple similar to cron. Use None for '*'. For example:

	bot.cron((20, 16, None, None, None), '420!', chan)

The bot will announce '420!' once everyday at 4:20pm

## Start your bot when you're done binding listeners

	bot.live()

### todo

* Testing.

### ideas

* It'd be cool if it were FIFO filesystem-based, like the 'ii' IRC client.
* It'd be cool if it backgrounded and had a CLI for starting/stopping/status checks 
