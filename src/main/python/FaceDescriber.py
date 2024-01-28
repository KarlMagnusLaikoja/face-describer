import face_recognition
import sys
import cv2
from subdescribers.EyeColourDescriber import EyeColourDescriber
from subdescribers.SkinColourDescriber import SkinColourDescriber
from subdescribers.FaceShapeDescriber import FaceShapeDescriber

def getCoordinatesFromPoints(coordinates):
    #Gets the pair of "lowest" and "highest" coordinates within a set of coordinates/points
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
        self.output_EN = {
            "face shape": "",
            "skin colour": "",
            "right eye colour": "",
            "left eye colour": ""
        }
        self.output_EE = {
            "näo kuju": "",
            "naha värv": "",
            "parema silma värv": "",
            "vasaku silma värv": ""
        }

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


        #Describe face shape
        #params: entire coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeFaceShape(
            (
                (coordinates[0][0], coordinates[16][0]),
                (coordinates[24][1], coordinates[8][1])
            )
        )

        #Describe skin colour
        #params: left cheek area coordinates in format ((lowestX, highestX), (lowestY, highestY))
        skinColourRGB = self.describeSkinColour(
            (
                (coordinates[10][0], coordinates[13][0]),
                (coordinates[1][1], coordinates[35][1])
            )
        )


        #Describe eyecolour
        #params: left eye coordinates, right eye coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeEyeColour(
            (
                (coordinates[43][0], coordinates[46][0]),
                (coordinates[43][1], coordinates[46][1])
            ),
            (
                (coordinates[37][0], coordinates[40][0]),
                (coordinates[37][1], coordinates[40][1])
            ),
            skinColourRGB
        )




        #Return output based on provided language code
        if(self.language=="EE"):
            return self.output_EE
        elif(self.language=="EN"):
            return self.output_EN


    def describeFaceShape(self, coordinates):
        #Instantiate face shape describer
        faceShapeDescriber = FaceShapeDescriber(self.image, coordinates)

        #Describe face shape
        shape = faceShapeDescriber.describe()

        #Mapping from english to estonian
        shapeMapping = {
            "diamond": "teemant",
            "oblong": "oblong",
            "oval": "ovaal",
            "round": "ümmargune",
            "square": "ruut",
        }


        self.output_EN["face shape"] = shape
        self.output_EE["näo kuju"] = shapeMapping[shape]




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


        self.output_EN["skin colour"] = colour
        self.output_EE["naha värv"] = colourMapping[colour]
        return (r, g, b)


    def describeEyeColour(self, leftEyeCoordinates, rightEyeCoordinates, skinColourRGB):
        #Instantiate eye colour describer
        eyeColourDescriber = EyeColourDescriber(self.image, leftEyeCoordinates, rightEyeCoordinates, skinColourRGB)

        #Describe both eyes
        #Return format: ("blue", "brown")
        leftEyeColour, rightEyeColour = eyeColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "blue": "sinine",
            "brown": "pruun",
            "green": "roheline",
            "grey": "hall",
            "hazel": "pähkelpruun",
            "red": "punane"
        }


        self.output_EN["left eye colour"] = leftEyeColour
        self.output_EN["right eye colour"] = rightEyeColour
        self.output_EE["vasaku silma värv"] = colourMapping[leftEyeColour]
        self.output_EE["parema silma värv"] = colourMapping[rightEyeColour]




fileName = sys.argv[1]
language = sys.argv[2]
print(FaceDescriber(fileName, language).describe())