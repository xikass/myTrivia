import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import  Question, Category
from flaskr.db import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    new_question = {'question': 'is this a new question?',
            'answer': 'this is an answer',
            'difficulty': 3,
            'category': 2}

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
        formatted_categories = {}
        for category in categories:
            formatted_categories[f'{category.id}'] = category.type

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertListEqual(data['questions'], formatted_questions[0:10])
        self.assertEqual(data['total_questions'], len(questions))
        self.assertDictEqual(data['categories'], formatted_categories)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resources not found')
    
    def test_create_questios(self):

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['question'], self.new_question['question'])
        self.assertEqual(data['answer'], self.new_question['answer'])
        self.assertEqual(data['difficulty'], self.new_question['difficulty'])
        self.assertEqual(data['category'], self.new_question['category'])
        self.assertTrue(data['success'])

    def test_get_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)

        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[f'{category.id}'] = category.type

        self.assertDictEqual(data['categories'], formatted_categories)
        self.assertTrue(data['success'])
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        questions = Question.query.filter(Question.category==2).all()
        formatted_questions = [question.format() for question in questions]
        category = Category.query.filter(Category.id==2).first_or_404().type

        self.assertListEqual(data['questions'], formatted_questions[0:10])
        self.assertEqual(data['total_questions'], len(formatted_questions[0:10]))
        self.assertTrue(data['success'])
        self.assertEqual(data['current_category'], category)
    
    def test_404_quest_by_cat(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resources not found')      

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()