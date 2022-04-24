from flask import Flask
from views import app_index

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
PORT = 5050

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# unneccessary if ngrok run before
# run_with_ngrok(app)

if __name__ == "__main__":
    app.register_blueprint(app_index)
    app.run(debug=False, port=PORT)