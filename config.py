from soroush_python_sdk import Client

bot_token = "jj5nH1BoZJsbHplz2v8DkiUHZv8o-uCn4c6AHJIxYP-OY_kNt63W0qHl6Wph7HhNzkVGXQ6x4IM9YFcWmMdEtf-uBRvnsZF97w78T" \
            "8GpG0Bv7SVLIv1FwM-uMKCGv2PBMfBb7flzBMvtlCZ1"

user = {'ali': 'NFiDxo8BngUgqnBRPKVqR8jwCqH-38zxDOeDDy_f7bUCOLgHJkJZJJIU75U'}
bot_admins = ('NFiDxo8BngUgqnBRPKVqR8jwCqH-38zxDOeDDy_f7bUCOLgHJkJZJJIU75U',)

keyb = {'main': Client.make_keyboard("اتفاقی|گزارشات|تنظیمات"),
        'admin': Client.make_keyboard("/reload|/restart|/load")}

default_settings = {'voice': 'parhizgar',
                    'reminder': 60 * 60}
MAX_PAGE = 604