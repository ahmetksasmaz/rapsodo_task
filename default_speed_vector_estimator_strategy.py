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
    
    def process(self, message_id, center_3d):
        self.position_x_history.append((message_id, center_3d.x))
        self.position_y_history.append((message_id, center_3d.y))
        self.position_z_history.append((message_id, center_3d.z))
        if self.position_x_history[-1][0] - self.position_x_history[0][0] > self.history_depth:
            self.position_x_history.pop(0)
            self.position_y_history.pop(0)
            self.position_z_history.pop(0)
        
        avg_speed_vector = message.Point3D(0,0,0)
        if len(self.position_x_history) >= 2:
            # Convert position history lists to numpy arrays
            pos_x_hist = [pos[1] for pos in self.position_x_history]
            pos_y_hist = [pos[1] for pos in self.position_y_history]
            pos_z_hist = [pos[1] for pos in self.position_z_history]
            x = np.array(pos_x_hist)
            y = np.array(pos_y_hist)
            z = np.array(pos_z_hist)

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
            avg_speed_vector.x = (calculate_input[1][0] - calculate_input[0][0]) / ((self.position_x_history[-1][0] - self.position_x_history[0][0]) * self.period)
            avg_speed_vector.y = (calculate_input[1][1] - calculate_input[0][1]) / ((self.position_x_history[-1][0] - self.position_x_history[0][0]) * self.period)
            avg_speed_vector.z = (predicted_z[1][0] - predicted_z[0][0]) / ((self.position_x_history[-1][0] - self.position_x_history[0][0]) * self.period)
            
        return avg_speed_vector