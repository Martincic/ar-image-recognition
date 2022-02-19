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
  
@app.route('/maskImage' , methods=['POST'])
def mask_image():
	# print(request.files , file=sys.stderr)
	file = request.files['image'].read() ## byte file
	npimg = np.fromstring(file, np.uint8)
	img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
	######### Do preprocessing here ################
	# img[img > 150] = 0
	## any random stuff do here
	################################################
	img = Image.fromarray(img.astype("uint8"))
	rawBytes = io.BytesIO()
	img.save(rawBytes, "JPEG")
	rawBytes.seek(0)
	img_base64 = base64.b64encode(rawBytes.read())
	return jsonify({'status':str(img_base64)})
  
if __name__ == "__main__":
  app.run()