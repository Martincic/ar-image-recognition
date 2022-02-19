from distutils.log import debug
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_ngrok import run_with_ngrok
from threading import Thread
from time import sleep
from flask import request
import numpy as np
import os
import cv2
import io
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
run_with_ngrok(app)
  
@app.route("/")
def index():
    return render_template('index.html')
  
@app.route('/maskImage' , methods=['POST'])

def mask_image():
  photo = request.files['photo']
  in_memory_file = io.BytesIO()
  photo.save(in_memory_file)
  data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
  color_image_flag = 1
  img = cv2.imdecode(data, color_image_flag)
  cv2.imshow('URL2Image',img)
  cv2.waitKey(0)

  return 'wo'

  
if __name__ == "__main__":
  print(os.getcwd())
  app.run()