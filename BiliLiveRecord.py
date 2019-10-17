# 请使用Python3

from urllib import request
from urllib.error import HTTPError
import json
import time

roomno = input('https://live.bilibili.com/') # 也可以直接改成固定直播间
url = 'https://live.bilibili.com/' + roomno
header = [
    ('User-Agent' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'),
    ('Accept' , '*/*'),
    ('Cookie' , "这里填你在live.bilibili.com的Cookie，不要忘记httponly的") # 不填就只有高清可以录
]
handler = request.HTTPHandler()
opener = request.build_opener(handler)
opener.addheaders = header
request.install_opener(opener)

while True:
    try:
        html = request.urlopen(url).read().decode('utf-8')
    except HTTPError:
        continue
    j = '{' + html.split('window.__NEPTUNE_IS_MY_WAIFU__={')[1].split('</script>')[0]
    room = json.loads(j)
    if room['roomInitRes']['data']['live_status'] == 1:
        liveurl = room['playUrlRes']['data']['durl'][0]['url'] # 0大概就是主线？
        #print(liveurl)
        filename = roomno + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.flv'
        print('Recording to file ' + filename)
        try:
            request.urlretrieve(liveurl, filename=filename)
            print('Done')
        except HTTPError:
            print('Failed, try again') # 偶尔会HTTP 475报错，不知道为啥
    else:
        time.sleep(1) # 直播状态检测间隔，默认1秒