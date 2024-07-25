import cv2 as cv
import message
import os

class MessageFactory:
    def __init__(self, image_directory_path, image_regex, file_number_starting_index):
        self.image_directory_path = image_directory_path
        self.image_regex = image_regex
        self.image_index = file_number_starting_index
        
    def next_message(self):
        if os.path.isfile(self.image_directory_path + '/' + self.image_regex % self.image_index) == False:
            return None        
        image = cv.imread(self.image_directory_path + '/' + self.image_regex % self.image_index)
        if image is None:
            return None
        msg = message.Message(self.image_index, image)
        self.image_index += 1
        return msg