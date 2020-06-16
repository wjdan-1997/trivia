import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','123','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_questions ={
                'question':'d',
                'answer':'wejdan-,',
                'category':2,
                'difficulty':4
            }
       
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
    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['totalQuestions'],13)
        

    def tes_404_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data =json.loads(res, data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'],6)
    

    def test_delete_questions(self):
        res = self.client().delete('/questions/22')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        # self.assertEqual(data['deleted'],30)
        self.assertEqual(data['total_questions'],13)
    
    def test_get_book_search_with_results(self):
        res = self.client().post('/questions/search' , json={'search':'what is yor name '})
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_post_questions(self):
        res =self.client().post('/questions', json=self.new_questions)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        pass


    def test_422_if_book_creation_fails(self):
        res = self.client().post('/questions', json=self.new_questions)
        data = json.loads(res.data)
        pass
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()