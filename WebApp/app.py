from flask import Flask, render_template, request
from ai_logic import process_reviews

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            uploaded_file = request.files['file']
            df = process_reviews(uploaded_file)
            return render_template('index.html', data=df.to_html())

    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True)
