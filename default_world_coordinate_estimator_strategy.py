import message

class DefaultWorldCoordinateEstimatorStrategy:
    def __init__(self, configuration):
        self.configuration = configuration

    def process(self, bbox, points_2d, center_2d):
        points_3d = [message.Point3D(0,0,0), message.Point3D(1,1,1), message.Point3D(2,2,2)]
        center_3d = message.Point3D(1,1,1)
        return points_3d, center_3d