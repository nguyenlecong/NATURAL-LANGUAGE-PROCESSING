from flask import Flask, request, render_template
import sys
sys.path.append('D:/Tai Lieu/HUST-Study/20202/NLP/project/code')
from url_input import main

app = Flask(__name__)
 
@app.route('/')
def my_form():
    return render_template('homepage.html')

@app.route('/', methods=['POST'])
def information():
    url = request.form['text']
    infor = main(url)

    return render_template('homepage.html', output=infor, input=url)
 
if __name__ == '__main__':
    app.run()