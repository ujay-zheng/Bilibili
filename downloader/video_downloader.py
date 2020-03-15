import requests
from utils.pyffmpeg import merge, set_ffmpeg_path, pre_hand_dir_path, pre_hand_dir
import os
from downloader.video_message import VideoMessage
import re


class VideoDownloader(VideoMessage):
    def __init__(self, av, ffmpeg_path=None):
        super(VideoDownloader, self).__init__(av)
        if ffmpeg_path:
            set_ffmpeg_path(ffmpeg_path)

    def _get_m4s_url(self, page):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Host': 'www.bilibili.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        params = {
            'p': page
        }
        res = requests.get(url=self.base_url, params=params, headers=headers)
        pattern = re.compile(
            '<script>window.__playinfo__.*?"video":.*?"baseUrl":"(.*?)".*?"audio":.*?"baseUrl":"(.*?)"')
        download_url = re.search(pattern, res.text)
        return download_url.group(1), download_url.group(2)

    def _get_resource(self, page, video_size, audio_size):
        video_url, audio_url = self._get_m4s_url(page)
        headers = {
            'Accept': '* / *',
            'Accept-Encoding': 'identity',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Host': video_url.split('/')[2],
            'Origin': 'https://www.bilibili.com',
            'Range': 'bytes=0-' + str(video_size),
            'Referer': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        video_response = requests.get(video_url, headers=headers)
        headers['Range'] = 'bytes=0-'+str(audio_size)
        headers['Host'] = audio_url.split('/')[2]
        audio_response = requests.get(audio_url, headers=headers)
        return video_response, audio_response

    def get_m4s_size(self, page):
        video_response, audio_response = self._get_resource(page, 10, 10)
        return video_response.headers['Content-Range'].split('/')[-1], \
            audio_response.headers['Content-Range'].split('/')[-1]

    def download_m4s(self, page, dir_path):
        dir_path = "{}{}_{}/m4s/".format(pre_hand_dir_path(dir_path), page, self.video_pages[page-1]['part'])
        pre_hand_dir(dir_path)
        audio_path = "{}{}".format(dir_path, "audio_p{}_{}.m4s".format(page, self.video_pages[page-1]['part']))
        video_path = "{}{}".format(dir_path, "video_p{}_{}_.m4s".format(page, self.video_pages[page-1]['part']))
        video_size, audio_size = self.get_m4s_size(page)
        video_response, audio_response = self._get_resource(page, video_size, audio_size)
        with open(video_path, 'wb') as f:
            f.write(video_response.content)
        with open(audio_path, 'wb') as f:
            f.write(audio_response.content)
        return video_path, audio_path, dir_path

    def download_video(self, page, dir_path, cover=True, keep=False):
        video_path, audio_path, m4s_path = self.download_m4s(page, dir_path)
        dir_path = "{}{}_{}/video/".format(pre_hand_dir_path(dir_path), page, self.video_pages[page-1]['part'])
        pre_hand_dir(dir_path)
        output_name = "p{}_{}.mkv".format(page, self.video_pages[page-1]['part'])
        try:
            path = merge(video_path, audio_path, dir_path, output_name, cover)
        except Exception as e:
            raise e
        finally:
            if not keep:
                os.remove(video_path)
                os.remove(audio_path)
                os.rmdir(m4s_path)
        return path

    def download(self, dir_path, start=1, end=None, cover=True, keep=False):
        dir_path = pre_hand_dir_path(dir_path) + self.title
        temp = enumerate(self.video_pages[start-1: end]) if end else enumerate(self.video_pages[start-1:])
        for i, page in temp:
            self.download_video(i+1, dir_path, cover=cover, keep=keep)
        return dir_path


if __name__ == '__main__':
    vd = VideoDownloader('av60977932')
    vd.download('D:\Code\Bilibili',  start=1, end=1, keep=True)
