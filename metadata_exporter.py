import os

class MetadataExporter:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path
        os.remove(self.output_file_path)
    
    def process(self, message):
        message_id = message.message_id
        metadata = message.metadata
        
        
        with open(self.output_file_path, 'a') as output_file:
            output_file.write(str(message_id) + "\t")
            output_file.write(str(metadata.ball_avg_3d_speed_vector.x) + "\t")
            output_file.write(str(metadata.ball_avg_3d_speed_vector.y) + "\t")
            output_file.write(str(metadata.ball_avg_3d_speed_vector.z) + "\t")
            output_file.write(str(metadata.gt_ball_bbox_iou) + "\t")
            output_file.write(str(metadata.gt_ball_2d_points_symmetric_difference_error) + "\t")
            output_file.write(str(metadata.gt_ball_2d_center_error) + "\n")