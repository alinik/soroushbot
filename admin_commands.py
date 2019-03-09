import os
import time

import config
from config import bot_admins


def start(bot, user, msg, res):
    setup_user(bot, user, res)
    send_to_admin(bot, "New User start_bot!")
    mesg = """🔸راهنما:
    با لمس کلید «صفحه جدید»، یک صفحه از قرآن به شما تحویل می شود.
    ◽با کلیدهای بعدی شما میتوانید قرائت ترتیل با صدای دو قاری و همچنین ترجمه صوتی همان صفحه را هم به راحتی دانلود و استفاده نمائید.
    ◽لطفاً بعد از قرائت هر صفحه کلید «خواندم» را لمس کنید تا جمع صفحات خوانده شده محاسبه شود.
    **************
    🔶 این کار هدیه ای از گروه فرنا می‌باشد. لطفا در کانال ما به آدرس زیر عضو شوید:
    التماس دعا
    @quran_farna◽"""
    return bot.send_text(user, mesg, config.keyb['main'])


def stop(bot, user, msg, res):
    user_list = res.get('user_list', set())
    if user in user_list:
        user_list.remove(user)
        res['user_list'] = user_list
    send_to_admin(bot, "A User stop!")
    return False, True


def send_to_admin(bot, message):
    for admin in bot_admins:
        bot.send_text(admin, message)


def loader(bot, **kwargs):
    """
    Pics from: https://www.searchtruth.org/quran/images9/0008.jpg
                 mogrify -gravity Center -crop 625x920+0+0 *.jpg
    voice 1  & translate: http://andishehonline.ir/tag/%D8%AA%D8%B1%D8%AC%D9%85%D9%87-%D8%B5%D9%88%D8%AA%DB%8C-%D9%82%D8%B1%D8%A2%D9%86-%D8%A8%D9%87-%D8%B5%D9%88%D8%B1%D8%AA-%D8%B5%D9%81%D8%AD%D9%87-%D8%A8%D9%87-%D8%B5%D9%81%D8%AD%D9%87/
            mediainfo --output="General;%FileName%.%FileExtension%,%Duration%\r\n" *.mp3 > duration.txt
    voice 2: http://www.quranhefz.ir/download/view-6186.aspx

    pics 2: http://moshaf.org/news/10218
        agi poppler-utils
        pdftoppm 0.pdf 0 -l 1 -jpeg
        mogrify -gravity Center -crop 750x1310+25+20 0-01.jpg
    :param bot:
    :param kwargs:
    :return:
    """

    user = kwargs['user']
    res = kwargs['res']
    topdir = 'res/'
    total, failed = 0, 0
    for dirpath, dirnames, files in os.walk(topdir):
        bot.send_text(user, '\n Loading %s Total: %d' % (dirpath, len(files)))
        duraion_file = os.path.join(dirpath, 'duration.txt')
        duration = dict()
        if os.path.exists(duraion_file):
            bot.send_text(user, '\n Duration file exists,')
            with open(duraion_file) as f:
                duration = {i.split(',')[0]: int(i.split(',')[1].strip()) for i in f.readlines() if i.strip()}

        print('\n Loading %s Total: %d' % (dirpath, len(files)), end='')
        delay = 1
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
                if error or not url:
                    print(f'upload failed for {key}[{error}]')
                    failed += 1
                    time.sleep(1 + delay)
                    delay = delay * 2 % 100
                    continue
                delay = 1
                if 'voice' in key:
                    res[key] = (url, size, duration.get(name, 120_000))
                else:
                    res[key] = (url, size)
                total += 1
            print('.', end='')
    res.sync()
    bot.send_text(user, f"Done total {total} files loaded, {failed} failed.")
    return False, True


def restart(bot, **kwargs):
    send_to_admin(bot, "Restart requested")


def bot_start_report(bot, **kwargs):
    from quran import user_report
    res = kwargs['res']
    for user in bot_admins:
        user_report(bot, user, res)
        bot.send_text(user, f'total User: {len(res.get("users:list", []))}')


def read(bot, **kwargs):
    user = kwargs['user']
    return bot.send_text(user, "قبول باشه انشاالله", keyboard=config.keyb['main'])


def setup_user(bot, user, res, **kwargs):
    user_list = res.get('users:list', set())
    user_list.add(user)
    res['users:list'] = user_list
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
