# RIT Campus navigator
Real time campus navigator. Sums the items detected in given image and calculates/outputs user's current position on RIT Zagreb campus.

Authors:
  - Sara Oguic (soguic)
  - Tomas Martincic (Martincic)
  - terminator

### Preview

![Preview of the program](https://raw.githubusercontent.com/Martincic/ar-image-recognition/main/preview.gif)

## Tools used
We've used [YOLOv5](https://github.com/ultralytics/yolov5) detection algorithm with which we've trained our dataset. The data was collected on site via video. We extracted the frames with [FFMPEG](https://ffmpeg.org/) and prepared with [Roboflow](https://roboflow.com/).

### Installation
```
pip install -r REQUIREMENTS.txt
python app.py
```
At this moment, the server on local network will be running. 

#### How to use 
Due to modern browser restrictions of interfacing hardware over insecure HTTP connections, we've decided to use `ngrok` tunneling. This will provide us with secure HTTPS connection which will then allow us to interface hardware (device's camera specifically). Because of this, you cannot simply connect to the server using local address, but you will have to use address from the output in terminal (once the server is started).

The address will look something like: `http://7a63-188-252-187-35.ngrok.io2-187-35.ngrok.io/`. This link will forward your connection to [ngrok](https://ngrok.com/) server and forward back to your local machine. This makes our application accessible form anywhere in the world AND makes it use secure connection. The only downside is the abstract link which we receive which will change upon every server restart.
