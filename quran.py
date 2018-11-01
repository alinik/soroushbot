import logging
import shelve

from soroush_python_sdk import Client

import admin_commands
import config
from admin_commands import ADMIN_COMMANDS

from random import shuffle


def restart_reading(bot, res):
    l = list(range(1, config.MAX_PAGE))
    shuffle(l)
    res['remaining'] = l
    res['finished'] = res.get('finished', 0) + 1
    for admin in config.bot_admins:
        bot.send_text(admin, f'one cycle finished,\n Total:{res["finished"]}. Restarting')


def select_page(bot, user, res):
    if 'remaining' not in res:
        restart_reading(bot, res)
    l = res['remaining']
    if len(l) == 0:
        restart_reading(bot, res)
        l = res['remaining']
    chosen = l.pop()
    res['remaining'] = l
    print(f'Page {chosen} choosed for user {user[:5]}')
    res[f'user:{user}:page_count'] = res.get(f'user:{user}:page_count', 0) + 1
    # temp = res.get('pending', [])
    # temp.append(chosen)
    # res['pending'] = temp
    return chosen
    # return 543


def bad_command(bot, user, msg, res):
    keyb = config.keyb['main']
    [error, success] = bot.send_text(user, "دستور نا مفهوم", keyb)
    for admin in config.bot_admins:
        bot.send_text(admin, "Bad command: %s" % msg, config.keyb['admin'])
    return [error, success]


def user_report(bot, user, res, **kwargs):
    return bot.send_text(user, "تعداد صفحات خوانده شده: %s" % res[f'user:{user}:page_count'])


def user_change_ghari(bot, user, res):
    settings = res[f'user:{user}:settings']
    next_ghari = settings['voice'] + 1
    if next_ghari not in config.VOICE_KEYS:
        next_ghari = 1
    settings['voice'] = next_ghari
    res[f'user:{user}:settings'] = settings
    return bot.send_text(user, f'قاری به {config.VOICE_KEYS[next_ghari]} تغییر کرد.')


def process_text(bot, user, msg, res):
    if msg.startswith('/'):
        cmd = msg[1:].split()[0]
        if cmd in ADMIN_COMMANDS.keys():
            error, success = ADMIN_COMMANDS[cmd](bot, user=user, res=res, msg=msg)
        else:
            if cmd == 'ghari':
                error, success = send_voice(bot, user, res, msg)

    elif msg == 'اتفاقی':
        page = select_page(bot, user=user, res=res)
        error, success = send_page(bot, user, page)
    elif msg == 'گزارشات':
        error, success = user_report(bot, user, res)
    elif msg == 'تغییر قاری':
        error, success = user_change_ghari(bot, user, res)
    elif msg == 'return':
        error, success = bot.send_text(user, 'بازگشت به منو اصلی', config.keyb['main'])
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


def make_ghari_keyb(page):
    keyb = [
        [
            dict(command=f'/ghari 1 {page:03}', text=f'ترتیل استاد {config.VOICE_KEYS[1]}'),
            dict(command=f'/ghari 2 {page:03}', text=f'ترتیل استاد {config.VOICE_KEYS[2]}'),
            dict(command=f'/ghari 0 {page:03}', text='ترجمه صوتی صفحه'), ],
        [
            {'command': f'/read {page:03}', 'text': 'خواندم'},
            {'command': 'return', 'text': 'منوی اصلی'}]
    ]
    return keyb


def send_page(bot, user, page):
    settings = get_user_settings(user=user, res=res)
    # keyb = Client.make_keyboard([[{'command': '/read %s' % page, 'text': 'خواندم'}, {'command': 'return', 'text': 'منوی اصلی'}]])
    keyb = make_ghari_keyb(page)
    pic = f'res:pages:{page:03}'
    if pic in res:
        url, size = res[pic]
        [error, success] = bot.send_image(user, url, "", size, keyboard=keyb)
    [error, success] = bot.change_keyboard(user, keyb)

    return error, success


def send_voice(bot, user, res, msg, **kwargs):
    cmd, voice, page = msg.split()
    # keyb = config.keyb['main']
    voice = f'res:voice:{voice}:{page}'
    if voice in res:
        url, size, duration = res[voice]
        [error, success] = bot.send_voice(user, url, "", size, duration)
        # [error, success] = bot.change_keyboard(user, keyb)
    return [error, success]


if __name__ == '__main__':
    try:
        bot = Client(config.bot_token)
        res = shelve.open('medias.dbm')
        print('starting bot...')
        admin_commands.bot_start_report(bot, res=res)
        main(bot, res)
    except Exception as e:
        print(e)
        logging.exception('Bad things happend!')
        try:
            for admin in config.bot_admins:
                bot.send_text(admin, str(e))
        except Exception:
            pass
    finally:
        res.close()
