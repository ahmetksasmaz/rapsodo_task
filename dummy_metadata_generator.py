import message

class DummyMetadataGenerator:
    def __init__(self):
        pass
    def __generate_metadata(self):
        metadata = message.Metadata()
        metadata.ball_bbox = message.Bbox(0, 0, 10, 10)
        metadata.ball_2d_points = [message.Point2D(0, 0), message.Point2D(1, 1), message.Point2D(2, 2)]
        metadata.ball_2d_center = message.Point2D(1, 1)
        metadata.ball_3d_points = [message.Point3D(0, 0, 0), message.Point3D(1, 1, 1), message.Point3D(2, 2, 2)]
        metadata.ball_3d_center = message.Point3D(1, 1, 1)
        metadata.ball_3d_points_speed_vectors = [message.Point3D(0, 0, 0), message.Point3D(1, 1, 1), message.Point3D(2, 2, 2)]
        metadata.ball_avg_3d_speed_vector = message.Point3D(1, 1, 1)
        
        metadata.gt_ball_bbox = message.Bbox(0, 0, 10, 10)
        metadata.gt_ball_2d_points = [message.Point2D(0, 0), message.Point2D(1, 1), message.Point2D(2, 2)]
        metadata.gt_ball_2d_center = message.Point2D(1, 1)
        return metadata
    
    def process(self, message):
        message.metadata = self.__generate_metadata()