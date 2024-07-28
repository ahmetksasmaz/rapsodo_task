from default_ball_tracker_strategy import DefaultBallTrackerStrategy

class BallTracker:
    def __init__(self, configuration):
        self.configuration = configuration
        self.strategy_name = configuration.ball_tracker_strategy
        if self.strategy_name == "default":
            self.strategy = DefaultBallTrackerStrategy(self.configuration)
        else:
            raise ValueError("Invalid ball tracker strategy: " + self.strategy_name)
        
    def process(self, msg):
        msg.metadata.ball_target_bbox = self.strategy.process(msg.metadata.ball_bboxes)
        