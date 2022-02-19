from distutils.log import debug
from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
from threading import Thread
from time import sleep
from flask import request
import numpy as np
import cv2

app = Flask(__name__)
run_with_ngrok(app)
  
@app.route("/")
def index():
    return render_template('index.html')
  
@app.route('/maskImage',methods=["POST"])
def disp_pic():
    data = request.data
    encoded_data = data.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  
if __name__ == "__main__":
  app.run()