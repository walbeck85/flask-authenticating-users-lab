#!/usr/-bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User, ArticlesSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    
    def get(self):
        articles = [ArticlesSchema().dump(article) for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):

    def get(self, id):
        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1

        if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = ArticlesSchema.dump(article)

            return make_response(article_json, 200)

        return {'message': 'Maximum pageview limit reached'}, 401

# --- 🔐 Authentication Classes 🔐 ---

class Login(Resource):
    def post(self):
        username = request.get_json().get('username')
        user = User.query.filter(User.username == username).first()
        
        if user:
            session['user_id'] = user.id
            user_schema = UserSchema()
            return user_schema.dump(user), 200
        else:
            return {'error': 'Invalid username or password'}, 401

class Logout(Resource):
    def delete(self):
        # 1. Clear the user_id from the session
        session['user_id'] = None
        
        # 2. Return 204 No Content
        return {}, 204

class CheckSession(Resource):
    def get(self):
        # 1. Check for user_id in session
        user_id = session.get('user_id')
        if user_id:
            # 2. Find the user
            user = User.query.filter(User.id == user_id).first()
            if user:
                # 3. Return user data and 200 OK
                user_schema = UserSchema()
                return user_schema.dump(user), 200
        
        # 4. If no user_id or user not found, return 401
        return {}, 401

# --- End Authentication Classes ---


api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')

# --- Authentication Routes ---
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
# --- End Authentication Routes ---

if __name__ == '__main__':
    app.run(port=5555, debug=True)