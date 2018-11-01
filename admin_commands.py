import os

import config
from config import bot_admins


def start(bot, user, msg, res):
    setup_user(bot, user, res)
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
                 mogrify -gravity Center -crop 625x920+0+0 *.jpg
    voice 1  & translate: http://andishehonline.ir/tag/%D8%AA%D8%B1%D8%AC%D9%85%D9%87-%D8%B5%D9%88%D8%AA%DB%8C-%D9%82%D8%B1%D8%A2%D9%86-%D8%A8%D9%87-%D8%B5%D9%88%D8%B1%D8%AA-%D8%B5%D9%81%D8%AD%D9%87-%D8%A8%D9%87-%D8%B5%D9%81%D8%AD%D9%87/
            mediainfo --output="General;%FileName%.%FileExtension%,%Duration%\r\n" *.mp3 > duration.txt
    voice 2: http://www.quranhefz.ir/download/view-6186.aspx
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
        duraion_file = os.path.join(dirpath, 'duration.txt')
        duration = dict()
        if os.path.exists(duraion_file):
            bot.send_text(user, '\n Duration file exists,')
            with open(duraion_file) as f:
                duration = {i.split(',')[0]: int(i.split(',')[1].strip()) for i in f.readlines() if i.strip()}

        print('\n Loading %s Total: %d' % (dirpath, len(files)), end='')
        for name in files:
            if config.DEBUG:
                t = name.split('.')[0]
                if t.isdigit() and (int(t) > config.DEBUG_PAGE or int(t) < 1):
                    continue

            file = os.path.join(dirpath, name)
            key = file.lower().replace('/', ':')[:-4]
            if key not in res:
                size = os.path.getsize(file)
                print('uploading ', key, size / 1024.0)
                [error, url] = bot.upload_file(file)
                if 'voice' in key:
                    res[key] = (url, size, duration.get(name, 0))
                else:
                    res[key] = (url, size)
                total += 1
            print('.', end='')
    res.sync()
    bot.send_text(user, "Done total %d files loaded." % total)
    return False, True


def restart(bot, **kwargs):
    for user in bot_admins:
        bot.send_text(user, "Restart requested")


def bot_start_report(bot, **kwargs):
    for user in bot_admins:
        bot.send_text(user, 'Bot started')
        total = len(kwargs['res'].get('remaining', []))
        bot.send_text(user, f'Total page remains {total}')


def read(bot, **kwargs):
    user = kwargs['user']
    return bot.send_text(user, "متشکرم", keyboard=config.keyb['main'])


def setup_user(bot, user, res, **kwargs):
    res[f'user:{user}:settings'] = config.default_settings
    res[f'user:{user}:page_count'] = 0
    return


def force_reload(bot, user, res, **kwargs):
    for i in res.keys():
        if i.startswith('res'):
            del res[i]
    return loader(bot, user=user, res=res, **kwargs)


ADMIN_COMMANDS = {'force_reload': force_reload,
                  'load': loader,
                  'sysrestart': restart,
                  'read': read,
                  'restart': setup_user}
