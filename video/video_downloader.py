import requests
from video.config import get_header
import re


class SingleVideoDownloader:
    def __init__(self, bv_url, page):
        self.bv_url = bv_url
        self.page = page
        self.video_url, self.audio_url = self._get_m4s_url()
        self.video_size, self.audio_size = self._get_m4s_size()

    def download(self, path):
        video_response, audio_response = self._get_resource(self.video_size, self.audio_size)
        with open("{}page{}_video.m4s".format(path, self.page), 'wb') as f:
            f.write(video_response.content)
        with open("{}page{}_audio.m4s".format(path, self.page), 'wb') as f:
            f.write(audio_response.content)

    def _get_m4s_url(self):
        headers = get_header('m4s_url')
        params = {
            'p': self.page
        }
        res = requests.get(url=self.bv_url, params=params, headers=headers)
        pattern = re.compile(
            '<script>window.__playinfo__.*?"video":.*?"baseUrl":"(.*?)".*?"audio":.*?"baseUrl":"(.*?)"')
        download_url = re.search(pattern, res.text)
        return download_url.group(1), download_url.group(2)

    def _get_m4s_size(self):
        video_response, audio_response = self._get_resource(10, 10)
        return video_response.headers['Content-Range'].split('/')[-1], \
            audio_response.headers['Content-Range'].split('/')[-1]

    def _get_resource(self, video_size, audio_size):
        video_header = get_header(
            'm4s_resource', Host=self.video_url.split('/')[2], Range='bytes=0-' + str(video_size), Referer=self.bv_url)
        audio_header = get_header(
            'm4s_resource', Host=self.audio_url.split('/')[2], Range='bytes=0-' + str(audio_size), Referer=self.bv_url)
        video_response = requests.get(self.video_url, headers=video_header)
        audio_response = requests.get(self.audio_url, headers=audio_header)
        return video_response, audio_response
