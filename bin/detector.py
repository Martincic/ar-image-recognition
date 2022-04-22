import torch
import numpy as np
import cv2
from time import time
import os

class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using OpenCV.
    """
    
    def __init__(self):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        """
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'


    def get_video_from_url(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        return cv2.VideoCapture('video3.mp4')


    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        model = torch.hub.load(os.getcwd()+'/yolov5', 'custom', path='best.pt', source='local')  # local repo

        return model


    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
     
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        
        self.json = results.pandas().xyxy[0].to_json()
        return labels, cord


    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]


    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.2:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def toJson(self, file):
        img = cv2.imread(file)
        try:
            self.score_frame(img)
        except:
            return "{}"
        return self.json

    def load_images_from_folder(self, folder):
        images = []
        for filename in os.listdir(folder):
            images.append(folder+filename)
        return images

    def predict_dot(self, predictions):
        dots = {
            '1':0,
            '2':0,
            '3':0,
            '4':0,
            '5':0,
            '6':0,
            '7':0,
            '8':0,
        }
        for room in predictions:
            dot = ''
            print(room)
            if room == '16' or room == '15' or room == '13':
                dot = '1'
            elif room == '19':
                dot = '2'
            elif room == '1':
                dot = '3'
            elif room == '9' or room == '10' or room == '11' or room == '8':
                dot = '4'
            elif room == '4' or room == '3' or room == '2':
                dot = '5'
            elif room == '5' or room == '7':
                dot = '6'
            elif room == '6':
                dot = '7'
            elif room == '27':
                dot = '8'
            elif room == 'lab' or room == 'paw':
                continue

            dots[dot] += predictions[room]['confidence']
        return max(dots, key=dots.get)




    # def __call__(self):
    #     """
    #     This function is called when class is executed, it runs the loop to read the video frame by frame,
    #     and write the output into a new file.
    #     :return: void
    #     """
    #     player = self.get_video_from_url()
    #     assert player.isOpened()
    #     x_shape = int(player.get(cv2.CAP_PROP_FRAME_WIDTH))
    #     y_shape = int(player.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     four_cc = cv2.VideoWriter_fourcc(*"MJPG")
    #     out = cv2.VideoWriter(self.in_file, four_cc, 20, (x_shape, y_shape))
    #     while True:
    #         start_time = time()
    #         ret, frame = player.read()
    #         if not ret:
    #             break
    #         frame = self.plot_boxes(results, frame)
    #         end_time = time()
    #         fps = 1/np.round(end_time - start_time, 3)
    #         out.write(frame)

# Create a new object and execute.
# detection = ObjectDetection("video3.avi")
# detection()
