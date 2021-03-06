from hon.packets import ID
import re


def restart(bot, input): 
    """Reloads and reconnects, admins only""" 
    if not input.admin: return False
    bot.close()
restart.commands = ['restart']

def join(bot, input): 
    """Joins a channel, admins only""" 
    if not input.admin: return False
    bot.write_packet(ID.HON_CS_JOIN_CHANNEL,input.group(2))
    bot.config.set_add('channels',input.group(2))
    bot.reply("Joined channel: {0}".format(input.group(2)))
join.commands = ['join']

def part(bot, input): 
    """parts a channel, admins only""" 
    if not input.admin: return False
    bot.write_packet(ID.HON_CS_LEAVE_CHANNEL,input.group(2))
    bot.config.set_del('channels',input.group(2))
    bot.reply("Left channel: {0}".format(input.group(2)))
part.commands = ['part']

def ignore(bot, input): 
    """makes bot ignore user, admins only""" 
    if not input.admin: return False
    bot.config.set_add('ignore',input.group(2).lower())
    bot.reply("Ignored {0}".format(input.group(2)))
ignore.commands = ['ignore']

def unignore(bot, input): 
    """makes bot stop ignoring user, admins only""" 
    if not input.admin: return False
    bot.config.set_del('ignore',input.group(2).lower())
    bot.reply("Unignored {0}".format(input.group(2)))
unignore.commands = ['unignore']

def regen_ban_re(bot):
    bot.store.banlist_re = re.compile('({0}$)'.format('$|'.join(bot.config.banlist)))

def ban(bot, input): 
    """makes bot ban user, bot will try to reban user on each occasion""" 
    if not input.admin: return False
    nick = input.group(2).lower()
    if input.origin[0] == ID.HON_SC_CHANNEL_MSG:
        bot.write_packet(ID.HON_CS_CHANNEL_BAN,input.origin[2],nick)
    if nick in bot.config.banlist:
        bot.reply('"{0}" was already in my banlist"'.format(nick))
    else:
        bot.config.set_add('banlist',nick)
        regen_ban_re(bot)
        bot.reply('{0} added to banlist'.format(nick))
#ban.commands = ['ban']

def unban(bot, input): 
    """makes bot stop banning user, admins only""" 
    if not input.admin: return False
    nick = input.group(2).lower()
    if input.origin[0] == ID.HON_SC_CHANNEL_MSG:
        bot.write_packet(ID.HON_CS_CHANNEL_UNBAN,input.origin[2],nick)
    if nick in bot.config.banlist:
        bot.config.set_del('banlist',nick)
        regen_ban_re(bot)
        bot.reply('{0} removed from banlist'.format(nick))
    else:
        bot.reply('Sorry, there was no "{0}" in my banlist"'.format(nick))
#unban.commands = ['unban']

def admin(bot, input): 
    """Adds person to admin list, owner only""" 
    if not input.owner: return False
    bot.config.set_add('admins',input.group(2).lower())
    bot.reply("Admin'd {0}".format(input.group(2)))
admin.commands = ['admin']

def unadmin(bot, input): 
    """Removes person from admins list, owner only""" 
    if not input.owner: return False
    bot.config.set_del('admins',input.group(2).lower())
    bot.reply("Unadmin'd {0}".format(input.group(2)))
unadmin.commands = ['unadmin']

def setup(bot):
    regen_ban_re(bot)

def query(bot, input):
    """Master server query"""
    if not input.owner: return False
    query = {'nickname' : input.group(2)}
    query['f'] = 'show_stats'
    query['table'] = 'player'
    data = bot.masterserver_request(query,cookie=True)
    print(data)
    bot.reply("Printed to stdout")
query.commands = ['query']

try:
    test = _eval
except:
    _eval = eval

def eval(bot, input):
    """Top Secret"""
    if not input.owner: return False
    send = str( _eval( input.group(2) ) )
    print(send)
    bot.reply(send)
eval.commands = ['eval']

def pprint(bot, input):
    """Top Secret"""
    if not input.owner: return False
    print( _eval( input.group(2) ) )
pprint.commands = ['print']