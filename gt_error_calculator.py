import message

class GroundTruthErrorCalculator:
    def __init__(self):
        pass
    
    def process(self, msg):
        metadata = msg.metadata
        metadata.gt_ball_bbox_iou = self.__calculate_iou(metadata.ball_target_bbox, metadata.gt_ball_bbox)
        
    def __calculate_iou(self, bbox, gt_bbox):
        if not gt_bbox:
            return 0.0
        x1 = max(bbox.x, gt_bbox.x)
        y1 = max(bbox.y, gt_bbox.y)
        x2 = min(bbox.x + bbox.w, gt_bbox.x + gt_bbox.w)
        y2 = min(bbox.y + bbox.h, gt_bbox.y + gt_bbox.h)
        
        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        union = bbox.w * bbox.h + gt_bbox.w * gt_bbox.h - intersection
        
        return intersection / union