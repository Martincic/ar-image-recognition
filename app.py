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
import base64, re, time
from PIL import Image
from io import BytesIO


UPLOAD_FOLDER = os.getcwd() +'/.upload_img/)'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# run_with_ngrok(app)
  
@app.route("/")
def index():
    return render_template('index.html')
  

@app.route('/maskImage' , methods=['POST'])
def maskImage():
    print('aaa')
    img_data= (request.data).decode("utf-8")

    #convert to png
    base64_data = re.sub('^data:image/.+;base64,', '', img_data )
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()

    #save png
    img.save(UPLOAD_FOLDER + str(t) + '.png', "PNG")

    imgByteArr = image_data.getvalue()
    imgByteArr = base64.encodebytes(imgByteArr).decode('ascii')
    print(imgByteArr)

    return imgByteArr


if __name__ == "__main__":
    app.run(debug=True, port=5050)