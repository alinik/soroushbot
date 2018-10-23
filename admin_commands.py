import os

import config
from config import bot_admins


def start(bot, user, msg, res):
    for admin in bot_admins:
        bot.send_text(admin, "New User start!")
    keyb = bot.make_keyboard("اتفاقی|گزارشات|تنظیمات")
    return bot.send_text(user, 'سلام این راهنمای کاربری است', keyb)


def stop(bot, user, msg, res):
    for admin in bot_admins:
        bot.send_text(admin, "New User start!")
    return None


def loader(bot, **kwargs):
    """
    Pics from: https://www.searchtruth.org/quran/images9/0008.jpg
    :param bot:
    :param kwargs:
    :return:
    """

    user = kwargs['user']
    res = kwargs['res']
    topdir = 'res/'
    total = 0
    for dirpath, dirnames, files in os.walk(topdir):
        bot.send_text(user, '\n Loading %s Total: %d' % (dirpath, len(files)))
        print('\n Loading %s Total: %d' % (dirpath, len(files)), end='')
        for name in files:
            file = os.path.join(dirpath, name)
            key = file.lower().replace('/', ':')[:-4]
            if key not in res:
                [error, url] = bot.upload_file(file)
                size = os.path.getsize(file)
                res[key] = (url, size)
                total += 1
            print('.', end='')
    res.sync()
    bot.send_text(user, "Done total %d files loaded." % total)
    return total


def restart(bot, **kwargs):
    for user in bot_admins:
        bot.send_text(user, "Restart requested")


def bot_start_report(bot, **kwargs):
    for user in bot_admins:
        bot.send_text(user, 'Bot started')
        total = len(kwargs['res'].get('remaining', -1))
        bot.send_text(user, f'Total page remains {total}')


def read(bot, **kwargs):
    user = kwargs['user']
    return bot.send_text(user, "متشکرم", keyboard=config.keyb['main'])


ADMIN_COMMANDS = {'load': loader,
                  'restart': restart,
                  'read': read}
