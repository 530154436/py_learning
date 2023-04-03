#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from typing import Union
from pathlib import Path


class ImageHandler(object):

    @classmethod
    def return_img_stream(cls, img_local_path: Union[Path, str]) -> str:
        """
        工具函数:
        获取本地图片流
        :param img_local_path:文件单张图片的本地绝对路径
        :return: 图片流
        """
        import base64
        img_stream = ''
        with open(str(img_local_path), 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream).decode()
        return img_stream
