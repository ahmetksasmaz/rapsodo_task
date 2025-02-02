from default_speed_vector_estimator_strategy import DefaultSpeedVectorEstimatorStrategy

class SpeedVectorEstimator:
    def __init__(self, configuration):
        self.configuration = configuration
        self.strategy_name = configuration.speed_vector_estimator_strategy
        if self.strategy_name == "default":
            self.strategy = DefaultSpeedVectorEstimatorStrategy(self.configuration)
        else:
            raise ValueError("Invalid speed vector estimator strategy: " + self.strategy_name)
        
    def process(self, message):
        metadata = message.metadata
        avg_speed_vector = self.strategy.process(message.message_id, metadata.ball_3d_center)
        metadata.ball_avg_3d_speed_vector = avg_speed_vector