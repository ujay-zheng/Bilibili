from downloader.video_downloader import VideoDownloader
from downloader.cc_downloader import CCDownloader
import os
from utils.pyffmpeg import pre_hand_dir_path, merge_cc, merge_double_cc
import fire


def download_video(avs, path):
    dirs = []
    for av in avs:
        vd = VideoDownloader(av)
        dirs.append(vd.download(path, 1, 3))
    return dirs


def download_cc(avs, path):
    for av in avs:
        ccd = CCDownloader(av)
        ccd.download(path, 1, 3)


def download(path, *avs):
    dirs = download_video(avs, path)
    download_cc(avs, path)
    for cur in dirs:
        for page in os.listdir(cur):
            files = os.listdir("{}/{}".format(pre_hand_dir_path(cur), page))
            if 'video' in files:
                video_dir = "{}/{}/video/".format(pre_hand_dir_path(cur), page)
            else:
                video_dir = None
            if 'cc' in files:
                cc_dir = "{}/{}/cc/".format(pre_hand_dir_path(cur), page)
            else:
                cc_dir = None
            if not cc_dir or not video_dir:
                break
            video_name = os.listdir(video_dir)[0]
            cc_file = os.listdir(cc_dir)
            cc_num = len(cc_file)
            if cc_num >= 2:
                merge_double_cc(
                    video_dir, video_name, cc_dir, cc_file[0], cc_file[1],
                    video_dir, "with_cc_{}".format(video_name), True)
            elif cc_num == 1:
                merge_cc(video_dir, video_name, cc_dir, cc_file[0], video_dir, "with_cc_{}".format(video_name), True)


if __name__ == '__main__':
    fire.Fire(download)
