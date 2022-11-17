import pytest, logging, unittest, os
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db

from App.models import *
from App.controllers import *

from wsgi import app


LOGGER = logging.getLogger(__name__)

"""
   Unit Tests
"""

# Unit tests for User model

class UserUnitTests(unittest.TestCase):
    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"
    
    def test_new_admin_user(self):
        user = User("bob", "bobpass", 2)
        assert user.access == 2

    def test_new_normal_user(self):
        user = User("bob", "bobpass", 1)
        assert user.access == 1

    def test_user_is_admin(self):
        user = User("bob", "bobpass", 2)
        assert user.is_admin()

    def test_user_is_not_admin(self):
        user = User("bob", "bobpass", 1)
        assert not user.is_admin()

    # pure function no side effects or integrations called
    def test_to_json(self):
        user = User("bob", "bobpass")
        user_json = user.to_json()
        self.assertDictEqual(user_json, {"access": 1, "id": None, "username": "bob"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method="sha256")
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

# Unit tests for Student model
class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("bob", "FST", "Computer Science")
        assert (
            student.name == "bob"
            and student.faculty == "FST"
            and student.programme == "Computer Science"
        )
    
    def test_student_to_json(self):
        student = Student("bob", "FST", "Computer Science")
        student_json = student.to_json()
        self.assertDictEqual(
            student_json,
            {
                "faculty": "FST",
                "id": None,
                "karma": 0,
                "name": "bob",
                "programme": "Computer Science",
            },
        )