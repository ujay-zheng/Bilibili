from biget.vtools.headers import get_header
import requests


def get_video_message(bvid, cid):
    message_url = 'https://api.bilibili.com/x/web-interface/view'
    params = {
        'bvid': bvid,
        'cid': cid
    }
    headers = get_header('video_message', Referer='https://www.bilibili.com/video/{}'.format(bvid))
    res = requests.get(message_url, params=params, headers=headers)
    return res.json()['data']
