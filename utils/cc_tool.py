import math
import requests
from .pyffmpeg import pre_hand_dir_path
# 下面这段处理CC字幕的代码是我copy来的


def _format_time(h, m, s, ms):
    return '{}:{}:{},{}'.format(str(h).zfill(2), str(m).zfill(2), str(s).zfill(2), str(ms).zfill(2))


def _text2time(text):
    hour = math.floor(text) // 3600
    minute = (math.floor(text) - hour * 3600) // 60
    sec = math.floor(text) - hour * 3600 - minute * 60
    mini_sec = int(math.modf(text)[0] * 1000)
    return hour, minute, sec, mini_sec


def json2srt(subtitles):
    srt_string = ''
    line = '{}\n{} --> {}\n{}\n\n'
    for i, subtitle in enumerate(subtitles, 1):
        start = subtitle['from']  # 获取开始时间
        end = subtitle['to']  # 获取结束时间
        content = subtitle['content']  # 获取字幕内容

        sh, sm, ss, sms = _text2time(start)
        eh, em, es, ems = _text2time(end)
        ems -= 1  # 此处减1是为了防止两个字幕同时出现

        start_str = _format_time(sh, sm, ss, sms)
        end_str = _format_time(eh, em, es, ems)
        # 一个片段
        srt_string += line.format(i, start_str, end_str, content)
    return srt_string


# class CCResource:
#     def __init__(self, cc_url, video_url):
#         headers = {
#             'Accept': 'application/json, text/javascript, */*; q=0.01',
#             'Referer': video_url,
#             'Sec-Fetch-Dest': 'empty',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                           '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
#         }
#         res = requests.get(url=cc_url, headers=headers)
#         self.data = res.json()['body']
#
#     def write_srt(self, dir_path, file_name):
#         file_path = "{}{}".format(pre_hand_dir_path(dir_path), file_name)
#         with open(file_path, "w", encoding='utf-8') as f:
#             f.write(json2srt(self.data))
#         return file_path