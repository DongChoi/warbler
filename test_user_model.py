"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from typing import Type
from unittest import TestCase

import sqlalchemy

from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD_2"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.u1 = u1
        self.u2 = u2



    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u1.messages), 0)
        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(len(self.u1.following), 0)
        self.assertEqual(self.u1.username, "testuser1")
        self.assertEqual(self.u1.email, "test1@test.com")

    def test_user_model_repr(self):
        """tests repr in user model"""
        self.assertEqual(self.u1.__repr__(), f"<User #{self.u1.id}: {self.u1.username}, {self.u1.email}>")
        self.assertNotEqual(self.u1.__repr__(), f"<User #{self.u2.id}: {self.u2.username}, {self.u2.email}>")

    def test_user_model_is_followed_by(self):
        """Tests if user is followed by another user"""

        u2_follow_u1 = Follows(user_being_followed_id=self.u1.id, user_following_id=self.u2.id)

        db.session.add(u2_follow_u1)
        db.session.commit()

        self.assertEqual(self.u1.is_followed_by(self.u2), True)
        self.assertEqual(self.u2.is_followed_by(self.u1), False)


    def test_user_model_is_following(self):
        """Tests if user is following another user"""

        u2_follow_u1 = Follows(user_being_followed_id=self.u1.id, user_following_id=self.u2.id)

        db.session.add(u2_follow_u1)
        db.session.commit()

        self.assertEqual(self.u1.is_following(self.u2), False)
        self.assertEqual(self.u2.is_following(self.u1), True)
        # test length of followers


    def test_user_model_sign_up(self):
        """Testing for authenticate function"""

        test_user = User.signup(email="test3@test.com",
                            username="testuser3",
                            password="HASHED_PASSWORD",
                            image_url="")

        db.session.commit()

        test_user_db = User.query.filter(User.username == "testuser3").one_or_none()

        self.assertEqual(test_user_db.email, "test3@test.com")
        self.assertEqual(test_user_db.username, "testuser3")
        self.assertEqual(test_user_db.password.startswith('$2b$12$'), True)
        self.assertNotEqual("test4", User.query.get(test_user.id).username)

    def test_unique_signup(self):
        """ Test for sign up with already existing values """

        with self.assertRaises(IntegrityError):
            already_existing_username = User.signup(email="test3@test.com",
                            username="testuser2",
                            password="HASHED_PASSWORD",
                            image_url="")
            db.session.commit()

    def test_non_null_signup(self):
        """ Test for sign up with an unfilled not nullable field """

        with self.assertRaises(IntegrityError):
            signup_with_no_username = User.signup(email="test4@test.com",
                            username=None,
                            password="HASHED_PASSWORD",
                            image_url=""
                            )
            db.session.commit()

    #more function with names separating happy/bad paths
    def test_user_model_authenticate(self):
        """Testing for authenticate function"""

        test_user = User.signup(email="test5@test.com",
                            username="testuser5",
                            password="PASSWORD",
                            image_url="")

        db.session.commit()

        self.assertEqual(User.authenticate(test_user.username, "PASSWORD"), test_user)
        self.assertEqual(User.authenticate("invalid_username", "PASSWORD"), False)
        self.assertEqual(User.authenticate(test_user.username, "hahaha"), False)