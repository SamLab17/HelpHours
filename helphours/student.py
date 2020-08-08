
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

    def serialize_student_view(self, position):
        return {
            'name': self.name,
            'position': position,
            # 'id': self.id
        }

    def serialize_instructor_view(self, position):
        return {
            'name': self.name,
            'position': position,
            'id': self.id
        }
