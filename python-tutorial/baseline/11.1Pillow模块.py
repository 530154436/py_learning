# /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import random
from PIL import Image,ImageFilter,ImageFont, ImageDraw

mainDir = '/Users/zhengchubin/Desktop/projects/ocr/data/movie'

def operateOnImage():
    imgPath = os.path.join(mainDir, '羞羞的铁拳_5.png')
    img = Image.open(imgPath)
    w,h = img.size
    print('Image size (width, height): ({}, {})'.format(w, h))

    # img.thumbnail((w // 2, h // 2))
    # img.save('羞羞的铁拳_5_thumbnail.png', 'png')

    img2=img.filter(ImageFilter.BLUR)
    img2.save('羞羞的铁拳_5_blur.png', 'png')

def rndChar():
    return chr(random.randint(65, 90))

def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def yanzhengma():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('code.jpg', 'jpeg')

if __name__ == '__main__':
    # operateOnImage()
    yanzhengma()