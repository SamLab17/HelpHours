import json
from typing import Union
from helphours.student import Student

"""
    Representation of the Queue in memory. This
    is a list of Student objects where index=0 is the
    "front" of the queue.
"""
student_queue: list[Student] = []

serialized_student_view = None
serialized_instructor_view = None

"""
    Enqueues a Student object to the end of the queue.
    If the students was already in the queue, based on
    EID, then their previous entry is removed and they are
    added to the end of the queue.
"""


def enqueue(student: Student):
    # check to see if they are in the queue already
    remove_eid(student.eid)

    # add them to the queue, return their place in line
    student_queue.append(student)
    generate_serialized_queues()
    return len(student_queue)


"""
    Returns the list of students so that it
    can be printed out on the View Queue page.
"""


def get_students():
    return student_queue


"""
    Returns the "runner-up" Student object.
    This is the student which is after the first person
    in .
"""


def peek_runner_up():
    return peek_student_at(1)


def peek_student_at(pos):
    if len(student_queue) <= pos:
        return None
    return student_queue[pos]


"""
    Removes a student based on a unique Visit ID.
    This ID is assigned when the student is added to the
    queue and their "visit" is added to the visits table.
    This ID is entirely sequential and thus students should NEVER
    be allowed to remove themselves based on this ID.
"""


def remove(id):
    for i in range(0, len(student_queue)):
        if(id == student_queue[i].id):
            del student_queue[i]
            generate_serialized_queues()
            return


"""
    Removes a student based on their UT EID that was
    entered when they joined the queue.
"""


def remove_eid(eid):
    for i in range(0, len(student_queue)):
        if(eid == student_queue[i].eid):
            s = student_queue[i]
            del student_queue[i]
            generate_serialized_queues()
            return s
    return None


"""
    Removes all students from the queue
"""


def clear():
    global student_queue
    student_queue = []
    generate_serialized_queues()


"""
    Handles creating a JSON representation of the queue
    when the front-end polls the current queue
"""


def get_serialized_queue(instructorView=False):
    if instructorView:
        if serialized_instructor_view is None:
            generate_serialized_queues()
        return serialized_instructor_view
    else:
        if serialized_student_view is None:
            generate_serialized_queues()
        return serialized_student_view


def generate_serialized_queues():
    global serialized_instructor_view
    global serialized_student_view
    students = get_students()

    instructor_serialized_list = [students[i].serialize_instructor_view(i) for i in range(len(students))]
    serialized_instructor_view = json.dumps({'queue': instructor_serialized_list})

    student_serialized_list = [students[i].serialize_student_view(i) for i in range(len(students))]
    serialized_student_view = json.dumps({'queue': student_serialized_list})


def get_position_for_join_token(join_token: str) -> Union[int, None]:
    for i, s in enumerate(student_queue):
        if s.join_token == join_token:
            return i
    return None
