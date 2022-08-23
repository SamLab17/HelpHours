from datetime import datetime
import uuid

class Student:

    VIRTUAL = 'virtual'
    IN_PERSON = 'in_person'

    """
        Class to represent a Student entry in the
        Lab Hours Queue.
    """
    def __init__(self, name, email, eid, desc, uid, modality=VIRTUAL):
        self.name = name
        self.email = email
        self.eid = eid
        self.desc = desc
        # Whether or not we've sent an email to this
        # student indicating they're next in line
        self.notified = False
        # Corresponds to the id of the visit entry
        # which was created when this student joined
        # the queue.
        self.id = str(uid)
        self.time_entered = datetime.now().strftime('%H:%M:%S')

        # Whether or not the student is in-person or virtual
        self.modality = modality

        self.join_token = str(uuid.uuid1())

    def serialize_student_view(self, position):
        return {
            'name': self.name,
            'position': position,
            'modality': self.modality,
            'join_token': f"{self.join_token}"
        }

    def serialize_instructor_view(self, position):
        return {
            'name': self.name,
            'position': position,
            'modality': self.modality,
            'desc': self.desc,
            'id': self.id,
            'time': self.time_entered,
        }
