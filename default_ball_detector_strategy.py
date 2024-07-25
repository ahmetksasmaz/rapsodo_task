import cv2 as cv
import message

class DefaultBallDetectorStrategy:
    def __init__(self):
        pass
    def process(self, image):
        bbox = message.Bbox(0,0,10,10)
        points_2d = [message.Point2D(0,0), message.Point2D(1,1), message.Point2D(2,2)]
        center_2d = message.Point2D(1,1)
        return bbox, points_2d, center_2d