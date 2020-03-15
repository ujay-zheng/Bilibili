# Some Tools about Bilibili   

## Table of Contents
- [Background](#background)
- [History](#history)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)

## Background   
Bilibili is one of my favorite Chinese video site. I will spent lots of time watching videos on Bilibili everyday, and
you know, this is the best pastime.But as I watched more and more videos, I find a problem.Some videos are so awesome 
that I want to download them and watch them again and again.Besides, when I am on the high speed train or some environment
where the signal is too poor to watch the video smoothly, the downloaded videos are especially important.We know that 
Bilibili on the mobile client can download videos and many download tools are already available, these methods still do 
not meet my needs.First of all, if i use the download tools and Bilibili mobile client to download videos in batches
(different av number), it will be a disaster for me because it is so inconvenient.What more, in some video the subtitles 
and video are separated witch is called "Closed Caption".Mobile client and most tools can not download the Closed Caption.
And the most important is that I want a complete set of tools to get all the information I need about Bililbii, not just 
download videos.So It will be a big project for me.At last, the software is only for learning and communication, please 
do not use it for any commercial purpose! Thank you everyone!    

## History
* v0.1
This version has basically completed my own needs and I haven't test it.I just did some video downloads through my own 
code without any problems.Besides, I wrote this demo in a hurry,so I highly recommend that you write the downloaded code 
through the documents I left (just use my class).And, when writing these classes, my design may not be very good. If you 
have better suggestions, please contact me by email.

## Install   
First of all, make sure you have installed ffmpeg.If you don't have it, then go to the [here](http://ffmpeg.org/) to 
download.And remember to add the path to the PATH environment variable.After that you need to enter the following command 
to install the necessary dependencies.
```
pip3 install -r requirement.txt
```

## Usage   
To be able to use my code in different situation, I just write some class but not a complete web or GUI project. So I
can quickly build a project through these class.For each class I have detailed instructions in the [docs](docs).I have 
provided you with a simple demo, you can directly use it if you just want to download the videos.Of course I still 
recommend that you write your own code based on the documentation in the [docs](docs).   
   
Let me show you how to use my simple demo.You can just run this command:
```
python demo.py download_path av1 av2 ... avn
```
Let me explain what this command does, and what we want.You can download any number of videos, by specifying the av 
number, which is av1 ... avn in the command(the size of n depends on the number you want to download).After that this 
command will create a directory which is named by the video title for each video under download_path.Then all sub-videos 
of each video (Bilibili uses p and a number to distinguish each sub-video) are downloaded in their own directory.it will
create new directory for each sub-video, and sub-video will be downloaded in the directory called video under the sub-video
directory created before, and if the sub-video has Closed Caption, than there will be a directory called cc under the
sub-video directory.By the way, there will be two video in video, one with Closed Caption, the other without it.By default, 
all subtitle files will be downloaded. If there is only one subtitle file, it will be merged with the video directly. If 
there are two or more subtitle files, only the first two files will be merged with the video.



## Maintainers    
| Maintainers                                         | Email                                                        |
| --------------------------------------------------- | ------------------------------------------------------------ |
|[@ujay-zheng](https://github.com/ujay-zheng) | 897013045@qq.com|