
from botinator import botinator

def state_changer(matches, messenger, state):
	state['mood'] = state['mood'] + 1
	return str(messenger) + ': woooot' + str(matches)

chan = '#jayparty'
bot = botinator.Bot('irc.freenode.net')
bot.nick('bottymcbotterson')
bot.user_and_ircname('bot', 'Winston Churchill')
bot.join(chan)

bot.state['mood'] = 0

bot.listen('hello bot *', 'well hi there')
bot.listen('hello *', 'well hey there')

bot.cron((None, 10, None, None, None), 'hey sup', chan)

bot.listen('change state', state_changer)

bot.live()
