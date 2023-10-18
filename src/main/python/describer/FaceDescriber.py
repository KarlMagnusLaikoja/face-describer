"""import face_recognition
from subdescribers import EyeColourDescriber


class FaceDescriber:
    def __init__(self, image):
        self.image = image
        self.output = "Pildil oleval inimesel on %eyeColour% värvi %eyeShape% kujuga silmad."

    def describe(self):
        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)
        if(len(face_landmarks_list)==0):
            return "Pildilt ei tuvastatud ühtegi nägu."
        if(len(face_landmarks_list)==1):
            return self.describeSingeFace(self)
        else: #Mitu nägu
            return self.describeMultipleFaces(self, face_landmarks_list)

    def describeSingleFace(self):
        eyeColourDescriber = EyeColourDescriber(self.image, self.output)
        self.output = eyeColourDescriber.describe()
        return self.output

    def describeMultipleFaces(self, face_landmarks_list):
        self.output = "Pildilt tuvastati mitu nägu."
        #for face_landmarks_dict in face_landmarks_list:
        #    eyeColourDescriber = EyeColourDescriber(self.image, self.output)
        #    self.output = eyeColourDescriber.describe()
        return self.output
"""