from default_ball_detector_strategy import DefaultBallDetectorStrategy

class BallDetector:
    def __init__(self, configuration):
        self.configuration = configuration
        self.strategy_name = configuration.ball_detector_strategy
        if self.strategy_name == "default":
            self.strategy = DefaultBallDetectorStrategy(self.configuration)
        else:
            raise ValueError("Invalid ball detector strategy: " + self.strategy_name)
        
    def process(self, msg):
        image = msg.image
        bbox = self.strategy.process(image)
        msg.metadata.ball_bbox = bbox