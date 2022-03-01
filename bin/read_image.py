from importlib.machinery import SOURCE_SUFFIXES
from random import sample
import cv2 as cv
import os
import matcher

MIN_MATCHES = 15

workingDir = os. getcwd()+'\\'

# To read image from disk, we use
# cv2.imread function, in below method,

def test_function():
    back_frame = '..\\static\\nodes\\back_frames\\'
    focus = '..\\static\\nodes\\specific_elements\\'

    for input in os.listdir(workingDir + back_frame):
        print(workingDir + back_frame+input)
        max = 0
        max_model = 'None'
        sample_img = cv.imread(workingDir + back_frame + input) #param2 0 for black and white
        scoring = {}
        for model in os.listdir(workingDir + focus):
            print(workingDir + focus + model)
            output_img = cv.imread(workingDir + focus + model)
            score = matcher.compare_images(sample_img, output_img)
            matcher.compare_templates(sample_img, output_img)

            scoring[model] = score
            if score > max:
                max = score
                max_model = model
                
        new_sorted_dict = dict(sorted(scoring.items(), key=lambda item: item[1], reverse=True))
        print(new_sorted_dict)
        matcher.draw_matches(path1=workingDir + back_frame + input,path2=workingDir + focus + max_model)

    # printing the execution time

    # # find the keypoints with ORB (no compute)
    # kp = orb.detect(img, None)

    # # compute the descriptors with ORB
    # kp, des = orb.compute(img, kp)

    # # draw only keypoints location,not size and orientation
    # img2 = cv.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    # cv.imshow(WINDOW_NAME,img2)
    # # cv.imshow(WINDOW_NAME, img) 
test_function()

