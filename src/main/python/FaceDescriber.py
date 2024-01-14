import face_recognition
import sys
import cv2
import extcolors
from PIL import Image
from subdescribers.EyeColourDescriber import EyeColourDescriber
from subdescribers.SkinColourDescriber import SkinColourDescriber

def getCoordinatesFromPoints(coordinates):
    xCoordinates = [pair[0] for pair in coordinates]
    yCoordinates = [pair[1] for pair in coordinates]
    lowestX = min(xCoordinates)
    lowestY = min(yCoordinates)
    highestX = max(xCoordinates)
    highestY = max(yCoordinates)
    return ((lowestX, highestX), (lowestY, highestY))

class FaceDescriber:
    def __init__(self, image, language):
        self.image = cv2.imread("../../../"+image)
        self.language = language
        self.output_EE = "Pildil oleval inimesel on %skinColour% nahk. Tal on %eyeColour% värvi %eyeShape% kujuga silmad."
        self.output_EN = "The person in the picture has %skinColour% skin. They have %eyeColour%, %eyeShape% shaped eyes."

    def assertSingleFace(self, face_landmarks_list):
        if(len(face_landmarks_list)==0):
            if(self.language=="EE"):
                print("Pildilt ei tuvastatud ühtegi nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Couldn't detect any faces.")
                sys.exit(101)
        elif(len(face_landmarks_list)>1):
            if(self.language=="EE"):
                print("Pildilt tuvastati mitu nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Multiple faces were detected.")
                sys.exit(101)

    def describe(self):
        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)
        #Verify that the image only contains a single face
        self.assertSingleFace(face_landmarks_list)
        face_landmarks = face_landmarks_list[0]
        #Gather all the coordinates into a single list
        coordinates = []
        for k, v in face_landmarks.items():
            for (x, y) in v:
                coordinates.append((x, y))


        #Describe skin colour
        #params: cheek area coordinates in format ((lowestX, highestX), (lowestY, highestY))
        skinColourRGB = self.describeSkinColour(
            (
                (coordinates[4][0], coordinates[12+1][0]),
                (coordinates[1][1], coordinates[34+1][1])
            )
        )


        #Describe eyecolour
        #params: left eye coordinates, right eye coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeEyeColour(
            getCoordinatesFromPoints(coordinates[42:47+1]),
            getCoordinatesFromPoints(coordinates[36:41+1]),
            skinColourRGB
        )




        #Return output based on provided language code
        if(self.language=="EE"):
            return self.output_EE
        elif(self.language=="EN"):
            return self.output_EN



    def describeSkinColour(self, coordinates):
        #Instantiate skin colour describer
        skinColourDescriber = SkinColourDescriber(self.image, coordinates)

        #Describe skin colour
        (r, g, b), colour = skinColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "pale white": "kahvatu valge",
            "fair": "hele",
            "darker white": "tumedam valge",
            "light brown": "helepruun",
            "brown": "pruun",
            "dark brown or black": "tumepruun või must"
        }

        self.output_EN = self.output_EN.replace("%skinColour%", colour)
        self.output_EE = self.output_EE.replace("%skinColour%", colourMapping[colour])
        return (r, g, b)


    def describeEyeColour(self, leftEyeCoordinates, rightEyeCoordinates, skinColourRGB):
        #Instantiate eye colour describer
        eyeColourDescriber = EyeColourDescriber(self.image, leftEyeCoordinates, rightEyeCoordinates, skinColourRGB)

        #Describe both eyes
        #Return format: ("blue", "brown")
        leftEyeColour, rightEyeColour = eyeColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "blue": ["sinine", "sinist"],
            "brown": ["pruun", "pruuni"],
            "green": ["roheline", "rohelist"],
            "grey": ["hall", "halli"],
            "hazel": ["pähkelpruun", "pähkelpruuni"],
            "red": ["punane", "punast"]
        }

        #Consider case where eyes are different coloured
        if(rightEyeColour==leftEyeColour):
            self.output_EN = self.output_EN.replace("%eyeColour%", rightEyeColour)
            self.output_EE = self.output_EE.replace("%eyeColour%", colourMapping[rightEyeColour][1])
        else:
            self.output_EN = self.output_EN.replace("%eyeColour%", "different coloured (the left is "+leftEyeColour+", the right is "+rightEyeColour+")")
            self.output_EE = self.output_EE.replace("värvi", "").replace("%eyeColour%", "eri värvi (vasak "+colourMapping[leftEyeColour][0]+", parem "+colourMapping[rightEyeColour][0]+")")





fileName = sys.argv[1]
language = sys.argv[2]
print(FaceDescriber(fileName, language).describe())