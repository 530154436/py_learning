#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename

from framework.web_flask import BASE_DIR
from framework.web_flask.controllers.image_handler import ImageHandler

blueprint = Blueprint('image', __name__)


@blueprint.route('/ajax-upload-image', methods=["POST"])
def ajax_upload_image():
    if request.method == 'POST':
        # 上传图片
        input_file = request.files['input_file']
        file = BASE_DIR.joinpath("data", "upload", secure_filename(input_file.filename))
        input_file.save(file)

        # 展示图片
        return {
            "base64": ImageHandler.return_img_stream(file)
        }


@blueprint.route('/ajax-image')
def ajax_image():
    return render_template("image/ajax-image.html")
