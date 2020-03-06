import requests
import re
import os


class VideoDownloader:
    def __init__(self, av):
        self.s = requests.Session()
        self.base_url = 'https://www.bilibili.com/video/' + av
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Host': 'www.bilibili.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                      'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        response = requests.get(url=self.base_url, headers=headers)
        pattern = re.compile(
            '<script>window.__playinfo__.*?"video":.*?"baseUrl":"(.*?)".*?"audio":.*?"baseUrl":"(.*?)"')
        download_url = re.search(pattern, response.text)
        self.video_url = download_url.group(1)
        self.audio_url = download_url.group(2)

        message_api = 'https://api.bilibili.com/x/player/pagelist'
        data = {
            'aid': av[2:],
            'jsonp': 'jsonp'
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
            'Referer': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        response = requests.get(message_api, params=data, headers=headers)
        self.title = response.json()['data'][0]['part']

    def _get_m4s_resource(self, video_size, audio_size):
        print(self.video_url)
        headers = {
            'Accept': '* / *',
            'Accept-Encoding': 'identity',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Host': self.video_url.split('/')[2],
            'Origin': 'https://www.bilibili.com',
            'Range': 'bytes=0-' + str(video_size),
            'Referer': self.base_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        }
        video_response = requests.get(self.video_url, headers=headers)
        headers['Range'] = 'bytes=0-'+str(audio_size)
        headers['Host'] = self.audio_url.split('/')[2]
        audio_response = requests.get(self.audio_url, headers=headers)
        return video_response, audio_response

    def get_m4s_size(self):
        video_response, audio_response = self._get_m4s_resource(10, 10)
        return video_response.headers['Content-Range'].split('/')[-1], audio_response.headers['Content-Range'].split('/')[-1]

    def download_m4s(self, path):
        if path[-1] != '/':
            path = path + '/'
        video_size, audio_size = self.get_m4s_size()
        video_response, audio_response = self._get_m4s_resource(video_size, audio_size)

        with open(path+self.title+"_video.m4s", 'wb') as f:
            f.write(video_response.content)

        with open(path+self.title+"_audio.m4s", 'wb') as f:
            f.write(audio_response.content)

        return path+self.title+"_video.m4s", path+self.title+"_audio.m4s"

    def merge(self, path, filename=None):
        video_path, audio_path = self.download_m4s(path)
        if path[-1] != '/':
            path = path + '/'
        if not filename:
            filename = self.title+".mp4"
        cmd = 'ffmpeg -i ' + video_path + ' -i ' + audio_path + ' -c:v copy -strict experimental ' + path+filename
        os.system(cmd)


# vd = VideoDownloader("av92795884")
# vd.merge('D:\Code\Bilibili')
