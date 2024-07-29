import cv2 as cv

class MetadataPrinter:
    def __init__(self, expand_lists = False):
        self.expand_lists = expand_lists
        
    def process(self, message):
        message_id = message.message_id
        image = message.image
        metadata = message.metadata
        image[int(metadata.ball_bbox.y + metadata.ball_bbox.h / 2)][int(metadata.ball_bbox.x + metadata.ball_bbox.w / 2)][:] = [0,255,255]
        cv.rectangle(image, (int(metadata.ball_bbox.x), int(metadata.ball_bbox.y)), (int(metadata.ball_bbox.x + metadata.ball_bbox.w), int(metadata.ball_bbox.y + metadata.ball_bbox.h)), (0,255,0), 2)
        
        cv.imwrite('output_images_' + str(message_id) + '.png', image)
        
        print("#######################################")
        print("Start of Message ID : ", "\t>>>>>>>>>", str(message_id), "<<<<<<<<<")
        print("Ball Bounding Box [x,y,w,h] : ", "[", str(metadata.ball_bbox.x), ",", str(metadata.ball_bbox.y), ",", str(metadata.ball_bbox.w), ",", str(metadata.ball_bbox.h), "]")
        print("Ball 3D Center [x,y,z] : ", "[", str(metadata.ball_3d_center.x), ",", str(metadata.ball_3d_center.y), ",", str(metadata.ball_3d_center.z), "]")
        print("Ball Average 3D Speed Vector [x,y,z] : ", "[", str(metadata.ball_avg_3d_speed_vector.x), ",", str(metadata.ball_avg_3d_speed_vector.y), ",", str(metadata.ball_avg_3d_speed_vector.z), "]")
        
        print("Ground Truth Ball Bbox IOU : ", metadata.gt_ball_bbox_iou)
                
        print("End of Message ID : ", "\t>>>>>>>>>", str(message_id), "<<<<<<<<<")
        print("#######################################")