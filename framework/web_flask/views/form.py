#!/usr/bin/env python3
# -*- coding:utf-8 -*--
from flask import Blueprint, render_template, request, jsonify
from framework.web_flask.controllers.single_gene_handler import SingleGeneHandler

blueprint = Blueprint('form', __name__)


@blueprint.route('/ajax-submit-form', methods=["POST"])
def ajax_submit_form():
    if request.method == 'POST':
        sg_handler = SingleGeneHandler()
        sg_handler.parse_form(request)
        print(sg_handler.json())
        return jsonify(sg_handler.json())


@blueprint.route('/ajax-form')
def ajax_table_stype():
    return render_template("form/ajax-form.html")
