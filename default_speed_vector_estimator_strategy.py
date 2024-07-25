import message

class DefaultSpeedVectorEstimatorStrategy:
    def __init__(self):
        pass
    def process(self, points_3d, center_3d):
        speed_vectors = [message.Point3D(0,0,0), message.Point3D(1,1,1), message.Point3D(2,2,2)]
        avg_speed_vector = message.Point3D(1,1,1)
        return speed_vectors, avg_speed_vector