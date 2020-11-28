import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import  Question, Category
from flaskr.db import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    new_question = {'question': 'string question?',
            'answer': 'string answer',
            'difficulty': 1,
            'category': 2}
    quiz_req = {
        'previous_questions' : [],
        'quiz_category' : {'id':2}
    }
    search_term1 = {"searchTerm": "eg"}
    search_term2 = {"searchTerm": "triv"}

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
    def test_get_categories(self):

        res = self.client().get('/categories')
        data = json.loads(res.data)

        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[f'{category.id}'] = category.type

        self.assertDictEqual(data['categories'], formatted_categories)
        self.assertTrue(data['success'])

    
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
    
    def test_delete_questions(self):
        #get random question to delete
        question = Question.query.first()
        questions_count = Question.query.count()

        res = self.client().delete(f'/questions/{question.id}')
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question.id)
        self.assertEqual(data['total_questions'], questions_count-1)

    
    def test_create_questions(self):
 
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['question'], self.new_question['question'])
        self.assertEqual(data['answer'], self.new_question['answer'])
        self.assertEqual(data['difficulty'], self.new_question['difficulty'])
        self.assertEqual(data['category'], self.new_question['category'])
        self.assertTrue(data['success'])
    
    def test_search_question(self):

        res = self.client().post('/questions/search', json=self.search_term1)
        data = json.loads(res.data)

        search_term = f"%{self.search_term1['searchTerm']}%"
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
        self.assertEqual(data['questions'], questions)
        self.assertEqual(data['total_questions'],len(questions))

        search_term = f"%{self.search_term2['searchTerm']}%"
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
        self.assertEqual(data['questions'], questions)
        self.assertEqual(data['total_questions'],len(questions))

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
    
    def test_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz_req)
        questions = Question.query.filter(Question.category == self.quiz_req['quiz_category']['id']).all()
        formatted_questions = [question.format() for question in questions]
        data = json.loads(res.data)

        self.assertNotIn(data['question']['id'], self.quiz_req['previous_questions'])
        self.assertIn(data['question'], formatted_questions)
        # test for all questions
        for question in formatted_questions:
            self.quiz_req['previous_questions'].append(question)
            res = self.client().post('/quizzes', json=self.quiz_req)
            data = json.loads(res.data)
            self.assertNotIn(data['question']['id'], self.quiz_req['previous_questions'])
            self.assertIn(data['question'], formatted_questions)

    def test_404_quest_by_cat(self):
        res = self.client().get('/categories/500/questions')
        data = json.loads(res.data)

        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resources not found')      

    def test_404_delete_question(self):
        res = self.client().delete('/questions/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resources not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()