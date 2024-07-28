import cv2 as cv
import message
import numpy as np

class DefaultBallTrackerStrategy:
    def __init__(self, configuration):
        self.configuration = configuration

    def process(self, bboxes):
        print(bboxes)
        if len(bboxes) == 0:
            return None
        else:
            return bboxes[0]