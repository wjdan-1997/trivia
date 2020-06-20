import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# def paginate_questions(m)


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def show_categories():
        category = Category.query.order_by(Category.id)
        categories = {}
        for find in category:
            categories[find.id] = find.type

        return jsonify({
            "success": True,
            "categories": categories,
            "total_categories": len(Category.query.all()),


        })

    @app.route('/questions', methods=['GET'])
    def show_questions():
        all_questions = Question.query.order_by(Question.id).all()
        question = paginate_questions(request, all_questions)

        if len(question) == 0:
            abort(404)

        category = Category.query.all()

        reindex_category = {}
        for find in category:
            reindex_category[find.id] = find.type

        return jsonify({
            "success": True,
            "questions": question,
            "categories": reindex_category,
            "totalQuestions": len(Question.query.all()),
            "book": "Math"

        })

    @app.route('/questions/<int:questions_id>', methods=['DELETE'])
    def delete_questions(questions_id):
        delete_questions = Question.query.filter(
            Question.id == questions_id).one_or_none()
        delete_questions.delete()

        return jsonify({
            "success": True,
            "deleted": questions_id,
            "name": delete_questions.answer,
            "total_questions": len(Question.query.all())
        })

    @app.route('/questions', methods=['POST'])
    def new_questions():

        from_body = request.get_json()

        new_question = from_body.get('question')
        new_answer = from_body.get('answer')
        new_difficulty = from_body.get('difficulty')
        new_category = from_body.get('category')

        question = Question(question=new_question, answer=new_answer,
                            difficulty=new_difficulty, category=new_category)

        question.insert()

        questions = Question.query.order_by(Question.id).all()
        add_question = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'add_question': add_question,
            'total_questions': len(Question.query.all())
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        from_body = request.get_json()

        search = from_body.get('searchTerm')
        submitSearch = Question.query.order_by(Question.id).filter(
            Question.question.ilike('%{}%'.format(search)))
        add_question = paginate_questions(request, submitSearch)

        return jsonify({
            "success": True,
            "questions": add_question,
            "totalQuestions": len(add_question),
            "ahmed": "fun"
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category_id(category_id):
        questions = Question.query.filter(Question.category == category_id)
        questions = paginate_questions(request, questions)

        print(questions)
        return jsonify({
            "success": True,
            "questions": questions,
            "totalQuestions": len(questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def questions_quiz():
        from_body = request.get_json()
        id = from_body['quiz_category']['id']
        previousQuestions=from_body['previous_questions']

        try:
            if id == 0:
                questions = Question.query.all()
                questions = random.choice(questions)

                quiz = {
                    'id': questions.id,
                    'question': questions.question,
                    'answer': questions.answer,
                    'category': questions.category,
                    'difficulty': questions.difficulty}

                return jsonify({
                    "question": quiz,
                    "previousQuestions": []


                })

            else:
                
                questions = Question.query.filter(
                    Question.category == id,~Question.id.in_(previousQuestions)).all()
                questions = random.choice(questions)

                
                quiz = {
                    'id': questions.id,
                    'question': questions.question,
                    'answer': questions.answer,
                    'category': questions.category,
                    'difficulty': questions.difficulty}

                return jsonify({
                    "question": quiz,
                    "previousQuestions": []})
        except:
            abort(422)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "METHOD NOT ALLOWED"
        }), 405

    return app
