import shelve
import logging
import admin_commands
from admin_commands import loader, ADMIN_COMMANDS
from client import Client
# from config import bot_token
import config


def select_page(bot,user,res):
    if 'remaining' not in res:
        from random import shuffle
        l = list(range(1, config.MAX_PAGE))
        shuffle(l)
        res['remaining'] = l
    l = res['remaining']
    chosen = l.pop()
    res['remaining'] = l
    print(f'Page {chosen} choosed for user {user[:5]}')
    temp = res.get('pending', [])
    temp.append(chosen)
    res['pending'] = temp
    # return chosen
    return 543


def bad_command(bot, user, msg, res):
    keyb = config.keyb['main']
    [error, success] = bot.send_text(user, "دستور نا مفهوم", keyb)
    for admin in config.bot_admins:
        bot.send_text(admin, "Bad command: %s" % msg, config.keyb['admin'])
    return [error, success]


def process_text(bot, user, msg, res):
    if msg.startswith('/'):
        cmd = msg[1:].split()[0]
        if cmd in ADMIN_COMMANDS.keys():
            error, success = ADMIN_COMMANDS[cmd](bot, user=user, res=res, msg=msg)

    elif msg == 'اتفاقی':
        page = select_page(bot,user=user,res=res)
        error, success = send_page(bot, user, page)
    else:
        error, success = bad_command(bot, user, msg, res)
    return error, success


COMMAND_TYPES = {'START': admin_commands.start,
                 'STOP': admin_commands.stop,
                 'TEXT': process_text}


def main(bot, res):
    messages = bot.get_messages()
    for message in messages:
        type_ = message['type']
        msg = message['body'].lower().strip()
        user = message['from']
        print("New message from {} \nType: {}\nBody: {}".format(message['from'], type_, message['body']))
        if type_ in COMMAND_TYPES:
            [error, success] = COMMAND_TYPES[type_](bot=bot, user=user, msg=msg, res=res)
        else:
            bad_command(bot, user, msg, res)

        if success:
            print('Message sent successfully')
        else:
            print('Sending message failed: {}'.format(error))


def get_user_settings(user, res):
    key = f'user:{user}:settings'
    if key not in res:
        res[key] = config.default_settings
    return res[key]


def send_page(bot, user, page):
    settings = get_user_settings(user=user, res=res)
    keyb = Client.make_keyboard([[{'command': '/read %s' % page, 'text': 'خواندم'},
                                  {'command': 'return', 'text': 'منوی اصلی'}]])

    pic = f'res:pages:{page}'
    if pic in res:
        url, size = res[pic]
        [error, success] = bot.send_image(user, url, "pagr 284", size,keyboard=keyb)
    voice = f'res:voice:{settings["voice"]}:{page}'
    if voice in res:
        url, size = res[voice]
        [error, success] = bot.send_voice(user, url, "page 284", size, 16600,keyboard=keyb)
    [error, success] = bot.change_keyboard(user,keyb)
    return error, success


if __name__ == '__main__':
    try:
        bot = Client(config.bot_token)
        res = shelve.open('medias.dbm')
        print('starting bot...')
        admin_commands.bot_start_report(bot,res=res)
        main(bot, res)
    except Exception as e:
        print(e)
        logging.exception('Bad things happend!')
    finally:
        res.close()
