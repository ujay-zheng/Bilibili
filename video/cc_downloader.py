import requests
from error.cc_exception import WithoutCCWarning
from utils.cc_tool import json2srt
from video.config import get_header
import warnings


class CCDownloader:
    def __init__(self, aid, cid, page):
        self.aid = aid
        self.cid = cid
        self.page = page
        self.av_url = 'https://www.bilibili.com/video/av{}'.format(aid)
        cc_message = self._get_cc_message()
        self.allow_subtitle, self.subtitle_list = cc_message['allow_submit'], cc_message['list']

    def _get_cc_message(self):
        message_url = 'https://api.bilibili.com/x/web-interface/view'
        params = {
            'aid': self.aid,
            'cid': self.cid
        }
        headers = get_header('cc_message', Referer=self.av_url)
        res = requests.get(message_url, params=params, headers=headers)
        return res.json()['data']['subtitle']

    def _get_resource(self, cc_url):
        headers = get_header('cc_resource', Referer="{}?p={}".format(self.av_url, self.page))
        res = requests.get(url=cc_url, headers=headers)
        return res.json()['body']

    def _download_single(self, cc_url, output):
        with open(output, "w", encoding='utf-8') as f:
            f.write(json2srt(self._get_resource(cc_url)))
        return output

    def download(self, path):
        if not self.allow_subtitle:
            warnings.warn(WithoutCCWarning("the video({} p {}) has no subtitle".format('av'+self.aid, self.page)))
        for cc_msg in self.subtitle_list:
            output = path + cc_msg['lan_doc'] + '.srt'
            self._download_single(cc_msg['subtitle_url'], output)