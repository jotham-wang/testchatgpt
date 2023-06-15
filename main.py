# -*- coding: utf-8 -*-

from flask import Flask, request, url_for, render_template, redirect, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

import traceback
import logging
from logging.handlers import RotatingFileHandler

from uuid import uuid4

from pipeline import chatbot
from core.utils import Timer


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
CORS(app, resources=r'/*')


def _get_request_data():
    content_type = request.headers.get('content-type')
    # print(content_type)
    if content_type == 'application/x-www-form-urlencoded':
        return request.values
    elif content_type == 'application/json':
        return request.get_json()
    else:
        return request.values if request.values else request.get_json()


# API interface of FlaskDemo
@app.route('/ChatGPTDemo', methods=['GET', 'POST'])
def FlaskDemo():

    if request.method == 'GET':
        return 'OK', 200

    _action = 'ChatGPTDemo'
    _status = 0
    _status_msg = {
        0: '请求成功',
        -1: '请求失败',
        -2: '请求参数错误'
    }
    request_id = ''
    outputs = None

    timer = Timer()
    timer.tic()

    for _ in range(1):
        try:
            content = _get_request_data()
            request_id = content.get('RequestId')
            inputs = content.get('Inputs')
            if not request_id:
                request_id = str(uuid4().int)
            timer.toc('get')
        except Exception as e:
            _status = -2
            app.logger.critical('[{}] {}'.format(request_id, traceback.format_exc()))
            break
        try:
            # put your pipelines here
            outputs = chatbot(inputs)
            #outputs = "--------------chatbot  test--------------  "
            timer.toc('chatbot')
        except Exception as e:
            _status = -1
            app.logger.critical('[{}] {}'.format(request_id, traceback.format_exc()))
            break

    api_res = {
        'RequestId': request_id,
        'ReturnId': _status,
        'Message': _status_msg.get(_status),
        'Outputs': outputs
    }

    app.logger.info('[{}] [ReturnId: {}] [Timer: {}]'.format(request_id, _status, timer.diffs))
    return jsonify(**api_res)


if __name__ == '__main__':
    # run as flask app
    handler = RotatingFileHandler(filename='log/flask.log', encoding='UTF-8')
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
    )
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=443, debug=True)  # The port when the service is started with `python main.py`


if __name__ != '__main__':
    # run in gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
