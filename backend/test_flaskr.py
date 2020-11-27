import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import  Question, Category
from flaskr.db import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        questions  = Question.query.all()
        formatted_questions = [question.format() for question in questions ]

        categories = Category.query.all()
        formatted_categories = dict()
        for category in categories:
            formatted_categories[f'{category.id}'] = category.type

        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertListEqual(data['questions'], formatted_questions[0:10])
        self.assertEqual(data['total_questions'], len(questions))
        self.assertDictEqual(data['categories'], formatted_categories)

    def test_422_delete_question(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertNotEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable entity')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()