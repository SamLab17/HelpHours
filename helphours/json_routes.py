from urllib import request
from helphours import app, queue_handler
from flask import jsonify, g
from flask_login import current_user
import flask


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
    def sanitize(x): return False if x is None else x
    return jsonify({'virtual_open': sanitize(g.queue_is_open), 'in_person_open': sanitize(g.in_person_queue_is_open)})


@app.route("/check_position_for", methods=['GET'])
def check_position_for():
    """Given a 'join_token', return what place in the queue the student is in.
    If the student for this token is no longer in the queue, returns -1."""
    tok = flask.request.args.get('join_token') 
    if (pos := queue_handler.get_position_for_join_token(tok)) is not None:
        return jsonify({'position': pos})
    return jsonify({'position': -1})
