import message
import cv2 as cv
import math
import numpy as np

class DefaultWorldCoordinateEstimatorStrategy:
    def __init__(self, configuration):
        self.configuration = configuration
        # Transformation from world coordinates to pixel coordinates
        # World coordinate to camera coordinate
        #
        #   Our world coordinate system is like this:
        #       origin: center of projection
        #       x+: the same direction with the camera's right 
        #       y+: towards the ground
        #       z+: the same direction with the camera's looking direction but parallel to the ground
        #
        #   Our camera coordinate system is like this:
        #       origin: center of projection
        #       x+: the same direction with the camera's right
        #       y+: orthogonal to y and z axis, parallel to image plane, towards the ground
        #       z+: optical axis with the same direction with the camera's looking direction
        #
        #   Rotation & Translation
        #
        #   Due to world coordinate origin and camera coordinate origin intersects
        #   Translation matrix will be [0,0,0]^T
        #
        #   And the camera is tilted only upwards sky 10 degrees
        #   Rotation matrix will be Rx(pi/18) according to our coordinate system
        #   Rx(pi/18) = [1, 0, 0; 0, cos(pi/18), -sin(pi/18); 0, sin(pi/18), cos(pi/18)]
        #   Transform matrix = [Rx(pi/18), [0,0,0]^T]
        #
        # Camera coordinate to image plane coordinate
        #
        #   Our image plane is parallel to the camera coordinate system's y-x plane
        #   Our image plane axes are named as u and v
        #   u+ is the same direction with x+ axis of camera coordinate
        #   v+ is the same direction with y+ axis of camera coordinate
        #   Focal length is 0.008 meters
        #   Pixel pitch is 0.0000048 meters
        #   And the origin of the image plane is shifted negative by 512 x (Pixel Pitch) on u axis and 640 x (Pixel Pitch) on v axis
        #   Projection matrix will be [0.008, 0, 512 x (Pixel Pitch); 0, 0.008, 640 x (Pixel Pitch); 0, 0, 1]
        # 
        # Image plane coordinate to pixel coordinate
        #   Our pixel coordinate system is like this:
        #       origin: u,v origin of the image plane
        #       u+: the same direction with u axis of the image plane
        #       v+: the same direction with v axis of the image plane
        #   Pixel pitch is 0.0000048 meters
        #   Our transformation matrix will be [1/(Pixel Pitch), 0, 0; 0, 1/(Pixel Pitch), 0; 0, 0, 1]
        #
        # Instead of multiplying pixel pitch and dividing again, we can directly multiply 1/(Pixel Pitch) with the focal length
        # and pixel pitch multipliers in the original projection matrix will cancelled out and we will have a single focal length
        # divided by pixel pitch
        #
        # Our new projection matrix will be [f/(Pixel Pitch), 0, 512; 0, f/(Pixel Pitch), 640; 0, 0, 1]
        # Our transform matrix was [Rx(pi/18), [0,0,0]^T]
        # Multiplying these two matrices will give us the final transformation matrix
        
        self.focal_length = self.configuration.camera_focal_length
        self.width = self.configuration.camera_width
        self.height = self.configuration.camera_height
        self.pixel_size = self.configuration.camera_pixel_size
        self.camera_tilt_angle = self.configuration.camera_upward_tilt_angle
        self.initial_distance_between_camera_and_ball = self.configuration.initial_distance_between_camera_and_ball
        self.ball_radius = self.configuration.ball_radius
        
        self.rotation_matrix = np.zeros((3, 3), dtype = "float32")
        self.translation_matrix = np.zeros((3, 1), dtype = "float32")
        
        self.transform_matrix = np.zeros((3, 4), dtype = "float32")
        self.project_matrix = np.zeros((3, 3), dtype = "float32")
        
        self.transform_matrix[0,0] = 1
        self.transform_matrix[0,1] = 0
        self.transform_matrix[0,2] = 0
        self.transform_matrix[1,0] = 0
        self.transform_matrix[1,1] = math.cos(math.pi * self.camera_tilt_angle / 180)
        self.transform_matrix[1,2] = math.sin(math.pi * self.camera_tilt_angle / 180)
        self.transform_matrix[2,0] = 0
        self.transform_matrix[2,1] = -math.sin(math.pi * self.camera_tilt_angle / 180)
        self.transform_matrix[2,2] = math.cos(math.pi * self.camera_tilt_angle / 180)
        
        self.transform_matrix[0,3] = 0
        self.transform_matrix[1,3] = 0
        self.transform_matrix[2,3] = 0
        
        self.rotation_matrix[:,0] = self.transform_matrix[:,0]
        self.rotation_matrix[:,1] = self.transform_matrix[:,1]
        self.rotation_matrix[:,2] = self.transform_matrix[:,2]
        
        self.translation_matrix[0,0] = 0
        self.translation_matrix[1,0] = 0
        self.translation_matrix[2,0] = 0
        
        self.project_matrix[0,0] = self.focal_length / self.pixel_size
        self.project_matrix[0,1] = 0
        self.project_matrix[0,2] = self.width / 2
        
        self.project_matrix[1,0] = 0
        self.project_matrix[1,1] = self.focal_length / self.pixel_size
        self.project_matrix[1,2] = self.height / 2
        
        self.project_matrix[2,0] = 0
        self.project_matrix[2,1] = 0
        self.project_matrix[2,2] = 1
        
        self.initialized_with_first_frame = False
        self.ball_area_in_pixel_when_4_meter_far_away = None
                
    def process(self, bbox):
        center_2d_matrix = np.zeros((3, 1), dtype = "float32")
        center_2d_matrix[0,0] = bbox.x + bbox.w / 2
        center_2d_matrix[1,0] = bbox.x + bbox.h / 2
        center_2d_matrix[2,0] = 1
        
        # constant_factor = math.pi * self.focal_length * self.focal_length * self.ball_radius * self.ball_radius
        # constant_factor /= (self.pixel_size * self.pixel_size)
        # calculated_distance = math.sqrt(constant_factor / (bbox.w * bbox.h))
        # center_3d = self.__transform_2d_to_3d_point(center_2d_matrix, calculated_distance)
        
        if not self.initialized_with_first_frame:
            self.ball_area_in_pixel_when_4_meter_far_away = bbox.w * bbox.h
            self.initialized_with_first_frame = True
            center_3d = self.__transform_2d_to_3d_point(center_2d_matrix, self.initial_distance_between_camera_and_ball)
        else:
            center_3d = self.__transform_2d_to_3d_point(center_2d_matrix, self.initial_distance_between_camera_and_ball * math.sqrt(self.ball_area_in_pixel_when_4_meter_far_away / (bbox.w * bbox.h)))
        
        center_3d = message.Point3D(center_3d[0],center_3d[1],center_3d[2])
        return center_3d
    
    def __transform_3d_to_2d_point(self, point_3d):
        transformed_3d_point = np.matmul(self.transform_matrix, point_3d)
        point_2d = np.matmul(self.project_matrix, transformed_3d_point)
        return (point_2d[0][0] / point_2d[2][0], point_2d[1][0] / point_2d[2][0])
    
    def __transform_2d_to_3d_point(self, point_2d, alpha):
        # Add 0.5 to each pixel coord to get the center of the pixel
        point_2d[0][0] += 0.5
        point_2d[1][0] += 0.5
        
        # alpha x Pixel Coord = Projection Matrix x ( Rotation Matrix x (World Coord + Translation) )
        # alpha x Inv Projection Matrix x Pixel Coord = Rotation Matrix x (World Coord + Translation)
        # alpha x Inv Rotation Matrix x Inv Projection Matrix x Pixel Coord = World Coord + Translation
        # alpha x Inv Rotation Matrix x Inv Projection Matrix x Pixel Coord - Translation = World Coord
        point_2d = np.matmul(np.linalg.inv(self.project_matrix), point_2d)      
        point_3d = np.matmul(np.linalg.inv(self.rotation_matrix), point_2d)
        point_3d = alpha * point_3d - self.translation_matrix
        
        # Return opposite of y axis to make it compatible with our real world coordinate system
        # Y+ is the sky in our real world coordinate system
        return (point_3d[0][0], point_3d[1][0], point_3d[2][0])