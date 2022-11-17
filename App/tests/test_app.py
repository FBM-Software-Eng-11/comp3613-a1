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

# Unit tests for Review model
class ReviewUnitTests(unittest.TestCase):
    def test_new_review(self):
        review = Review(1,1,"good student", "positive")
        assert review.student_id == 1 and review.user_id == 1 and review.text == "good student" and review.reviewType == "positive"

    def test_review_to_json(self):
            review = Review(1, 1, "good","positive")
            review_json = review.to_json()
            self.assertDictEqual(
                review_json,
                {
                    "id": None,
                    "user_id": 1,
                    "student_id": 1,
                    "time": review.get_time(),
                    "review type": "positive",
                    "text": "good",
                    "karma": 20,
                    "num_upvotes": 0,
                    "num_downvotes": 0,
                    
                },
             )

# Unit tests for Votes Model
class VotesUnitTests(unittest.TestCase):
    def test_new_vote(self):
        review = Review(1,1,"good student", "positive")
        vote = Votes(1, 1, "up")
        assert vote.review_id == 1 and vote.voteType == "up" and vote.voter_id == 1



"""
    Integration Tests
"""

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"})
    create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd() + "/App/test.db")


# Integration tests for User model
class UsersIntegrationTests(unittest.TestCase):
    def test_authenticate(self):
        user = create_user("bob", "bobpass")
        assert authenticate("bob", "bobpass") is not None

    def test_create_admin(self):
        test_admin = create_user("rick1", "rickpass", 2)
        admin = get_user_by_username("rick1")
        assert test_admin.username == admin.username and test_admin.is_admin()

    def test_create_user(self):
        test_user = create_user("john", "johnpass", 1)
        user = get_user_by_username("john")
        assert user.username == "john" and not user.is_admin()

    def test_get_user(self):
        test_user = create_user("johnny", "johnpass", 1)
        user = get_user(test_user.id)
        assert test_user.username == user.username

    def test_get_all_users_json(self):
        users = get_all_users()
        users_json = get_all_users_json()
        assert users_json == [user.to_json() for user in users]

    def test_update_user(self):
        user = create_user("danny", "johnpass", 1)
        update_user(user.id, "daniel")
        assert get_user(user.id).username == "daniel"

    def test_delete_user(self):
        user = create_user("bobby", "bobbypass", 1)
        uid = user.id
        delete_user(uid)
        assert get_user(uid) is None

    # Integration tests for Student model
class StudentIntegrationTests(unittest.TestCase):
    def test_create_student(self):
        test_student = create_student("bob", "fst", "cs")
        student = get_student(test_student.id)
        assert test_student.name == student.name

    def test_get_students_by_name(self):
        students = get_students_by_name("bob")
        assert students[0].name == "bob"

    def test_get_all_students_json(self):
        students = get_all_students()
        students_json = get_all_students_json()
        assert students_json == [student.to_json() for student in students]

    # tests updating a student's name, programme and/or faculty
    def test_update_student(self):
        with self.subTest("Update name"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, "bobby")
            assert get_student(student.id).name == "bobby"
        with self.subTest("Update programme"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, programme="it")
            assert get_student(student.id).programme == "it"
        with self.subTest("Update faculty"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, faculty="fss")
            assert get_student(student.id).faculty == "fss"
        with self.subTest("Update all"):
            student = create_student("bob", "fst", "cs")
            update_student(student.id, "bobby", "it", "fss")
            assert get_student(student.id).name == "bobby"
            assert get_student(student.id).programme == "it"
            assert get_student(student.id).faculty == "fss"

    def test_delete_student(self):
        student = create_student("bob", "fst", "cs")
        sid = student.id
        delete_student(sid)
        assert get_student(sid) is None

# Integration tests for Review model
class ReviewIntegrationTests(unittest.TestCase):
    def test_create_review(self):
        test_review = create_review(1, 1, "good", "positive")
        review = get_review(test_review.id)
        assert test_review.text == review.text and test_review.id == 1

    def test_update_review_text(self):
        test_review = create_review(1, 1, "good", "positive")
        update_review(test_review.id, "great student", "positive")
        assert get_review(test_review.id).text == "great student" and get_review(test_review.id).get_review_karma() == 20

    def test_update_review_reviewType(self):
        test_review = create_review(1, 1, "good", "positive")
        update_review(test_review.id, "great student", "negative")
        assert get_review(test_review.id).reviewType == "negative" and get_review(test_review.id).get_review_karma() == -10

    def test_delete_review(self):
        test_review = create_review(1, 1, "good", "postive")
        rid = test_review.id
        delete_review(rid)
        assert get_review(rid) is None

    def test_get_review_json(self):
        test_review = create_review(1, 1, "good","positive")
        review_json = get_review_json(test_review.id)
        assert review_json == test_review.to_json()

    def test_get_all_reviews_json(self):
        reviews = get_all_reviews()
        reviews_json = get_all_reviews_json()
        assert reviews_json == [review.to_json() for review in reviews]
