import unittest
from ..student import Student


class TestStudent(unittest.TestCase):

    def test_name(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "Help", "")
        self.assertEqual("John Doe", x.name)

    def test_email(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "Help", "")
        self.assertEqual("john@gmail.com", x.email)

    def test_eid(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "Help", "")
        self.assertEqual("jd123", x.eid)

    def test_desc(self):
        x = Student("John Doe", "john@gmail.com", "jd123", "Help", "")
        self.assertEqual("Help", x.desc)

    def test_combined(self):
        x = Student("Jane Doe", "jane@gmail.com", "jd1234", "Need help", "")
        self.assertEqual("Jane Doe", x.name)
        self.assertEqual("jane@gmail.com", x.email)
        self.assertEqual("jd1234", x.eid)
        self.assertEqual("Need help", x.desc)


if __name__ == '__main__':
    unittest.main()
