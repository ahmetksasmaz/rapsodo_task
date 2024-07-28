import cv2 as cv

class MetadataPrinter:
    def __init__(self, expand_lists = False):
        self.expand_lists = expand_lists
        
    def process(self, message):
        message_id = message.message_id
        image = message.image
        metadata = message.metadata
        
        # image = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        # image[int(metadata.ball_2d_center.x)][int(metadata.ball_2d_center.y)][:] = [0,255,255]
        # image[metadata.ball_bbox.y, metadata.ball_bbox.x:metadata.ball_bbox.x + metadata.ball_bbox.w, metadata.ball_bbox.y + metadata.ball_bbox.h] = 255
        
        cv.imwrite('output_images_' + str(message_id) + '.png', image)
        
        print("#######################################")
        print("Start of Message ID : ", "\t>>>>>>>>>", str(message_id), "<<<<<<<<<")
        print("Ball Bounding Box [x,y,w,h] : ", "[", str(metadata.ball_bbox.x), ",", str(metadata.ball_bbox.y), ",", str(metadata.ball_bbox.w), ",", str(metadata.ball_bbox.h), "]")
        print("Ball 2D Points [x,y] : ")
        if self.expand_lists:
            for point in metadata.ball_2d_points:
                print("\t", "[", str(point.x), ",", str(point.y), "]")
        else:
            print("\t", "...")
        print("Ball 2D Center [x,y] : ", "[", str(metadata.ball_2d_center.x), ",", str(metadata.ball_2d_center.y), "]")
        print("Ball 3D Points [x,y,z] : ")
        if self.expand_lists:
            for point in metadata.ball_3d_points:
                print("\t", "[", str(point.x), ",", str(point.y), ",", str(point.z), "]")
        else:
            print("\t", "...")
        print("Ball 3D Center [x,y,z] : ", "[", str(metadata.ball_3d_center.x), ",", str(metadata.ball_3d_center.y), ",", str(metadata.ball_3d_center.z), "]")
        print("Ball 3D Points Speed Vectors [x,y,z] : ")
        if self.expand_lists:
            for vector in metadata.ball_3d_points_speed_vectors:
                print("\t", "[", str(vector.x), ",", str(vector.y), ",", str(vector.z), "]")
        else:
            print("\t", "...")
        print("Ball Average 3D Speed Vector [x,y,z] : ", "[", str(metadata.ball_avg_3d_speed_vector.x), ",", str(metadata.ball_avg_3d_speed_vector.y), ",", str(metadata.ball_avg_3d_speed_vector.z), "]")
        
        print("Ground Truth Ball Bbox IOU : ", metadata.gt_ball_bbox_iou)
        print("Ground Truth 2D Points Symmetric Difference Error : ", metadata.gt_ball_2d_points_symmetric_difference_error)
        print("Ground Truth 2D Center Displacement Error : ", metadata.gt_ball_2d_center_error)
                
        print("End of Message ID : ", "\t>>>>>>>>>", str(message_id), "<<<<<<<<<")
        print("#######################################")