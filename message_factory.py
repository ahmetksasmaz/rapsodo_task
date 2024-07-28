import cv2 as cv
import message
import os
import numpy as np

class MessageFactory:
    def __init__(self, image_directory_path, image_regex, file_number_starting_index, ground_truth_mask_directory_path, ground_truth_mask_regex, ground_truth_mask_index):
        self.image_directory_path = image_directory_path
        self.image_regex = image_regex
        self.image_index = file_number_starting_index
        self.ground_truth_mask_directory_path = ground_truth_mask_directory_path
        self.ground_truth_mask_regex = ground_truth_mask_regex
        self.ground_truth_mask_index = ground_truth_mask_index
        
    def next_message(self):
        if os.path.isfile(self.image_directory_path + '/' + self.image_regex % self.image_index) == False:
            return None
        image = cv.imread(self.image_directory_path + '/' + self.image_regex % self.image_index)
        if image is None:
            return None
        
        if os.path.isfile(self.ground_truth_mask_directory_path + '/' + self.ground_truth_mask_regex % self.ground_truth_mask_index) == False:
            return None
        
        ground_truth_mask = cv.imread(self.ground_truth_mask_directory_path + '/' + self.ground_truth_mask_regex % self.ground_truth_mask_index, cv.IMREAD_GRAYSCALE)
        if ground_truth_mask is None:
            return None
        
        gt_ball_bbox = self.__gt_metadata_extract(ground_truth_mask)
        
        msg = message.Message(self.image_index, image)
        msg.metadata.gt_ball_bbox = gt_ball_bbox
        
        self.image_index += 1
        self.ground_truth_mask_index += 1
        return msg

    def __gt_metadata_extract(self, ground_truth_mask):
        pts = np.where(ground_truth_mask == 255)
        x = pts[1]
        y = pts[0]
        ball_bbox = message.Bbox(min(x), min(y), max(x) - min(x), max(y) - min(y))
        return ball_bbox