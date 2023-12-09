from flask import Flask, render_template, request
import requests
import json
from ai_logic import categorize_review
app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
OPENAI_API_ENDPOINT = 'https://api.openai.com/v1/engines/davinci-codex/completions'

# List to store the history of questions and answers
history = []

@app.route('/')
def index():
    return render_template('index.html', history=history)

@app.route('/get_response', methods=['POST'])
def get_response():
    question = request.form['question']

    try:
        answer = categorize_review(question)
        print(answer)
        # Add the current question and answer to the history list
        # history.append({'question': question, 'answer': answer})

        return render_template('index.html', question=question, answer=answer)

    except Exception as e:
        print(e)
        return render_template('index.html', question=question, answer="answer")


if __name__ == '__main__':
    app.run(debug=True)
