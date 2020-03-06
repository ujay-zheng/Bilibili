# 一些关于Bilibili的工具

* 本项目主要为一些Bilibili的常用（对于我自己来说常用）工具，主要依靠爬虫来实现。    
* git规范遵循[南昌大家园工作室的git规范](https://yanshuo.io/assets/player/?deck=58f7703ba22b9d006c15edee#/)

* 运行前先pip install -r requirements.txt

* Bilibili视频下载的说明
    * 首先确保你的电脑安装了ffmpeg， 如果没有安装ffmpeg将代码将无法正确执行， 如果没有ffmpeg的可以前往
    [官网](https://www.ffmpeg.org/)安装，并且记得配置环境变量。（需要ffmpeg的原因是B站是音频分开的
    当你进行爬虫的时候只能获得一段视频文件和语音文件，所以需要通过ffmpeg来进行合成）
    * 代码主要为video_downloader.py中的VideoDownloader类（如果不想看后面那段话的话，可以直接看文件中最下面两行，那就是一个使用的例子）
    构造该类的时候需要传入一个av号（此处av号的格式必须为avxxxxx，不能个只写
    数字）。如果你只想下载视频的MP4文件，那么直至需要调用merge函数即可，merge函数中传入存放的文件夹路径以及文件名称（记得以.mp4结尾），
    当然文件名是可选项，如果不填的话会以视频标题作为文件名。merge函数还会获得两个m4s文件，这是合成前的视频文件和语音文件。如果想获得视
    频文件和语音文件的大小可以调用get_m4s_size函数。其他函数没有调用的必要。
