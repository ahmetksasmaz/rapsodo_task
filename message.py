class Bbox:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Metadata:
    ball_bbox = None
    ball_2d_points = None
    ball_2d_center = None
    ball_3d_points = None
    ball_3d_center = None
    ball_3d_points_speed_vectors = None
    ball_avg_3d_speed_vector = None
    
    gt_ball_bbox = None
    gt_ball_2d_points = None
    gt_ball_2d_center = None
    
    gt_ball_bbox_iou = None # Intersection over Union of measures and ground truth
    gt_ball_2d_points_symmetric_difference_error = None # Number of elements of symmetric difference set of measures and ground truth divided by number of elements of ground truth
    gt_ball_2d_center_error = None # Euclidean distance between measures and ground truth

class Message:
    image = None
    message_id = None
    metadata = Metadata()
    
    def __init__(self, message_id, image):
        self.message_id = message_id
        self.image = image