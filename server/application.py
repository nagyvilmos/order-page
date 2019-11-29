import functools
import logging
import os
import threading
from datetime import datetime

import pymongo
from flask import Flask, abort, after_this_request, jsonify, render_template, request
from flask_cors import CORS
from flask_pymongo import PyMongo

import mailer
from constants import (LOG_FILE, LOG_LEVEL, MAIL_PORT, MAIL_SERVER, MONGO_DB,
                       MONGO_URI, STATIC_FOLDER, TEMPLATE_FOLDER)
from model.model import OrderPage

# set up logging for the for the application:
logLevel = getattr(
    logging,
    os.environ.get(
        LOG_LEVEL,
        'WARNING'
    ))

FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
logFile = os.environ.get(LOG_FILE)

if logFile == None:
    logging.basicConfig(format=FORMAT, level=logLevel)
else:
    logging.basicConfig(format=FORMAT, filename=logFile, level=logLevel)

log = logging.getLogger('orderpage')

log.info("Starting Order Page API server")
application = Flask(__name__,
                    static_folder=os.environ[STATIC_FOLDER],
                    template_folder=os.environ[TEMPLATE_FOLDER])

application.config.update({
    'MONGO_URI': os.environ[MONGO_URI] + os.environ[MONGO_DB]})

CORS(application)

log.debug('Load database')
mongo = PyMongo(application)

log.debug('Load mailer')
mailer.init_mailer(application, mongo)

log.debug('create model')
order_page = OrderPage(mongo)


def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or
                    'Content-Encoding' in response.headers):
                return response
            gzip_buffer = BytesIO()
            gzip_file = gzip.GzipFile(mode='wb',
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func


def _post_event(event):
    pass


@application.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@application.route('/api', methods=['GET', 'POST'])
@gzipped
def api():
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = {}
        for n in request.args:
            v = request.args[n]
            try:
                func = {
                    'id': int
                }.get(n, str)
                data[n] = func(v)
            except Exception as ex:
                log.warning(ex)
                data[n] = v
    reply = order_page.request(data)
    post_handle = reply.pop('post')
    if post_handle is not None:
        print(post_handle)
    return jsonify()
# api()


log.info('Server started')
# run the server from here
if __name__ == '__main__':
    application.run(debug=True)
