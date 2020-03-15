import os

software = "ffmpeg"


def set_ffmpeg_path(path):
    global software
    software = path


def pre_hand_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def pre_hand_dir_path(file_dir):
    return file_dir if file_dir[-1] == '/' or file_dir[-1] == '\\' else file_dir + '/'


def merge(video_path, audio_path, dir_path, file_name, cover):
    dir_path = pre_hand_dir_path(dir_path)
    file_path = "{}{}".format(dir_path, file_name)
    if not cover and os.path.exists(file_path):
        raise FileExistsError
    cmd = '{} -i "{}" -i "{}" -y -c:v copy "{}"' if cover else '{} -i {} -i {} -c:v copy {}'
    os.system(cmd.format(software, video_path, audio_path, file_path))
    return file_path


def merge_cc(video_path, video_file, cc_path, cc_file, dir_path, file_name, cover, insert):
    dir_path = pre_hand_dir_path(dir_path)
    pre_hand_dir(dir_path)
    file_path = "{}{}".format(dir_path, file_name)
    os.chdir(cc_path)
    if not cover and os.path.exists(file_path):
        raise FileExistsError
    if insert:
        cmd = r'{} -i "{}" -y -vf subtitles={} "{}'
    else:
        cmd = '{} -i "{}" -f srt -i "{}" -y -map 0:0 -map 0:1 -map 1:0 -c:v copy -c:a copy -c:s srt "{}"'
    os.system(cmd.format(software, pre_hand_dir_path(video_path)+video_file, cc_file, file_path))
    return file_path


def merge_double_cc(video_path, video_file, cc_path, cc_file1, cc_file2, dir_path, file_name, cover):
    dir_path = pre_hand_dir_path(dir_path)
    pre_hand_dir(dir_path)
    file_path = "{}{}".format(dir_path, file_name)
    os.chdir(cc_path)
    if not cover and os.path.exists(file_path):
        raise FileExistsError
    cmd = '{} -i "{}" -f srt -i "{}" -i "{}" -y -map 0:0 -map 0:1 -map 1:0 -map 2:0  -c:v copy -c:a copy -c:s ' \
          'srt -metadata:s:s:0 language="{}" -metadata:s:s:1 language="{}" "{}"'
    os.system(
        cmd.format(
            software, pre_hand_dir_path(video_path)+video_file, cc_file1, cc_file2, cc_file1, cc_file2, file_path))
    return file_path
