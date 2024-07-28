import cv2 as cv
import message
from ultralytics import YOLO
import numpy as np

class DefaultBallDetectorStrategy:
    def __init__(self, configuration):
        self.configuration = configuration
        self.model = YOLO('yolov8'+configuration.ball_detector_yolov8_model_size+'.pt')

    def process(self, image):
        # results = self.model.track(image, persist=True, show=True, conf=0.001)
        results = self.model.predict(image)
        results = results[0].cpu()
        ball_result_indices = []
        index = 0
        for cls in results.boxes.cls:
            if int(cls) == self.configuration.ball_detector_ball_class_id:
                ball_result_indices.append(index)
            index += 1
        
        bboxes = []
        
        for ball_result_index in ball_result_indices:
            result_bbox = results.boxes.xywh[ball_result_index]
            x = result_bbox[0].numpy()
            y = result_bbox[1].numpy()
            w = result_bbox[2].numpy()
            h = result_bbox[3].numpy()
            
            x -= w / 2
            y -= h / 2
            
            x = max(0,min(x, image.shape[1]))
            y = max(0,min(y, image.shape[0]))
            
            if x + w >= image.shape[1]:
                w = image.shape[1] - x
                
            if y + h >= image.shape[0]:
                h = image.shape[0] - y
                
            bboxes.append(message.Bbox(x, y, w, h))
        
        return bboxes