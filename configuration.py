import yaml

class Configuration:
    # Camera Parameters
    camera_fps = None
    camera_pixel_size = None
    camera_width = None
    camera_height = None
    camera_focal_length = None
    
    # Ball Parameters
    ball_radius = None
    
    # Setup Parameters
    camera_upward_tilt_angle = None
    initial_distance_between_camera_and_ball = None
    
    # Strategy Parameters
    ball_detector_strategy = None
    world_coordinate_estimator_strategy = None
    speed_vector_estimator_strategy = None
    
    # Ball Detector Parameters
    ball_detector_yolov8_model_size = None
    ball_detector_ball_class_id = None

    # Ball Tracker Parameters
    ball_detector_initial_search_region_bbox = None
    ball_detector_history_depth = None
    ball_detector_bbox_size_multiplier = None
    
    # World Coordinate Estimator Parameters
    world_coordinate_estimator_dummy_parameter = None

    # Speed Vector Estimator Parameters
    speed_vector_estimator_history_depth = None
    
    # Experiment parameters
    output_file_path = None
    
    def __init__(self, configuration_file_path):
        self.configuration_file_path = configuration_file_path
        
        with open(configuration_file_path, 'r') as stream:
            config_data = yaml.safe_load(stream)
                        
            self.camera_fps = config_data['camera']['fps']
            self.camera_pixel_size = config_data['camera']['pixel_size']
            self.camera_width = config_data['camera']['width']
            self.camera_height = config_data['camera']['height']
            self.camera_focal_length = config_data['camera']['focal_length']
            
            self.ball_radius = config_data['ball']['radius']
            
            self.camera_upward_tilt_angle = config_data['setup']['camera_upward_tilt_angle']
            self.initial_distance_between_camera_and_ball = config_data['setup']['initial_distance_between_camera_and_ball']
            
            self.ball_detector_strategy = config_data['strategy']['ball_detector']
            self.world_coordinate_estimator_strategy = config_data['strategy']['world_coordinate_estimator']
            self.speed_vector_estimator_strategy = config_data['strategy']['speed_vector_estimator']
            
            self.ball_detector_yolov8_model_size = config_data['ball_detector']['yolov8_model_size']
            self.ball_detector_ball_class_id = config_data['ball_detector']['ball_class_id']
            self.ball_detector_initial_search_region_bbox = config_data['ball_detector']['initial_search_region_bbox']
            self.ball_detector_history_depth = config_data['ball_detector']['history_depth']
            self.ball_detector_bbox_size_multiplier = config_data['ball_detector']['bbox_size_multiplier']
            self.world_coordinate_estimator_dummy_parameter = config_data['world_coordinate_estimator']['dummy_parameter']
            self.speed_vector_estimator_history_depth = config_data['speed_vector_estimator']['history_depth']
            
            self.output_file_path = config_data['experiment']['output_file_path']