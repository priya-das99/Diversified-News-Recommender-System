from flask import Flask, render_template, request, redirect, url_for, flash, session
from .database import get_trending_news, get_recommended_news, authenticate_user, get_news_by_id, track_news_click
import os
from datetime import timedelta

from PIL import Image
import base64
import io

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)



@app.route('/')
def home():
    if 'user_id' not in session:
        app.logger.info('No user_id in session, redirecting to login')
        return redirect(url_for('login'))
    try:
        app.logger.info(f'Fetching news for user: {session["user_id"]}')
        trending_news = get_trending_news()
        app.logger.info(f'Got {len(trending_news)} trending news items')
        recommended_news = get_recommended_news(session['user_id'])
        app.logger.info(f'Got {len(recommended_news)} recommended news items')
    except Exception as e:
        app.logger.error(f'Error fetching news: {str(e)}')
        flash('Error fetching news: ' + str(e))
        return render_template('error.html'), 500
    return render_template('index.html', trending_news=trending_news, recommended_news=recommended_news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        # Authenticate user (no password check)
        if authenticate_user(user_id, password):
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        recommended_news = get_recommended_news(session['user_id'])
    except Exception as e:
        flash('Error fetching recommended news: ' + str(e))
        return render_template('error.html'), 500
    return render_template('recommendations.html', recommended_news=recommended_news)

@app.route('/news/<news_id>')
def news_detail(news_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    try:
        news = get_news_by_id(news_id)
        if not news:
            flash('News item not found.')
            return redirect(url_for('home'))
        
        # Track the news click
        if track_news_click(session['user_id'], news_id):
            recommended_news = get_recommended_news(session['user_id'])
        else:
            flash('Error tracking news interaction.')
            return redirect(url_for('home'))
    
    except Exception as e:
        flash('Error fetching news details: ' + str(e))
        return render_template('error.html'), 500
    return render_template('news_detail.html', news=news, recommended_news=recommended_news)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
