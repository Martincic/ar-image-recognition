from importlib.machinery import SOURCE_SUFFIXES
import cv2 as cv
import time
import sys
import os
import socket
import struct

address = ("192.168.0.32", 8080)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(1000)


client, addr = s.accept()
# print ('got connected from %s' % addr)

buf = ''
while len(buf)<4:
    buf += client.recv(4-len(buf))
size = struct.unpack('!i', buf)
print ("receiving %s bytes" % size)

with open('tst.jpg', 'wb') as img:
    while True:
        data = client.recv(1024)
        if not data:
            break
        img.write(data)
print ('received, yay!')

client.close()






exit()

MIN_MATCHES = 130
font = cv.FONT_HERSHEY_SIMPLEX 
WINDOW_NAME = "AR Image Recognition"
workingDir = os. getcwd()+'/'


def rescaleFrame(frame, scale=0.75):
    # frame.shape[1] is width of the image
    width = int(frame.shape[1] * scale)

    # frame.shape[0] is height of the image
    height = int(frame.shape[0] * scale)

    return cv.resize(frame, (width,height), interpolation=cv.INTER_AREA)


# Capture photo to be used as model
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    # gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    if cv.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
        cv.imwrite('static/img/models/capture.png',frame)
        break

    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

# To read image from disk, we use
# cv2.imread function, in below method,

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    k = cv.waitKey(1)
    # CLOSE ON 'q'
    if k == ord("q"):
        # delete created window from screen
        cap.release()
        cv.destroyAllWindows()

    # sample_img = cv.imread(workingDir + 'static/img/models/'+model) #param2 0 for black and white
    sample_img = cv.imread(workingDir + 'static/img/models/capture.png')
    # output_img = cv.imread(workingDir + 'static/img/samples/'+filename)
    output_img = frame
    if sample_img is None: sys.exit("..no sample image found")
    if output_img is None: sys.exit("..no output image found")

    # border, random img decoration shit
    # img = cv.copyMakeBorder(img, 10, 10, 10, 10, cv.BORDER_CONSTANT, None, value = 0)

    # window, second param by default WINDOW_AUTOSIZE
    cv.namedWindow(WINDOW_NAME)

    #works without time and threads, but errors in closing 
    start = time.time()
    cv.startWindowThread()

    # Initiate ORB detector
    orb = cv.ORB_create()

    # create brute force  matcher object
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    # Compute model keypoints and its descriptors
    kp_model, des_model = orb.detectAndCompute(sample_img, None)  
    # Compute scene keypoints and its descriptors
    kp_frame, des_frame = orb.detectAndCompute(output_img, None)
    # Match frame descriptors with model descriptors
    try:
        matches = bf.match(des_model, des_frame)
    except:
        print('Error... Ignoring...')
        break
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > MIN_MATCHES:
        # draw first 15 matches.
        
        output_img = cv.drawMatches(sample_img, kp_model, output_img, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        
        
        cv.putText(output_img, "Static model", (30, 30), font, 1, (255, 25, 25), 1, cv.LINE_AA)
        cv.putText(output_img, "WebCam ("+str(len(matches))+" matches)", (700, 30), font, 1, (255, 25, 25), 1, cv.LINE_AA)

        # resized_img = rescaleFrame(output_img, 0.5)
        # show result 
        cv.imshow(WINDOW_NAME, output_img)
        time.sleep(2)
        # if param 0 wait forever
    else:
        print("Not enough matches have been found - %d/%d" % (len(matches),
                                                            MIN_MATCHES))


    # # find the keypoints with ORB (no compute)
    # kp = orb.detect(img, None)

    # # compute the descriptors with ORB
    # kp, des = orb.compute(img, kp)

    # # draw only keypoints location,not size and orientation
    # img2 = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    # cv.imshow(WINDOW_NAME,img2)
    # # cv.imshow(WINDOW_NAME, img)
