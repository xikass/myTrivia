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
    formatted_questions = [question.format() for question in query[start:end]]

    return formatted_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        '''
          return all categories from the database
          categories dict contains
          key = the category id
          value = the category type
        '''
        categories = Category.query.all()

        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type

        return jsonify({
            'categories': formatted_categories,
            'success': True
        })

    @app.route('/questions')
    def get_questions():
        '''
        consume page (integer)
        if not supplied, page default to 1
        Return 10 question objects per page if success
        Return 404 if failed
        '''
        try:
            # get questions
            questions = Question.query.all()

            current_questions = paginate_questions(request, questions)

            if current_questions == []:
                abort(404)
            # get categories
            categories = Category.query.all()

            formatted_categories = dict()
            for category in categories:
                formatted_categories[category.id] = category.type
            # set data dictionary
            data = {
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'categories': formatted_categories,
                'current_category': None
            }
            return jsonify(data)
        except:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        consume question_id (integer)
        Return the deleted question id and the total remaining questions
        Return 404 if failed
        '''
        # get question
        question = Question.query.filter(Question.id == question_id).first()
        if question is None:
            abort(404)
        # delete question
        try:
            question.delete()
            total_questions = Question.query.count()
            data = {
                'success': True,
                'deleted': question_id,
                'total_questions': total_questions
            }
            return jsonify(data)
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        if search_term != '':
            search_term = f'%{search_term}%'

            # get all questions that has case insensetive LIKE search_term
            try:
                questions = Question.query.filter(
                    Question.question.ilike(search_term)).all()
                questions_list = [question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'questions': questions_list,
                    'total_questions': len(questions_list)
                })
            except:
                abort(400)
        else:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        '''
          creating new question, the following should be supplied:
            {
              "question" : "string of the question statement?",
              "answer" : "string of the answer",
              "difficulty" : an integer between 1 and 3 inclusive,
              "category" : category_id
            }
          if failed will return 400

        '''
        # get body json
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty')
        category = body.get('category')
        if (question is None or answer is None):
            abort(400)
        try:
            question_obj = Question(question=question,
                                    answer=answer,
                                    difficulty=difficulty,
                                    category=category)
            question_obj.insert()
            data = question_obj.format()
            data['success'] = True
            return jsonify(data)
        except:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        '''
        consume category_id (integer)
        get all questions that have the same category_id value
        return 404 if failed
        '''
        try:
            # get questions
            query = Question.query.filter(
                Question.category == category_id).all()
            if query == []:
                abort(404)
            questions_list = paginate_questions(request, query)
            # get questions category
            category = Category.query.filter(
                Category.id == category_id).first_or_404().type
            # set data
            data = {
                'success': True,
                'questions': questions_list,
                'total_questions': len(questions_list),
                'current_category': category
            }
            return jsonify(data)
        except:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play():
        # get data
        req = request.get_json()
        previous_questions = req.get('previous_questions')
        quiz_category = req.get('quiz_category')

        # set questions list
        questions = ''
        if quiz_category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == quiz_category['id']).all()

        if questions == []:
            abort(404)
        questions = [question.format() for question in questions]

        data = {
            'question': None,
            'success': True
        }
        counter = 0
        while(counter < len(questions)):
            q = random.choice(questions)
            if q['id'] in previous_questions:
                counter += 1
                continue
            data['question'] = q
            return jsonify(data)

        return jsonify(data)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resources not found'
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
        }), 500

    return app
