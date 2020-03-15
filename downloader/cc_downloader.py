from downloader.video_message import VideoMessage
import requests
from error.cc_exception import NotFoundError, WithoutCCError
from utils.pyffmpeg import pre_hand_dir_path, pre_hand_dir
from utils.cc_tool import json2srt


class CCDownloader(VideoMessage):
    def __init__(self, av):
        super(CCDownloader, self).__init__(av)

    def get_cc_message(self, page):
        message_url = 'https://api.bilibili.com/x/web-interface/view'
        params = {
            'aid': self.av[2:],
            'cid': self.video_pages[page - 1]['cid']
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'Referer': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        res = requests.get(message_url, params=params, headers=headers)
        return res.json()['data']['subtitle']

    def _get_zh_resource(self, page):
        subtitle = self.get_cc_message(page)
        if not subtitle['allow_submit']:
            print("the video({} p {}) has no Chinese subtitle".format(self.av, page))
            raise NotFoundError
        for cc in subtitle['list']:
            if '简体' in cc['lan_doc'] or 'zh' in cc['lan'] or '中文' in cc['lan_doc']:
                return cc['subtitle_url'], cc['lan_doc']
        raise NotFoundError

    def _get_resource(self, cc_url, page):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': "{}?p={}".format(self.base_url, page),
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        res = requests.get(url=cc_url, headers=headers)
        return res.json()['body']

    def download_single(self, page, cc_url, file_path):
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(json2srt(self._get_resource(cc_url, page)))
        return file_path

    def download_zh_single(self, page, dir_path):
        zh_url, cc_name = self._get_zh_resource(page)
        dir_path = '{}{}_{}/cc/'.format(pre_hand_dir_path(dir_path), page, self.video_pages[page - 1]['part'])
        pre_hand_dir(dir_path)
        file_path = "{}cc_p{}_{}.srt".format(dir_path, page, cc_name)
        return self.download_single(page, zh_url, file_path)

    def download_all_language(self, page, dir_path):
        cc_messages = self.get_cc_message(page)
        if not cc_messages['allow_submit']:
            print("the video({} p {}) has no subtitle".format(self.av, page))
            raise WithoutCCError
        for cc_message in cc_messages['list']:
            temp_path = "{}{}_{}/cc/".format(pre_hand_dir_path(dir_path), page, self.video_pages[page - 1]['part'])
            pre_hand_dir(temp_path)
            temp_path = "{}cc_p{}_{}.srt".format(temp_path, page, cc_message['lan_doc'])
            self.download_single(page, cc_message['subtitle_url'], temp_path)

    def download(self, dir_path, start=1, end=None):
        dir_path = pre_hand_dir_path(dir_path) + self.title
        temp = enumerate(self.video_pages[start-1: end])if end else enumerate(self.video_pages[start-1:])
        for i, page in temp:
            try:
                self.download_all_language(i + 1, dir_path)
            except WithoutCCError:
                continue

    def download_zh(self, dir_path, start=1, end=None):
        dir_path = pre_hand_dir_path(dir_path) + self.title
        temp = enumerate(self.video_pages[start-1: end]) if end else enumerate(self.video_pages[start-1:])
        for i, page in temp:
            try:
                self.download_zh_single(i + 1, dir_path)
            except NotFoundError as e:
                continue


if __name__ == '__main__':
    ccd = CCDownloader("av60977932")
    ccd.download(r'D:\Code\Bilibili', start=1, end=3)
