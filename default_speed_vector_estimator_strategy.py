import message
import numpy as np
from sklearn.linear_model import LinearRegression

class DefaultSpeedVectorEstimatorStrategy:
    def __init__(self, configuration):
        self.configuration = configuration
        self.fps = configuration.camera_fps
        self.history_depth = configuration.speed_vector_estimator_history_depth
        self.period = 1.0 / self.fps
        self.position_x_history = []
        self.position_y_history = []
        self.position_z_history = []
    
    def process(self, points_3d, center_3d):
        speed_vectors = []
        
        self.position_x_history.append(center_3d.x)
        self.position_y_history.append(center_3d.y)
        self.position_z_history.append(center_3d.z)
        if len(self.position_x_history) > self.history_depth:
            self.position_x_history.pop(0)
            self.position_y_history.pop(0)
            self.position_z_history.pop(0)
        
        avg_speed_vector = message.Point3D(0,0,0)
        if len(self.position_x_history) >= 2:
            # Convert position history lists to numpy arrays
            x = np.array(self.position_x_history)
            y = np.array(self.position_y_history)
            z = np.array(self.position_z_history)

            # Reshape arrays to have a single feature
            x = x.reshape(-1, 1)
            y = y.reshape(-1, 1)
            input = np.concatenate((x, y), axis=1)
            output = z.reshape(-1, 1)

            # Create a linear regression model
            model = LinearRegression()

            # Fit the model to the data
            model.fit(input, output) 

            calculate_input = [input[0], input[-1]]
            predicted_z = model.predict(calculate_input)
            avg_speed_vector.x = (calculate_input[1][0] - calculate_input[0][0]) / ((len(input) - 1) * self.period)
            avg_speed_vector.y = (calculate_input[1][1] - calculate_input[0][1]) / ((len(input) - 1) * self.period)
            avg_speed_vector.z = (predicted_z[1][0] - predicted_z[0][0]) / ((len(input) - 1) * self.period)
            
        return speed_vectors, avg_speed_vector