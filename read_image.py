from importlib.machinery import SOURCE_SUFFIXES
import cv2 as cv
import time
import sys
import os

MIN_MATCHES = 15

WINDOW_NAME = "test window"

workingDir = os. getcwd()+'/'

# To read image from disk, we use
# cv2.imread function, in below method,

for model in os.listdir(workingDir + 'static/img/models'):
    for filename in os.listdir(workingDir + 'static/img/samples'):
        sample_img = cv.imread(workingDir + 'static/img/models/'+model) #param2 0 for black and white
        output_img = cv.imread(workingDir + 'static/img/samples/'+filename)
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
        matches = bf.match(des_model, des_frame)
        # Sort them in the order of their distance
        matches = sorted(matches, key=lambda x: x.distance)

        if len(matches) > MIN_MATCHES:
            # draw first 15 matches.
            output_img = cv.drawMatches(sample_img, kp_model, output_img, kp_frame,
                                matches[:MIN_MATCHES], 0, flags=2)
            # show result
            cv.imshow(WINDOW_NAME, output_img)
            # if param 0 wait forever
            k = cv.waitKey(0)

            # CLOSE ON 'q'
            if k == ord("q"):
                # delete created window from screen
                cv.destroyAllWindows()
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