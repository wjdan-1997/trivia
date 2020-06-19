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
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', '123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_questions = {
            'question': 'what is yor name',
            'answer': 'wejdan-,',
            'category': 2,
            'difficulty': 4
        }

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    # """
    def test_get_categories(self):
        res=self.client().get('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['total_categories'],6)

    def test_categories_failing(self):
        res=self.client().post('/categories')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'METHOD NOT ALLOWED')


    def test_get_questions_failing(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(data['success'], False)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 19)


    def test_delete_questions(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],23)
        self.assertEqual(data['total_questions'],19)

    def test_failing_delete(self):
        res=self.client().post('/questions/23')
        data=json.loads(res.data)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'METHOD NOT ALLOWED')

    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'Who discovered penicillin?'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_search_failing(self):
        res = self.client().get('/questions/search',
                                json={'searchTerm': 'Who discovered penicillin?'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'METHOD NOT ALLOWED')

    def test_post_questions(self):
        res =self.client().post('/questions', json=self.new_questions)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        pass

    def test_422_if_question_creation_fails(self):
        res = self.client().get('/questions', json={"kkkkkk"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
