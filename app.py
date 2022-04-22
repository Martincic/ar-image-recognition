from distutils.log import debug
from charset_normalizer import detect
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_ngrok import run_with_ngrok
from threading import Thread
from time import sleep
from flask import request
from matplotlib.font_manager import json_load
import numpy as np
import os
import cv2
import io
import time
import base64, re, time
from PIL import Image
from io import BytesIO
from bin.detector import ObjectDetection
import json
import timeit


UPLOAD_FOLDER = os.getcwd() +'/.upload_img/'
TMP = UPLOAD_FOLDER +'tmp.png'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

detector = ObjectDetection()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# run_with_ngrok(app)
  
@app.route("/")
def index():
    return render_template('index.html')
  
@app.route('/uploadImage' , methods=['POST'])
def uploadImage():
    img_data= (request.data).decode("utf-8")

    #convert to png
    base64_data = re.sub('^data:image/.+;base64,', '', img_data )
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()

    #save png
    img.save(UPLOAD_FOLDER + str(t) +'.png', "PNG")
    return "OK"

@app.route('/processImages' , methods=['GET'])
def processImages():
    start = time.time()

    predictions = {}

    # Process all images from upload folder
    for image in detector.load_images_from_folder(UPLOAD_FOLDER):
        res = detector.toJson(image)
        printable = json.loads(res)
        # try:
        ds = [printable['name'], printable['confidence']]
        d = {}
        for k in printable['name'].keys():
            d[k] = tuple(d[k] for d in ds)

        # d = {'0': ('lab', 0.8962739706), '1': ('5', 0.7687639594), '2': ('paw', 0.7554306984), '3': ('lab', 0.3543389738), '4': ('3', 0.3261405826)}
        for key in d:
            name, confidence = d[key]
            try: # if confidence exists, append it
                predictions[name]['confidence'] += confidence
                predictions[name]['occurences'] += 1
            except: # if confidence don't exist, set it
                predictions[name] = {"confidence":confidence, "occurences":1}
            txt = "%4s with confidence of %1.3f" % d[key]
            print(txt)
        print('==============')
    print(predictions)

        # except:
        # print('err')
    
    # Delete all uploaded images once done
    for image in detector.load_images_from_folder(UPLOAD_FOLDER):
        os.remove(image)
    end = time.time()
    print(end - start)

    dot = detector.predict_dot(predictions)

    return '{"dot_id":"'+dot+'"data":'+str(predictions).replace('\'', '\"')+"}"


if __name__ == "__main__":
    app.run(debug=True, port=5050)