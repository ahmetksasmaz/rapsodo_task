class Bbox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.w}, {self.h})'

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

class Metadata:
    ball_bboxes = None
    ball_target_bbox = None
    ball_3d_center = None
    ball_avg_3d_speed_vector = None
    
    gt_ball_bbox = None
    
    gt_ball_bbox_iou = None # Intersection over Union of measures and ground truth

class Message:
    image = None
    message_id = None
    metadata = Metadata()
    
    def __init__(self, message_id, image):
        self.message_id = message_id
        self.image = image