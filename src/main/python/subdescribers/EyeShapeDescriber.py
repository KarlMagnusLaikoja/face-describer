import face_recognition
import cv2
import extcolors
import math
from PIL import Image

class EyeShapeDescriber:
    def __init__(self, image):
        self.image = image