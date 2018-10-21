from os.path import getsize
from sys import path
from client import Client
from config import bot_token

bot = Client(bot_token)


def start(user):
    print('in stop')
    keyb = bot.make_keyboard("اتفاقی|جزء خاص")
    return bot.send_text(user, 'سلام این راهنمای کاربری است', keyb)


def stop(user):
    print('in stop')
    keyb = bot.make_keyboard("اتفاقی|جزء خاص")
    return bot.send_text(user, 'سلام این راهنمای کاربری است', keyb)


def main():
    messages = bot.get_messages()
    for message in messages:
        type_ = message['type']
        msg = message['body']
        user = message['from']
        print("New message from {} \nType: {}\nBody: {}".format(message['from'], type_, message['body']))

        if type_ == 'START':
            [error, success] = start(message['from'])
        elif type_ == 'STOP':
            [error, success] == stop(message['from'])
        elif type_ == 'TEXT':
            if msg == 'اتفاقی':
                pic = 'res/pages/283.jpg'
                # [error,url] = bot.upload_file(pic)
                url = 'oyWe4P1rgcpdzNkdYjG5zhPgihIKBc_aA-_jmYJUO6lP9V0YfoFouhGEkhj7EK3a6CpwB9PC2UIhW_T5jLm-wFoZXuH6bJUWC_rXH8id25bHZxW3b4Z9JZHvEFG6wd5epCLRBYedQDBpkR877EaHvi3zbNZ6VeC2kK_hGsHPyVNCG9tH6h_ppg-ibNxbwhCVSP4m9hRBnonK0V0nPsH3W9FBYwPaksDiVbK1dwKB4ZEl4EY7LbnTLbEAav8wuGjdadaaUg86CEr-eBZIZCrrEq1b2nOHkppo3cQ6wTwfoQrboOzXNEsT5hw-nzFiPzB7GH5iUwsR8kdBg21NqGy80tU9QdOo9SrlhQZUcSwQslfwJrtkxKo4dxgA_0nTSF70m6B3SA7e8OjFR12GQ53eIxGTqWrhPdxwSzupaMm0r5Va4Cv2MPgTNfhOxjFNfxuJ-jEZAQ6gR_EHEOdYcrgybYvIe0fQ8U-kKMR1eL0NtB5MLcXnaoSyV7obRfk'
                [error, success] = bot.send_image(user, url, "pagr 284", getsize(pic))
                voice = 'res/voice/542.mp3'
                # [error,url] = bot.upload_file(voice)
                url='5l0XAX7qY7eLpNkXG-RIA0k_Z121GTOggFPayF5YgqDQ1BsXaLiCEUsGDHcJQGKw7pcigam0gm3qG7R063O7xONrSkL0c1zPUwhaFN2BTaJSYA2QtbSG9nUDgNuAIlloaTBBJrmHxj7FEv-0kpLQZkmphsywNEjsbgWVBZkCFRspT3eSMLp_Bm3qPPDdGn--xNZuBqRvQzwsAon7Bem-2lyJHcFFscoYIzSE4dqZNg0YzNr4oIapfc_jGW7ivwfjbFV71gMft137cF0l_Nnav08-aiMdHwY4C_s8T_-yxditL8lF9IcOFAThsHx_2-lpCDHOpjMnG4__Rc0ginV2ddgU4SezAUzdBH2PGOQzw1D98II-a7exPVA7lmtE7WOyG9vYH7d8zYLpxE3DMUufl_9Up6-vsIWEEeYwC08PV5GX5trBI4ByzI12jwgYb9Lcuy-0oVdtmECYIA_1QzBsy4UCLA914SZcyst3j-40G-QlXsTG9RH0bkztIns'
                print(url)
                [error, success] = bot.send_voice(user, url, "page 284", getsize(voice),16600)

            else:
                [error, success] = bot.send_text(user,"دستور نا مفهوم")

        if success:
            print('Message sent successfully')
        else:
            print('Sending message failed: {}'.format(error))


if __name__ == '__main__':
    print('starting bot...')
    main()
