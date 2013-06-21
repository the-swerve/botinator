
import botinator

chan = '#jayparty'
bot = botinator.Bot('irc.freenode.net')
bot.nick('bottymcbotterson')
bot.user_and_ircname('bot', 'Winston Churchill')
bot.join(chan)

bot.listen('hello bot *', 'well hi there')
bot.listen('hello *', 'well hey there')

bot.cron((None, 10, None, None, None), 'hey sup', chan)

bot.live()
