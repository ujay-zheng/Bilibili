import requests
from bs4 import BeautifulSoup


class VideoMessage:
    def __init__(self, av):
        self.av = av
        self.base_url = 'https://www.bilibili.com/video/{}'.format(av)
        self.video_pages = _get_page_list(av, self.base_url)
        self.title = BeautifulSoup(requests.get(self.base_url).text, 'lxml').head.title.text


def _get_page_list(av, base_url):
    playlist_url = 'https://api.bilibili.com/x/player/pagelist'
    params = {
        'aid': av[2:],
        'jsonp': 'jsonp'
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': base_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    res = requests.get(playlist_url, params=params, headers=headers)
    return res.json()['data']


if __name__ == "__main__":
    vm = VideoMessage("av60977932")
    print(vm.video_pages)
