#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    articles_data = [{
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date.isoformat() if article.date else None
    } for article in articles]
    return make_response(jsonify(articles_data), 200)

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize or get page_views from session
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check if user has exceeded the free article limit
    if session['page_views'] > 3:
        return {'message': 'Maximum pageview limit reached'}, 401
    
    # Find the article by id
    article = Article.query.filter_by(id=id).first()
    
    if article:
        article_data = {
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.isoformat() if article.date else None
        }
        return make_response(jsonify(article_data), 200)
    return {'message': 'Article not found'}, 404

if __name__ == '__main__':
    app.run(port=5555)