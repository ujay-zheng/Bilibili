from error.warn import ParameterError


def get_header(name, **kwargs):
    if permission[name](**kwargs):
        return dict(headers[name], **kwargs)
    else:
        raise ParameterError


permission = {
    'm4s_url': lambda **kwargs: not len(kwargs),
    'm4s_resource': lambda **kwargs: 'Host' in kwargs.keys()
                                     and 'Range' in kwargs.keys() and 'Referer' in kwargs.keys() and len(kwargs) == 3,
    'page_list': lambda **kwargs: 'Referer' in kwargs.keys() and len(kwargs) == 1,
    'cc_message': lambda **kwargs: 'Referer' in kwargs.keys() and len(kwargs) == 1,
    'cc_resource': lambda **kwargs: 'Referer' in kwargs.keys() and len(kwargs) == 1
}


headers = {
    'm4s_url': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Host': 'www.bilibili.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                  'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        },
    'm4s_resource': {
        'Accept': '* / *',
        'Accept-Encoding': 'identity',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Host': None,
        'Origin': 'https://www.bilibili.com',
        'Range': None,
        'Referer': None,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        },
    'page_list': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': None,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    },
    'cc_message': {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Host': 'api.bilibili.com',
        'Origin': 'https://www.bilibili.com',
        'Referer': None,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    },
    'cc_resource': {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': None,
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
}
