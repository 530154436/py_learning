#!/usr/bin/env python3
# -*- coding:utf-8 -*--
import io
import pandas as pd
from pipes import quote
from flask import make_response, send_from_directory
from pathlib import Path


class ExcelDownloader:
    def __init__(self, file: Path):
        self.file: Path = file

    def __call__(self):
        # out = io.BytesIO()
        # df = pd.read_excel(self.file.__str__())
        # with pd.ExcelWriter(out) as writer:
        #     df.to_excel(excel_writer=writer, index=False)
        # response = make_response(out.getvalue())
        # response.headers["Content-Disposition"] = "attachment; filename=%s" % quote(self.file.name)
        # response.headers["Content-type"] = "application/x-xls"
        # return response
        response = send_from_directory(str(self.file.parent), self.file.name, as_attachment=True)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % quote(self.file.name)
        # response.headers["Content-type"] = "application/vnd.ms-excel"
        return response


class CsvDownloader:
    def __init__(self, file: Path):
        self.file: Path = file
        self.data = pd.read_csv(file)

    def __call__(self):
        out = io.StringIO()
        response = make_response(out.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=%s" % quote(self.file.name)
        response.headers["Content-type"] = "text/csv"
        return response
