from soroush_python_sdk import Client

DEBUG = False
DEBUG_PAGE = 10
bot_token = "jj5nH1BoZJsbHplz2v8DkiUHZv8o-uCn4c6AHJIxYP-OY_kNt63W0qHl6Wph7HhNzkVGXQ6x4IM9YFcWmMdEtf-uBRvnsZF97w78T" \
            "8GpG0Bv7SVLIv1FwM-uMKCGv2PBMfBb7flzBMvtlCZ1"

user = {'ali': 'NFiDxo8BngUgqnBRPKVqR8jwCqH-38zxDOeDDy_f7bUCOLgHJkJZJJIU75U'}
bot_admins = ('NFiDxo8BngUgqnBRPKVqR8jwCqH-38zxDOeDDy_f7bUCOLgHJkJZJJIU75U',)
# '7UhksfDFWrRkKaczg4Y3Wwho4rHNyzUQAenY9a4F5ZCdPJpUKjzMQ1WRerY', #ghodrati
# }
keyb = {'main': Client.make_keyboard("صفحه جدید|گزارشات"),
        'admin': Client.make_keyboard("/reload|/restart|/load")}

VOICE_KEYS={1: 'سعد قامدی', 2: 'پرهیزگار'}
default_settings = {'voice': 1, 'reminder': 60 * 60}
MAX_PAGE = 604 if not DEBUG else DEBUG_PAGE
SEJDEH = (528, 597, 480, 416)
