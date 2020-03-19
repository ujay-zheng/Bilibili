import requests
from bs4 import BeautifulSoup
from utils.pypyth import pre_handle_path, standardized_path
from video.config import get_header
from video.video_downloader import SingleVideoDownloader
from video.cc_downloader import CCDownloader
from utils.pyffmpeg import merge, merge_cc, merge_double_cc
import os


class Video:
    def __init__(self, av):
        self.av = av
        self.av_url = 'https://www.bilibili.com/video/{}'.format(av)
        self.title = BeautifulSoup(requests.get(self.av_url).text, 'lxml').head.title.text
        self.page_list = _get_page_list(av, self.av_url)  # 每一集的信息（一个list）， 只需要其中每个的cid，page和part
        self.page_num = len(self.page_list)

    def download(self, path, start=1, end=None, cover=True, keep=True, bilingual=True, insert=False):
        path = '{}{}/'.format(standardized_path(path), self.title)
        page_range = range(start - 1, end) if end else range(start - 1, self.page_num)
        for page_id in page_range:
            part = self.page_list[page_id]
            part_path = '{}page_{}_{}/'.format(path, part['page'], part['part'])
            part_video_path, part_m4s_path, part_cc_path = part_path + 'video/', part_path + 'm4s/', part_path + 'cc/'
            pre_handle_path(part_video_path, part_m4s_path, part_cc_path)
            svd = SingleVideoDownloader(self.av_url, part['page'])
            svd.download(part_m4s_path)
            ccd = CCDownloader(self.av[2:], part['cid'], part['page'])
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
                merge_cc(video, part_cc_path, cc_files[0], part_video_path+"page{}_with_cc.mkv".format(part['page']),
                         cover, insert)
            elif bilingual and cc_nums >= 2:
                merge_double_cc(video, part_cc_path, cc_files[0], cc_files[1],
                                part_video_path+"page{}_with_double_cc.mkv".format(part['page']), cover)


def _get_page_list(av, video_url):
    params = {
        'aid': av[2:],
        'jsonp': 'jsonp'
    }
    headers = get_header('page_list', Referer=video_url)
    res = requests.get('https://api.bilibili.com/x/player/pagelist', params=params, headers=headers)
    return res.json()['data']


if __name__ == '__main__':
    v = Video('av51815774')
    v.download("D:\Code", start=2, end=2)
