#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="biget",
    version="0.1.0",
    keywords=("pip", "bilibili", 'video download', 'spider', 'B站视频下载', '弹幕'),
    description="关于B站的一个爬虫，可以获取视频的信息，下载视频等",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/ujay-zheng/biget",
    author="ujay",
    author_email="897013045@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['requests', 'beautifulsoup4', 'lxml']
)
