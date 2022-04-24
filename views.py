import os
import base64, re, time

from flask import render_template, Blueprint, request
from PIL import Image
from io import BytesIO
from json import loads as json_loads
from bin.detector import ObjectDetection


detector = ObjectDetection()
app_index = Blueprint('index', __name__, static_folder="./static")

UPLOAD_FOLDER = os.getcwd() + '/.upload_img/'
TMP = UPLOAD_FOLDER + 'tmp.png'


# MAIN PAGE
@app_index.route("/")
def index():
    return render_template('index.html')


# SAVE CAMERA STREAM FRAMES ON 'SCAN'
@app_index.route('/uploadImage' , methods=['POST'])
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


# PROCESS FRAMES
@app_index.route('/processImages' , methods=['GET'])
def processImages():
    start = time.time()

    predictions = {}

    # Process all images from upload folder
    for image in detector.load_images_from_folder(UPLOAD_FOLDER):
        res = detector.toJson(image)
        printable = json_loads(res)
        # try:
        ds = [printable['name'], printable['confidence']]
        d = {}
        for k in printable['name'].keys():
            d[k] = tuple(d[k] for d in ds)

        # d = {'0': ('lab', 0.8962739706), '1': ('5', 0.7687639594), '2': ('paw', 0.7554306984), '3': ('lab', 0.3543389738), '4': ('3', 0.3261405826)}
        for key in d:
            name, confidence = d[key]
            try: # if confidence exists, app_indexend it
                predictions[name]['confidence'] += confidence
                predictions[name]['occurences'] += 1
            except: # if confidence don't exist, set it
                predictions[name] = {"confidence":confidence, "occurences":1}
            txt = "%4s with confidence of %1.3f" % d[key]
            print(txt)
        print('==============')
    print(predictions)
    
    # Delete all uploaded images once done
    for image in detector.load_images_from_folder(UPLOAD_FOLDER):
        os.remove(image)
    end = time.time()
    print(end - start)

    dot = detector.predict_dot(predictions)

    return '{"dot_id":"'+dot+'","data":'+str(predictions).replace('\'', '\"')+"}"
