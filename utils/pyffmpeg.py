import os


def merge(video, audio, output, cover):
    if not cover and os.path.exists(output):
        raise FileExistsError
    cmd = 'ffmpeg -i "{}" -i "{}" -y -c:v copy "{}"' if cover else 'ffmpeg -i {} -i {} -c:v copy "{}"'
    print(cmd.format(video, audio, output))
    os.system(cmd.format(video, audio, output))


def merge_cc(video, cc_path, cc_file, output, cover, insert):
    os.chdir(cc_path)
    if not cover and os.path.exists(output):
        raise FileExistsError
    if insert:
        cmd = r'ffmpeg -i "{}" -y -vf subtitles={} "{}'
    else:
        cmd = 'ffmpeg -i "{}" -f srt -i "{}" -y -map 0:0 -map 0:1 -map 1:0 -c:v copy -c:a copy -c:s srt "{}"'
    print(cmd.format(video, cc_file, output))
    os.system(cmd.format(video, cc_file, output))


def merge_double_cc(video, cc_path, cc_file1, cc_file2, output, cover):
    os.chdir(cc_path)
    if not cover and os.path.exists(output):
        raise FileExistsError
    cmd = 'ffmpeg -i "{}" -f srt -i "{}" -i "{}" -y -map 0:0 -map 0:1 -map 1:0 -map 2:0  -c:v copy -c:a copy -c:s ' \
          'srt -metadata:s:s:0 language="{}" -metadata:s:s:1 language="{}" "{}"'
    print(cmd.format(video, cc_file1, cc_file2, cc_file1, cc_file2, output))
    os.system(cmd.format(video, cc_file1, cc_file2, cc_file1, cc_file2, output))
