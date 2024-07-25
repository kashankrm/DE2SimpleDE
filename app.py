from flask import Flask, render_template, request, jsonify
from pipeline import DE2A2DEBot, get_news
from datetime import datetime, timedelta
import random

app = Flask(__name__)
bot = DE2A2DEBot('')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    keyword = request.form['keyword']
    date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    news_data = get_news(keyword, date)
    return jsonify(news_data)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    translation = bot.transcribe(text)
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
