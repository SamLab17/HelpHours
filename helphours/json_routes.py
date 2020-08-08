from helphours import app, queue_handler
from flask import jsonify, g
from flask_login import current_user


@app.route("/queue", methods=['GET'])
def queue():
    """ Returns a JSON representation of the queue """
    students = queue_handler.get_students()

    if current_user.is_authenticated:
        serialized_list = [students[i].serialize_instructor_view(i) for i in range(len(students))]
    else:
        serialized_list = [students[i].serialize_student_view(i) for i in range(len(students))]

    return jsonify({'queue': serialized_list})


@app.route("/queue_status", methods=['GET'])
def queue_status():
    status = 'OPEN' if g.queue_is_open else 'CLOSED'
    return jsonify({'status': status})
