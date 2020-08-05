import unittest
import sys
sys.path.append('../helphours')
sys.path.append('..')
from student import Student


class TestStudent(unittest.TestCase):

    def test_name(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("John Doe", x.name)

    def test_email(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("john@gmail.com", x.email)

    def test_eid(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "")
        self.assertEqual("jd123", x.eid)

    def test_combined(self):
        x = Student("Jane Doe", "jane@gmail.com", "jd1234", "")
        self.assertEqual("Jane Doe", x.name)
        self.assertEqual("jane@gmail.com", x.email)
        self.assertEqual("jd1234", x.eid)


if __name__ == '__main__':
    unittest.main()
