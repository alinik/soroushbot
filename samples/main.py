import datetime
import json
from time import sleep
from urllib3.exceptions import InsecureRequestWarning
import requests as r

r.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = "https://bot.soroush-hamrah.ir/jj5nH1BoZJsbHplz2v8DkiUHZv8o-uCn4c6AHJIxYP-OY_kNt63W0qHl6Wph7HhNzkVGXQ6x4IM9YFcWm" \
      "MdEtf-uBRvnsZF97w78T8GpG0Bv7SVLIv1FwM-uMKCGv2PBMfBb7flzBMvtlCZ1/"
params = {'verify': False, 'headers': {'content-type': 'application/stream+json', 'accept': 'application/stream+json'}}
url_get = url + 'getMessage'
url_send = url + 'sendMessage'


def parse(data):
    data_lines = data.replace('\n\n', '\n').splitlines()
    data_json = [json.loads(x[5:]) for x in data_lines if x.startswith('data:')]
    return data_json


# r.get(url)
def test_conn():
    while True:
        resp = r.get(url_get, **params)
        result = parse(resp.text)
        for item in result:
            print('responding ', datetime.datetime.fromtimestamp(int(item['time']) // 1000), item['from'][:8], 'text:',
                  item['body'], 'type', item['type'], end='')
            reply(item['from'], 'Hi back')


def test_stream():
    req = r.get(url_get, stream=True,timeout=1000, **params)
    while True:
        raw = req.raw.read().decode()
        if raw == '':
            sleep(.1)
            continue
        p = parse(raw)
        print('raw:', raw)
        for item in p:
            reply(item['from'], 'hi back')


def test_stream2():
    req = r.get(url_get, stream=True,timeout=1000, **params)
    for i in req.iter_lines():
        if i == b'': continue
        print(i)
        item = parse(i.decode())[0]
        print('responding ', datetime.datetime.utcfromtimestamp(int(item['time']) // 1000), item['from'][:8], 'text:',
              item['body'], 'type', item['type'], end='')
        reply(item['from'], 'hi back 2')


def reply(to, body):
    data = dict(to=to, body=body, type='TEXT')
    resp = r.post(url_send, json=json.dumps(data), **params)
    print(resp.text)


if __name__ == '__main__':
    # test_conn()
    # test_stream()
    test_stream2()

