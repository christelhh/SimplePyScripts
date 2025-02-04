#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт парсит файл формата fb2, вытаскивает из него картинки и сохраняет их в папке с таким же названием,
как файл fb2."""


import base64
import io
import os
import traceback

from lxml import etree

# pip install humanize
from humanize import naturalsize as sizeof_fmt

from PIL import Image

from common import get_file_name_from_binary


def do(file_name, output_dir="output", debug=True):
    dir_fb2 = os.path.basename(file_name)
    dir_im = os.path.join(output_dir, dir_fb2)
    os.makedirs(dir_im, exist_ok=True)
    debug and print(dir_im + ":")

    total_image_size = 0

    with open(file_name, "rb") as fb2:
        tree = etree.XML(fb2.read())

        binaries = tree.xpath("./*[local-name()='binary']")
        for i, binary in enumerate(binaries, 1):
            try:
                im_id = binary.attrib["id"]
                content_type = binary.attrib["content-type"]

                im_file_name = get_file_name_from_binary(im_id, content_type)
                im_file_name = os.path.join(dir_im, im_file_name)

                im_data = base64.b64decode(binary.text.encode())

                count_bytes = len(im_data)
                total_image_size += count_bytes

                with open(im_file_name, mode="wb") as f:
                    f.write(im_data)

                im = Image.open(io.BytesIO(im_data))
                debug and print(
                    f"    {i}. {im_id} {sizeof_fmt(count_bytes)} format={im.format} size={im.size}"
                )

            except:
                traceback.print_exc()

    file_size = os.path.getsize(file_name)
    debug and print()
    debug and print("fb2 file size =", sizeof_fmt(file_size))
    debug and print(
        f"total image size = {sizeof_fmt(total_image_size)} ({total_image_size / file_size * 100:.2f}%)"
    )


if __name__ == "__main__":
    fb2_file_name = "../input/Непутевый ученик в школе магии 1. Зачисление в школу (Часть 1).fb2"
    do(fb2_file_name)
