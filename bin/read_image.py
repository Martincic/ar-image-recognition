from importlib.machinery import SOURCE_SUFFIXES
import cv2 as cv
import time
import sys
import os
import timeit


MIN_MATCHES = 15

WINDOW_NAME = "test window"

workingDir = os. getcwd()+'/'

good = 0
bad = 0

# To read image from disk, we use
# cv2.imread function, in below method,

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
    # Match frame descriptors with model descriptors
    matches = bf.match(des_model, des_frame)
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

def test_function():
    focus = '../static/nodes/front_frames/'
    back_frame = '../static/nodes/focus/'

    sum_hit = 0
    sum_all = 0
    counter = 0
    for input in os.listdir(workingDir + back_frame):
        max = 0
        max_model = 'None'
        sample_img = cv.imread(workingDir + back_frame + input) #param2 0 for black and white
        
        for model in os.listdir(workingDir + focus):
            counter = counter+1
            output_img = cv.imread(workingDir + focus + model)
            temp = compare_images(sample_img, output_img)

            if temp > max:
                max = temp
                max_model = model
            sum_all = sum_all + temp
        draw_matches(path1=workingDir + back_frame + input,path2=workingDir + focus + max_model)
        print('MAX FROM FIRST: '+str(max))
        sum_hit = sum_hit + max
        print('Input: '+input)
        print('Model:' +max_model)
        print(max)

    print('Average matches: ' + str(sum_all/counter))
    print('Average hits: ' + str(sum_hit/31))
    # printing the execution time

    # # find the keypoints with ORB (no compute)
    # kp = orb.detect(img, None)

    # # compute the descriptors with ORB
    # kp, des = orb.compute(img, kp)

    # # draw only keypoints location,not size and orientation
    # img2 = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    # cv.imshow(WINDOW_NAME,img2)
    # # cv.imshow(WINDOW_NAME, img) 
t = timeit.timeit(lambda: test_function(), number=1)
print(t)

print('TOTAL GOOD MATCHES: '+str(good))
print('TOTAL BAD MATCHES: '+str(bad))

