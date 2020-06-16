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
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

# def get_catgory(category):
#       category=[i.fromat1() for i in category]
#       return category

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def show_categories():
    category= Category.query.order_by(Category.id)
    category=[find.type.format() for find in category]

    # m=Category.query.all()
    # formm=paginate_questions(request,m)
    # print(formm)
    return jsonify({
      "success":True,
      "categories":category,
      "total_categories":len(Category.query.all()),
      
  
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
  @app.route('/questions', methods=['GET'])
  def show_questions():
    all_questions = Question.query.order_by(Question.id).all()
    question=paginate_questions(request,all_questions)
    # print(question)
    category= Category.query.order_by(Category.id).with_entities(Category.type).all()

    return jsonify({ 
      "success":True,
      "questions":question,
      "categories":category,
      "totalQuestions":len(Question.query.all()),
      "book":"Math"
     
    })
        
        

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID.
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:questions_id>', methods=['DELETE'])
  def delete_questions(questions_id):
    delete_questions = Question.query.filter(Question.id == questions_id).one_or_none()
    delete_questions.delete()  
    # print(delete_questions)
    # x=Question.query.filter(Question.id == 9).one_or_none()
    # print(x.question)

    return jsonify({
      "success":True,
      "deleted": questions_id,
      "name": delete_questions.answer,
      "total_questions":len(Question.query.all())
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
  def new_questions():
        
    from_body = request.get_json()
    # print(from_body)

    new_question=from_body.get('question')
    new_answer=from_body.get('answer')
    new_difficulty=from_body.get('difficulty')
    new_category=from_body.get('category')
    
    question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
    # print(question)
    question.insert()

    questions=Question.query.order_by(Question.id).all()
    
    add_question=paginate_questions(request,questions)
    
    return jsonify({
      'success':True,
      'add_question':add_question,
      'total_questions':len(Question.query.all())
    })
 
    
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
        
    from_body = request.get_json()
    # print(from_body)  
    search = from_body.get('searchTerm')
    submitSearch = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
    add_question=paginate_questions(request,submitSearch)
    
    return jsonify({
        "success":True,
        "questions":add_question,
        "totalQuestions":len(add_question),
        "ahmed":"fun"
    })
  
    
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_by_category_id(category_id): 
   questions=Question.query.filter(Question.category ==category_id)
   questions=paginate_questions(request,questions)
  #  questions=Category.query.filter_by(category.type=category_id).all()

   print(questions)
   return jsonify({
     "success":True,
     "questions":questions,
     "totalQuestions":len(questions)
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
  @app.route('/quizzes', methods=['POST'])
  def get_questions_quiz():
        from_body = request.get_json()
        id=from_body['quiz_category']['id']

        
      
   
        questions=Question.query.filter(Question.category == id ).all()
        questions=random.choice(questions)
        
     
        
        f={
        'id': questions.id,
        'question': questions.question,
        'answer': questions.answer,
        'category': questions.category,
        'difficulty': questions.difficulty}
        print(f)
       
        return jsonify({
         "question":f,
         "previousQuestions":[]
         

        })
       
           


       

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
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
  
  return app

    