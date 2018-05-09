#coding: utf-8

import os
import json
import datetime
import logging

import tornado.ioloop
import tornado.web


PIC_STORE_PATH = "/home/pi/Receives/pictures/img"


class UploadHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def post(self):
        file_name = self.get_argument("file_name")
        logging.warn("File name: %s", file_name)
        extension = os.path.splitext(file_name)[-1]
        content_type = self.get_argument("content_type")
        tmp_path = self.get_argument("tmp_path")
        logging.warn("tmp_path: %s", tmp_path)
        file_md5 = self.get_argument("md5")
        size = self.get_argument("size")
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        new_dir = os.path.join(PIC_STORE_PATH, date)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        new_path = os.path.join(new_dir, date+'_'+file_md5+extension)
        logging.warn("Writing into path %s", new_path)
        with open(new_path, 'a') as new_file:
            with open(tmp_path, 'rb') as f:
                new_file.write(f.read())
        os.remove(tmp_path)
        self.write(dict(
            file_path=new_path,
            size=size,
            ret=0
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
