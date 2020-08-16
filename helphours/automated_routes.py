import json
from helphours import app, queue_handler, log
from flask import request


@app.route('/clear', methods=['POST'])
def clear():
    if 'token' not in request.form:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    expected_token = app.config['CLEAR_TOKEN']
    if request.form['token'] != expected_token:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    queue_handler.clear()
    log.info('Queue was cleared through /clear route')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/open', methods=['POST'])
def open():
    global queue_is_open
    if 'token' not in request.form:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    expected_token = app.config['OPEN_TOKEN']
    if request.form['token'] != expected_token:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    queue_is_open = True
    log.info('Queue was opened through /open route')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/close', methods=['POST'])
def close():
    global queue_is_open
    if 'token' not in request.form:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    expected_token = app.config['CLOSE_TOKEN']
    if request.form['token'] != expected_token:
        return json.dumps({'success': False}), 401, {'ContentType': 'application/json'}
    queue_is_open = False
    log.info('Queue was closed through /close route')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
