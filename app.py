from flask import Flask, send_from_directory, request, jsonify
from pipeline import DE2A2DEBot, get_news
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__, static_folder='../news-translator/build', static_url_path='/')
bot = DE2A2DEBot('')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    data = request.get_json()
    keyword = data['keyword']
    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    news_data = get_news(keyword, date)
    return jsonify(news_data)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    translation = bot.transcribe(text)
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
