from default_world_coordinate_estimator_strategy import DefaultWorldCoordinateEstimatorStrategy

class WorldCoordinateEstimator:
    def __init__(self, configuration):
        self.configuration = configuration
        self.strategy_name = configuration.world_coordinate_estimator_strategy
        if self.strategy_name == "default":
            self.strategy = DefaultWorldCoordinateEstimatorStrategy(self.configuration)
        else:
            raise ValueError("Invalid world coordinate estimator strategy: " + self.strategy_name)
        
    def process(self, message):
        metadata = message.metadata
        center_3d = self.strategy.process(metadata.ball_bbox)
        metadata.ball_3d_center = center_3d