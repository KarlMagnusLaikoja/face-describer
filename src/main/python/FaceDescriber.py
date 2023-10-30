import face_recognition
import sys
import cv2
from subdescribers.EyeColourDescriber import EyeColourDescriber

class FaceDescriber:
    def __init__(self, image, language):
        self.image = cv2.imread("../../../"+image)
        self.language = language
        self.output_EE = "Pildil oleval inimesel on %eyeColour% värvi %eyeShape% kujuga silmad."
        self.output_EN = "The person in the picture has %eyeColour%, %eyeShape% shaped eyes."

    def describe(self):
        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)
        if(len(face_landmarks_list)==0):
            if(self.language=="EE"):
                print("Pildilt ei tuvastatud ühtegi nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Couldn't detect any faces.")
                sys.exit(101)

        if(len(face_landmarks_list)==1):
            self.describeEyeColour()
            if(self.language=="EE"):
                return self.output_EE
            elif(self.language=="EN"):
                return self.output_EN

        else:
            if(self.language=="EE"):
                print("Pildilt tuvastati mitu nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Multiple faces were detected.")
                sys.exit(101)

    def describeEyeColour(self):
        eyeColourDescriber = EyeColourDescriber(self.image)
        rightEyeColour, leftEyeColour = eyeColourDescriber.describe()
        colourMapping = {
            "blue": ["sinine", "sinist"],
            "brown": ["pruun", "pruuni"],
            "green": ["roheline", "rohelist"],
            "grey": ["hall", "halli"],
            "hazel": ["pähkelpruun", "pähkelpruuni"],
            "red": ["punane", "punast"]
        }

        if(rightEyeColour==leftEyeColour):
            self.output_EN = self.output_EN.replace("%eyeColour%", rightEyeColour)
            self.output_EE = self.output_EE.replace("%eyeColour%", colourMapping[rightEyeColour][1])
        else:
            self.output_EN = self.output_EN.replace("%eyeColour%", "different coloured (the left is "+leftEyeColour+", the right is "+rightEyeColour+")")
            self.output_EE = self.output_EE.replace("värvi", "").replace("%eyeColour%", "eri värvi (vasak "+colourMapping[leftEyeColour][0]+", parem "+colourMapping[rightEyeColour][0]+")")




fileName = sys.argv[1]
language = sys.argv[2]
print(FaceDescriber(fileName, language).describe())