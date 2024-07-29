import sys

from message_factory import MessageFactory
from metadata_printer import MetadataPrinter
from dummy_metadata_generator import DummyMetadataGenerator
from configuration import Configuration
from gt_error_calculator import GroundTruthErrorCalculator
from ball_detector import BallDetector
from world_coordinate_estimator import WorldCoordinateEstimator
from speed_vector_estimator import SpeedVectorEstimator
from metadata_exporter import MetadataExporter

class Runner:    
    def __init__(self, configuration_file_path):
        self.configuration = Configuration(configuration_file_path)
        self.output_file_path = self.configuration.output_file_path
        self.message_factory = MessageFactory('images', 'IMG%d.bmp', 1, 'gt_masks', 'IMG%d.png', 1)
        self.metadata_printer = MetadataPrinter(expand_lists=False)
        self.dummy_metadata_generator = DummyMetadataGenerator()
        self.gt_error_calculator = GroundTruthErrorCalculator()
        self.ball_detector = BallDetector(self.configuration)
        self.world_coordinate_estimator = WorldCoordinateEstimator(self.configuration)
        self.speed_vector_estimator = SpeedVectorEstimator(self.configuration)
        self.metadata_exporter = MetadataExporter(self.output_file_path)

    def run(self):
        while True:
            # Acquire Message
            message = self.message_factory.next_message()
            if message is None:
                break
            
            # Detect Ball
            self.ball_detector.process(message)
            
            # Unfortunately target ball is not detected for this frame
            if message.metadata.ball_bbox is None:
                continue
            
            # Ground Truth Equalizer
            # It is used to test world coordinate estimator and speed vector estimator
            # It should be commented out when considering ball detector
            # message.metadata.ball_bbox = message.metadata.gt_ball_bbox
            
            # Estimate World Coordinates
            self.world_coordinate_estimator.process(message)
            
            # Estimate Speed Vectors
            self.speed_vector_estimator.process(message)
            
            # Fill dummy message metadata
            # It is used to test the metadata printer and metadata exporter
            # Also it is used to test plotter
            # self.dummy_metadata_generator.process(message)
            
            # Compare with Ground Truth
            self.gt_error_calculator.process(message)
            
            # Print Metadata
            self.metadata_printer.process(message)
            
            # Export Metadata   
            self.metadata_exporter.process(message)


if __name__ == '__main__':
    if sys.argv[1:]:
        runner = Runner(sys.argv[1])
    else:
        runner = Runner("configuration.yaml")
    runner.run()