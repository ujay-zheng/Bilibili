import requests
from bs4 import BeautifulSoup
from utils.pypyth import pre_handle_path, standardized_path
from biget.vtools.headers import get_header
from biget.vtools.downloader import CCDownloader, SingleVideoDownloader
from utils.pyffmpeg import merge, merge_cc, merge_double_cc
import os
from biget.vtools.utils import get_video_message


class Video:
    def __init__(self, bv):
        self.bv = bv
        self.bv_url = 'https://www.bilibili.com/video/{}'.format(bv)
        self.title, self.date = self._get_title_date()
        self.page_list = _get_page_list(bv, self.bv_url)
        self.page_num = len(self.page_list)
        self.data = None
        self.bullet_comments = None

    def download(self, pages, path=os.getcwd(), cover=True, keep=True, bilingual=True, insert=False):
        path = '{}{}/'.format(standardized_path(path), self.title)
        for page_id in pages:
            part = self.page_list[page_id]
            part_path = '{}page_{}_{}/'.format(path, part['page'], part['part'])
            part_video_path, part_m4s_path, part_cc_path = part_path + 'video/', part_path + 'm4s/', part_path + 'cc/'
            pre_handle_path(part_video_path, part_m4s_path, part_cc_path)
            svd = SingleVideoDownloader(self.bv_url, part['page'])
            svd.download(part_m4s_path)
            ccd = CCDownloader(self.bv[2:], part['cid'], part['page'])
            ccd.download(part_cc_path)
            video_m4s = "{}page{}_video.m4s".format(part_m4s_path, part['page'])
            audio_m4s = "{}page{}_audio.m4s".format(part_m4s_path, part['page'])
            video = part_video_path + "page{}.mkv".format(part['page'])
            merge(video_m4s, audio_m4s, video, cover)
            if not keep:
                os.remove(video_m4s)
                os.remove(audio_m4s)
                os.rmdir(part_m4s_path)
            cc_files = os.listdir(part_cc_path)
            cc_nums = len(cc_files)
            if cc_nums == 0:
                continue
            elif not bilingual or cc_nums == 1:
                merge_cc(video, part_cc_path, cc_files[0], part_video_path + "page{}_with_cc.mkv".format(part['page']),
                         cover, insert)
            elif bilingual and cc_nums >= 2:
                merge_double_cc(video, part_cc_path, cc_files[0], cc_files[1],
                                part_video_path + "page{}_with_double_cc.mkv".format(part['page']), cover)

    def access(self):
        video_msg = get_video_message(self.bv, self.page_list[0]['cid'])
        tags = self._get_tags_info(video_msg['aid'])
        self.data = {
            'bvid': video_msg['bvid'],
            'aid': video_msg['aid'],
            'page_num': self.page_num,
            'title': self.title,
            'date': self.date,
            'owner': video_msg['owner']['name'],
            'owner_id': video_msg['owner']['mid'],
            'view': video_msg['stat']['view'],
            'danmaku': video_msg['stat']['danmaku'],
            'reply': video_msg['stat']['reply'],
            'favorite': video_msg['stat']['favorite'],
            'coin': video_msg['stat']['coin'],
            'share': video_msg['stat']['share'],
            'now_rank': video_msg['stat']['now_rank'],
            'his_rank': video_msg['stat']['his_rank'],
            'like': video_msg['stat']['like'],
            'page': self.page_list,
            'tags': [{'tag_id': tag['tag_id'], 'tag_name': tag['tag_name']} for tag in tags],
        }

    def get_bullet(self, pages):
        self.bullet_comments = [_save_bullet_comments(self.page_list[page_id]['cid']) for page_id in pages]

    def _get_title_date(self):
        res = BeautifulSoup(requests.get(self.bv_url).text, 'lxml')
        return res.head.title.text, \
            res.find('meta', attrs={'data-vue-meta': 'true', 'itemprop': 'uploadDate'}).attrs['content']

    def _get_tags_info(self, aid):
        url = 'https://api.bilibili.com/x/tag/archive/tags'
        params = {
            'aid': aid
        }
        header = get_header('tags', Referer=self.bv_url)
        res = requests.get(url, headers=header, params=params)
        return res.json()['data']


def _save_bullet_comments(cid):
    url = 'https://api.bilibili.com/x/v1/dm/list.so'
    params = {
        'oid': cid
    }
    headers = get_header('bullet_comments')
    res = requests.get(url, headers=headers, params=params)
    res.encoding = 'utf8mb4'
    r = BeautifulSoup(res.text, 'lxml')
    return r.find_all('d')


def _get_page_list(bv, video_url):
    params = {
        'bvid': bv,
        'jsonp': 'jsonp'
    }
    headers = get_header('page_list', Referer=video_url)
    res = requests.get('https://api.bilibili.com/x/player/pagelist', params=params, headers=headers)
    return res.json()['data']
