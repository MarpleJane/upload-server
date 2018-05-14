#coding: utf-8

import os
import json
import datetime
import logging

import tornado.ioloop
import tornado.web


MEDIA_STORE_PATH = "/home/pi/Receives/media"
COLUMN_STORE_PATH = "/home/pi/Receives/columns"
HTML_AC = """<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><title>Document</title></head><body>"""
HTML_BC = """</body></html>"""


class UploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Accept", "*/*")

    def post(self):
        new_path = ""
        media_type = self.get_argument("media_type", "else")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        content_type = "html"
        if media_type == "else":
            file_name = self.get_argument("file_name")
            logging.warn("File name: %s", file_name)
            extension = os.path.splitext(file_name)[-1]
            content_type = self.get_argument("content_type")
            tmp_path = self.get_argument("tmp_path")
            logging.warn("tmp_path: %s", tmp_path)
            file_md5 = self.get_argument("md5")
            size = self.get_argument("size")
            new_dir = os.path.join(MEDIA_STORE_PATH, date)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            new_path = os.path.join(new_dir, date+'_'+file_md5+extension)
            logging.warn("Writing into path %s", new_path)
            with open(new_path, 'w') as new_file:
                with open(tmp_path, 'rb') as f:
                    new_file.write(f.read())
            os.remove(tmp_path)
        elif media_type == "column":
            logging.warn("Column's turn")
            column_name = self.get_argument("column")
            tmp_content = self.get_argument("content")
            content = HTML_AC + tmp_content + HTML_BC
            new_dir = os.path.join(COLUMN_STORE_PATH, date)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            new_path = os.path.join(new_dir, date+'_'+column_name+'.html')
            with open(new_path, 'w') as new_file:
                new_file.write(content)
        else:
            logging.warn("Unknown type")
        self.write(dict(
            file_path=os.path.relpath(new_path, "/home/pi"),
            ret=0,
            content_type=content_type
        ))


def make_app():
    return tornado.web.Application([
          (r'/uploadHandler', UploadHandler),
    ])


if __name__ == "__main__":
    port = 8888
    app = make_app()
    app.listen(port)
    logging.warn("Server start at port[%d]", port)
    tornado.ioloop.IOLoop.current().start()
