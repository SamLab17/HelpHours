
class Student:
    """
        Class to represent a Student entry in the
        Lab Hours Queue.
    """
    def __init__(self, name, email, eid, uid):
        self.name = name
        self.email = email
        self.eid = eid
        # Whether or not we've sent an email to this
        # student indicating they're next in line
        self.notified = False
        # Corresponds to the id of the visit entry
        # which was created when this student joined
        # the queue.
        self.id = str(uid)


class StudentJSON:
    def __init__(self, student_obj, queue_position):
        self.name = student_obj.name
        self.position = queue_position
        self.uid = student_obj.id

    def serialize(self):
        return {
            'name': self.name,
            'position': self.position,
            'uid': self.uid
        }
