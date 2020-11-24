import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from .models import Question, Category
from .db import setup_db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r'/*': {'origins':'*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
    return response

  @app.route('/')
  def hello():
    return jsonify({
      'message': 'Hello, World!'
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1 , type=int)
    start = (page-1)*10
    end = start+10
    questions = Question.query.all()
    categories = Category.query.all()
    formatted_questions = [question.format() for question in questions ]
    formatted_categories = [category.format() for category in categories]
    
    return jsonify({
      'success' : True,
      'questions' : formatted_questions[start:end],
      'total_questions' : len(formatted_questions),
      'categories' : formatted_categories,
      'current_category': None
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).firts()
    question.delete()
    return jsonify({
      'success': True
    })
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    '''
    @TODO: complete this
    '''
    body = request.get_json()
    question=body.get('question'),
    answer= body.get('answer', None),
    difficulty=body.get('difficulty', None)
    question_obj = Question(question=question, 
                            answer=answer, 
                            difficulty=difficulty, 
                            category=None)
    
    return jsonify({"success": question_obj.question})


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    