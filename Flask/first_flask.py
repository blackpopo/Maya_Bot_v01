from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name = 'MAYA')

@app.route('/API', methods=['POST'])
def API():
    sentence = request.form['sentence']
    feeling = request.form['user_name']


if __name__=='__main__':
    app.run(port=8080, debug=True)