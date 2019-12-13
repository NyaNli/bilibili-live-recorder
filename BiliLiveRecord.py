# 请使用Python3

from urllib import request
from urllib.error import HTTPError
import json
import time

roomno = input('https://live.bilibili.com/') # 也可以直接改成固定直播间
url = 'https://live.bilibili.com/' + roomno
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
        html = request.urlopen(url).read().decode('utf-8')
    except HTTPError:
        continue
    j = '{' + html.split('window.__NEPTUNE_IS_MY_WAIFU__={')[1].split('</script>')[0]
    room = json.loads(j)
    if room['roomInitRes']['data']['live_status'] == 1: # 没判断加密码什么的，因为暂时也没遇到
        roomid = room['roomInitRes']['data']['room_id']
        qn = 10000 # 不填platform参数原画是4，platform参数填web原画就是10000，以防万一还是先确认一下
        qualities = room['roomInitRes']['data']['play_url']['quality_description']
        for q in qualities:
            if q['desc'] == '原画':
                qn = q['qn']
                break
        try: # 原画画质未必存在html里，要重新获取url了
            playUrl = json.loads(request.urlopen('https://api.live.bilibili.com/room/v1/Room/playUrl?cid=' + str(roomid) + '&qn=' + str(qn) + '&platform=web').read().decode('utf-8'))
            if playUrl['code'] != 0:
                print('Get live stream urls failed: ' + playUrl['message'])
                continue
        except HTTPError:
            continue
        liveurl = playUrl['data']['durl'][0]['url'] # 0大概就是主线？
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
