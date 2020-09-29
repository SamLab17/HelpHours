from helphours import app, queue_handler
from flask import jsonify, g
from flask_login import current_user


@app.route("/queue", methods=['GET'])
def queue():
    """ Returns a JSON representation of the queue """
    queue_json = queue_handler.get_serialized_queue(instructorView=current_user.is_authenticated)
    return app.response_class(
        response=queue_json,
        mimetype='application/json'
    )


@app.route("/queue_status", methods=['GET'])
def queue_status():
    status = 'OPEN' if g.queue_is_open else 'CLOSED'
    return jsonify({'status': status})
