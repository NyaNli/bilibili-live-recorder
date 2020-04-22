# 请使用Python3

from urllib import request
from urllib.error import HTTPError
import json
import time

roomno = input('https://live.bilibili.com/') # 也可以直接改成固定直播间
header = [
    ('User-Agent' , 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'),
    ('Accept' , '*/*')
    # 好像不再需要登录了
]
handler = request.HTTPHandler()
opener = request.build_opener(handler)
opener.addheaders = header
request.install_opener(opener)

while True:
    try:
        roominfo = request.urlopen('https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id=' + roomno).read().decode('utf-8')
    except HTTPError:
        continue
    roominfo = json.loads(roominfo)
    if roominfo['code'] != 0:
        print(roominfo['message']) # 加密码会在这里提示，加了密码一般是不想被录制的
        time.sleep(1)
        continue
    roomid = roominfo['data']['room_info']['room_id']
    if roominfo['data']['room_info']['live_status'] == 1:
        try:
            playUrl = json.loads(request.urlopen('https://api.live.bilibili.com/room/v1/Room/playUrl?cid=' + str(roomid) + '&qn=4').read().decode('utf-8'))
            if playUrl['code'] != 0:
                print('Get live stream urls failed: ' + playUrl['message'])
                continue
        except HTTPError:
            continue
        liveurl = playUrl['data']['durl'][0]['url'] # 0大概就是主线？这里可以优化一下出错自动换一下线
        #print(liveurl)
        filename = roomno + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.flv'
        print('Recording to file ' + filename)
        try:
            request.urlretrieve(liveurl, filename=filename)
            print('Done')
        except HTTPError:
            print('Failed, try again') # 偶尔会HTTP 475报错，应该是为了防止盗播
    else:
        time.sleep(1) # 直播状态检测间隔，默认1秒
