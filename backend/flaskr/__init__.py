import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from .models import Question, Category
from .db import setup_db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, query):

  page_number = request.args.get('page', 1, type=int)
  start = (page_number-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE
  formatted_questions = [question.format() for question in query]

  return formatted_questions[start:end]

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
    if categories is None:
      abort(404)

    formatted_categories = dict()
    for category in categories:
      formatted_categories[category.id] = category.type
    
    return jsonify({
      'categories' :formatted_categories,
      'success' : True
    })

  '''
  @TODO: 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    #get questions
    questions = Question.query.all()
    if len(questions) == 0:
      abort(404)
    current_questions = paginate_questions(request, questions)
    #get categories
    categories  = Category.query.all()
    if len(categories) == 0:
      abort(404)
    formatted_categories = dict()
    for category in categories:
      formatted_categories[category.id] = category.type
    #set data dictionary
    data = {
      'success' : True,
      'questions' : current_questions,
      'total_questions' : len(questions),
      'categories' : formatted_categories,
      'current_category': None
    }
    return jsonify(data)
  '''
  @TODO: 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    #get question
    question = Question.query.filter(Question.id == question_id).first()
    if question is None:
      abort(422)
    #delete question
    try:
      question.delete()
      total_questions =  Question.query.count()
      data = {
      'success': True,
      'deleted' : question_id,
      'total_questions': total_questions
      }
      return jsonify(data)
    except:
      abort(422)
    
  '''
  @TODO: 

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    #get body json
    body = request.get_json()

    search_term =body.get('searchTearm', None)
    if search_term:
      search_term = f'%{search_term}%'
      # get all questions that has case insensetive LIKE search_term
      try:
        questions = Question.query.filter(Question.question.ilike(search_term)).all()
        questions_list = [question.format() for question in questions]
        return jsonify({
        'success' : True,
        'questions' : questions_list,
        'total_questions' : len(questions_list)
        })
      except:
        abort(400)
    else:
      question=body.get('question', None),
      answer= body.get('answer', None),
      difficulty=body.get('difficulty', None)
      category = body.get('category', None)
      question_obj = Question(question=question, 
                            answer=answer, 
                            difficulty=difficulty, 
                            category=category)
      question_obj.insert()
      data = question_obj.format()
      data['success']= True
      return jsonify(data)

    
  '''
  @TODO: 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      #get questions
      query = Question.query.filter(Question.category==category_id).all()
      questions_list = paginate_questions(request, query)
      #get questions category
      category = Category.query.filter(Category.id==category_id).first_or_404().type
      #set data 
      data = {
      'success':True,
      'questions': questions_list,
      'total_questions': len(questions_list),
      'current_category': category
      }
      return jsonify(data)
    except:
      abort(404)
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
  @app.route('/quizzes', methods=['POST'])
  def play():
    #get data
    req = request.get_json()
    previous_questions = req.get('previousQuestions')
    quizz_category = req.get('quiz_category', None)

    #set 
    questions = ''
    if quizz_category['id'] == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == quizz_category['id']).all()
    
    questions = [question.format() for question in questions]
    while ( True) :
      q = random.choice(questions)
      if q in previous_questions:
        continue
      else:
        return jsonify(q.format())

    


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

    