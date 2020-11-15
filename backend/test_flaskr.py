import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Actor, Movie, actor_movies


class ActorTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Bind the app to the appropriate context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        # Execute after each test
        pass

    #--------------------------------------------------------------------------#
    # Test GET actors endpoint
    #--------------------------------------------------------------------------#
    def test_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

class MovieTestCase(unittest.TestCase):

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Bind the app to the appropriate context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        # Execute after each test
        pass

    #--------------------------------------------------------------------------#
    # Test suite for successful operation and expected errors for Movies
    #--------------------------------------------------------------------------#


if __name__ == "__main__":
    unittest.main()
