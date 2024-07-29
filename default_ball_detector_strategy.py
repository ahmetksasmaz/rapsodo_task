import cv2 as cv
import message
from ultralytics import YOLO
import numpy as np

class DefaultBallDetectorStrategy:
    def __init__(self, configuration):
        self.configuration = configuration
        self.model = YOLO('yolov8'+configuration.ball_detector_yolov8_model_size+'.pt')
        search_bbox = configuration.ball_detector_initial_search_region_bbox
        self.next_search_region_bbox = message.Bbox(search_bbox[0], search_bbox[1], search_bbox[2], search_bbox[3])
        self.history_depth = configuration.ball_detector_history_depth
        self.bbox_size_multiplier = configuration.ball_detector_bbox_size_multiplier
        self.bbox_history = []

    def process(self, image):
        # results = self.model.track(image, persist=True, show=True, conf=0.001)
        crop_borders_x0 = max(0, int(self.next_search_region_bbox.x))
        crop_borders_y0 = max(0, int(self.next_search_region_bbox.y))
        crop_borders_x1 = min(image.shape[1], int(self.next_search_region_bbox.x + self.next_search_region_bbox.w))
        crop_borders_y1 = min(image.shape[0], int(self.next_search_region_bbox.y + self.next_search_region_bbox.h))
        cropped_image = image[crop_borders_y0:crop_borders_y1, crop_borders_x0:crop_borders_x1]
        results = self.model.predict(cropped_image)
        results = results[0].cpu()
        ball_result_index = -1
        index = 0
        for cls in results.boxes.cls:
            if int(cls) == self.configuration.ball_detector_ball_class_id:
                ball_result_index = index
            index += 1
        
        if ball_result_index == -1:
            return None
        
        result_bbox = results.boxes.xywh[ball_result_index]
        x = result_bbox[0].numpy() + crop_borders_x0
        y = result_bbox[1].numpy() + crop_borders_y0
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
            
        bbox = message.Bbox(x, y, w, h)
        
        # Append ball bbox to history
        self.bbox_history.append(bbox)
        # Remove oldest bbox from history if history is full
        if len(self.bbox_history) > self.history_depth:
            self.bbox_history.pop(0)

        if len(self.bbox_history) == 1:
            x_center_speed = 0
            y_center_speed = 0
            w_speed = 0
            h_speed = 0
        else:
            x_center_speed = (self.bbox_history[-1].x + self.bbox_history[-1].w / 2 - self.bbox_history[0].x - self.bbox_history[0].w) / len(self.bbox_history)
            y_center_speed = (self.bbox_history[-1].y + self.bbox_history[-1].h / 2 - self.bbox_history[0].y - self.bbox_history[0].h) / len(self.bbox_history)
            w_speed = (self.bbox_history[-1].w - self.bbox_history[0].w) / len(self.bbox_history)
            h_speed = (self.bbox_history[-1].h - self.bbox_history[0].h) / len(self.bbox_history)
        
        # Estimate center of the ball in the next frame
        # Estimate size of the ball in the next frame
        self.next_search_region_bbox.x = self.bbox_history[-1].x + self.bbox_history[-1].w / 2 + x_center_speed
        self.next_search_region_bbox.y = self.bbox_history[-1].y + self.bbox_history[-1].h / 2 + y_center_speed
        self.next_search_region_bbox.w = self.bbox_history[-1].w + w_speed
        self.next_search_region_bbox.h = self.bbox_history[-1].h + h_speed
        
        # Expand bbox by specified percentage to make sure the ball is inside the bbox
        self.next_search_region_bbox.w *= self.bbox_size_multiplier
        self.next_search_region_bbox.h *= self.bbox_size_multiplier
        
        self.next_search_region_bbox.x -= self.next_search_region_bbox.w / 2
        self.next_search_region_bbox.y -= self.next_search_region_bbox.h / 2
        
        
        return bbox