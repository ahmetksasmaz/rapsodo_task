import message

class GroundTruthErrorCalculator:
    def __init__(self):
        pass
    
    def process(self, msg):
        metadata = msg.metadata
        metadata.gt_ball_bbox_iou = self.__calculate_iou(metadata.ball_bbox, metadata.gt_ball_bbox)
        metadata.gt_ball_2d_points_symmetric_difference_error = self.__calculate_symmetric_difference_error(metadata.ball_2d_points, metadata.gt_ball_2d_points)
        metadata.gt_ball_2d_center_error = self.__calculate_center_error(metadata.ball_2d_center, metadata.gt_ball_2d_center)
        
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
    
    def __calculate_symmetric_difference_error(self, points, gt_points):
        if not gt_points:
            return 1.0
        set_points = set((point.x, point.y) for point in points)
        set_gt_points = set((gt_point.x, gt_point.y) for gt_point in gt_points)
        symmetric_difference = set_points.symmetric_difference(set_gt_points)
        return len(symmetric_difference) / len(set_gt_points)
    
    def __calculate_center_error(self, point, gt_point):
        if not gt_point:
            return float("inf")
        return ((point.x - gt_point.x) ** 2 + (point.y - gt_point.y) ** 2) ** 0.5