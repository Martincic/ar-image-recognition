from importlib.machinery import SOURCE_SUFFIXES
from random import sample
import cv2 as cv
import time
import sys

WINDOW_NAME = "test window"
MIN_MATCHES = 15

def compare_images(sample, output, draw=False):
    if sample is None: sys.exit("..no sample image found")
    if output is None: sys.exit("..no output image found")

    # Initiate ORB detector
    orb = cv.ORB_create()

    # create brute force  matcher object
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    # Compute model keypoints and its descriptors
    kp_model, des_model = orb.detectAndCompute(sample, None)  
    # Compute scene keypoints and its descriptors
    kp_frame, des_frame = orb.detectAndCompute(output, None)
    matches = 0
    # Match frame descriptors with model descriptors
    if des_model is not None and des_frame is not None:
        matches = bf.match(des_model, des_frame)
    else: 
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        return matches
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)

    return len(matches)

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv.resize(image, dim, interpolation=inter)


def draw_matches(path1, path2):
        sample_img = ResizeWithAspectRatio(cv.imread(path1), height=600) #param2 0 for black and white
        output_img = ResizeWithAspectRatio(cv.imread(path2), height=600) 
        if sample_img is None: sys.exit("..no sample image found")
        if output_img is None: sys.exit("..no output image found")
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

        
        # draw first 15 matches.
        output_img = cv.drawMatches(sample_img, kp_model, output_img, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        print("FROM SECOND: "+str(len(matches)))
        # show result
        cv.imshow(WINDOW_NAME, output_img)
        # if param 0 wait forever
        k = cv.waitKey(0)

        # CLOSE ON 'e'
        if k == ord("e"):
            # delete created window from screen
            global good
            good = good + 1
            cv.destroyAllWindows()
        # CLOSE ON 'q'
        if k == ord("q"):
            global bad 
            bad = bad + 1
            # delete created window from screen
            cv.destroyAllWindows()
        
        else:
            print("Not enough matches have been found - %d/%d" % (len(matches),
                                                                MIN_MATCHES))

def pixelize(input):
    # Get input size
    height, width = input.shape[:2]

    # Desired "pixelated" size
    w, h = (16, 16)

    # Resize input to "pixelated" size
    temp = cv.resize(input, (w, h), interpolation=cv.INTER_LINEAR)

    # Initialize output image
    output = cv.resize(temp, (width, height), interpolation=cv.INTER_NEAREST)

def compare_templates(img1, img2):
    img = img1
    template = img2
    h, w, _ = template.shape

    # methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR,
    #             cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]

    # for method in methods:
    img2 = img.copy()

    result = cv.matchTemplate(img2, template, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        # location = min_loc
    # else:
    location = max_loc

    bottom_right = (location[0] + w, location[1] + h)    
    cv.rectangle(img2, location, bottom_right, 255, 5)
    cv.imshow('Match', img2)
    cv.imshow('Template', template)
    cv.waitKey(0)
    cv.destroyAllWindows()