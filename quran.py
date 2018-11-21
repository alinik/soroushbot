import logging
from random import shuffle

import admin_commands
import config
from admin_commands import ADMIN_COMMANDS
from utils import ignore_exception


@ignore_exception
def restart_reading(bot, res):
    all_list = list(range(1, config.MAX_PAGE))
    shuffle(all_list)
    res['remaining'] = all_list
    res['finished'] = res.get('finished', 0) + 1
    admin_commands.send_to_admin(f'one cycle finished,\n Total:{res["finished"]}. Restarting')


def select_page(bot, user, res):
    if 'remaining' not in res:
        restart_reading(bot, res)
    remainings = res['remaining']
    if len(remainings) == 0:
        restart_reading(bot, res)
        remainings = res['remaining']
    chosen = remainings.pop()
    res['remaining'] = remainings
    logging.info(f'Page {chosen} choosed for user {user[:5]}')
    res[f'user:{user}:page_count'] = res.get(f'user:{user}:page_count', 0) + 1
    return chosen


@ignore_exception
def bad_command(bot, user, msg, res):
    keyb = config.keyb['main']
    [error, success] = bot.send_text(user, "دستور نا مفهوم", keyb)
    logging.warning(f"bad command: {msg}")
    for admin in config.bot_admins:
        bot.send_text(admin, "Bad command: %s" % msg, config.keyb['admin'])
    return [error, success]


@ignore_exception
def user_report(bot, user, res, **kwargs):
    finished = res['finished']
    remainings = len(res['remaining'])
    report = "تعداد صفحات خوانده شده توسط شما: %s" % res[f'user:{user}:page_count']
    report += f'\n تا کنون بوسیله این بات {finished} بار ختم صورت گرفته است.'
    report += f'\nاز ختم جاری {remainings} صفحه باقی مانده است.'
    return bot.send_text(user, report,config.keyb['main'])


@ignore_exception
def process_text(bot, user, msg, res):
    if msg.startswith('/'):
        cmd = msg[1:].split()[0]
        if cmd in ADMIN_COMMANDS.keys():
            error, success = ADMIN_COMMANDS[cmd](bot, user=user, res=res, msg=msg)
        else:
            if cmd == 'ghari':
                error, success = send_voice(bot, user, res, msg)

    elif msg == 'صفحه جدید':
        page = select_page(bot, user=user, res=res)
        error, success = send_page(bot, user, page,res)
    elif msg == 'گزارشات':
        error, success = user_report(bot, user, res)
    elif msg == 'return':
        error, success = bot.send_text(user, 'بازگشت به منو اصلی', config.keyb['main'])
    else:
        error, success = bad_command(bot, user, msg, res)
    return error, success


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


@ignore_exception
def send_page(bot, user, page,res):
    keyb = make_ghari_keyb(page)
    pic = f'res:pages:{page:03}'
    url, size = res[pic]
    [error, success] = bot.send_image(user, url, "", size, keyboard=keyb)
    [error, success] = bot.change_keyboard(user, keyb)

    return error, success


@ignore_exception
def send_voice(bot, user, res, msg, **kwargs):
    error, success = False, True
    cmd, voice, page = msg.split()
    voice = f'res:voice:{voice}:{page}'
    url, size, duration = res[voice]
    [error, success] = bot.send_voice(user, url, "", size, duration)
    return [error, success]


def start_bot(bot, res):
    while True:
        try:
            messages = bot.get_messages()
            for message in messages:
                type_ = message['type']
                msg = message['body'].lower().strip()
                user = message['from']
                logging.info(f"New message from {message['from'][:10]} : {type_}:{message['body']}")
                if type_ in COMMAND_TYPES:
                    [error, success] = COMMAND_TYPES[type_](bot=bot, user=user, msg=msg, res=res)
                else:
                    [error, success] = bad_command(bot, user, msg, res)

                if success:
                    logging.debug('Message sent successfully')
                else:
                    logging.warning('Sending message failed: {}'.format(error))
        except Exception as e:
            if bot:
                for admin in config.bot_admins:
                    bot.send_text(admin, 'Exception Happened:\n' + str(e))


COMMAND_TYPES = {'START': admin_commands.start,
                 'STOP': admin_commands.stop,
                 'TEXT': process_text}

