"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

from flask import session

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()
        self.testuser_id = testuser.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()


    def test_signup_get(self):
        """Can we see the signup form?"""

        with self.client as c:
            # with c.session_transaction() as sess:
            #     sess[CURR_USER_KEY] = self.testuser_id


            resp = c.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('signup form', html)


    def test_signup_post(self):
        """Can we successfully sign up and redirect?"""

        with self.client as c:
            resp = c.post('/signup', follow_redirects=True,
            data =
                {'username': 'testuser2',
                'password': 'test_password',
                'email': 'testuser2@gmail.com',
                'image_url': ''})

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[CURR_USER_KEY],
            User.query.filter(User.username == 'testuser2').one_or_none().id)
            self.assertIn("testing for homepage", html)

    def test_login(self):
        """ Can we successfully login """

        with self.client as c:
            resp = c.post('/login', follow_redirects=True,
                data =
                    {'username': 'testuser',
                    'password': 'testuser'
                    })

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session[CURR_USER_KEY], self.testuser.id)
            self.assertIn(f"Hello", html)