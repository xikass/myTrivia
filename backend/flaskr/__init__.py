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
  
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'categories' :formatted_categories
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
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE

    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions ]
    current_questions = formatted_questions[start:end]
    if len(current_questions) == 0:
      abort(404)

    categories  = Category.query.all()
    formatted_categories = dict()

    for category in categories:
      formatted_categories[category.id] = category.type
    

    return jsonify({
      'success' : True,
      'questions' : current_questions,
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
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    question = Question.query.filter(Question.id == question_id).first()
   
    if question is None:
      abort(404)
    
    question.delete()

    total_questions =  Question.query.count()
    return jsonify({
      'success': True,
      'deleted' : question_id,
      'total_questions': total_questions
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

    body = request.get_json()
    question=body.get('question'),
    answer= body.get('answer'),
    difficulty=body.get('difficulty')
    category = body.get('category', None)
    question_obj = Question(question=question, 
                            answer=answer, 
                            difficulty=difficulty, 
                            category=category)
    question_obj.insert()
    
    return jsonify(question_obj.format())


  '''
  @TODO: 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json()

    search_term = f'%{body.get("searchTerm")}%'

    questions = Question.query.filter(Question.question.ilike(search_term)).all()

    formatted_questions = [question.format() for question in questions]

    return jsonify({
      'questions' : formatted_questions,
      'total_questions' : len(formatted_questions),
      'current_category' : None
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    
    category = Category.query.join(Question, Category.id == Question.category_id).filter(Category.id == category_id).first()
    
    if category is None:
      category = Category.query.filter(Category.id == category_id).first()
      return jsonify({
        'questions': [],
        'total_questions' : 0,
        'current_category' : category.type
      })

    formatted_questions = [question.format() for question in category.questions]
    formatted_category = category.format()


    return jsonify({
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': formatted_category['type']
    })
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
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error' : 404,
      'message': 'resources not found'
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error' : 405,
      'message' : 'Method Not allowed'
    }), 405
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success' : False,
      'error' : 400,
      'message' : 'Bad Request'
    }),400
    
  return app

    