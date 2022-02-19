from distutils.log import debug
from flask import Flask, render_template
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
  
@app.route("/")
def index():
    return render_template('index.html')
  
if __name__ == "__main__":
  app.run(debug=True)