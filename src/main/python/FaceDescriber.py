import face_recognition
import sys
import cv2
import extcolors
from PIL import Image
from subdescribers.EyeColourDescriber import EyeColourDescriber


def crop(coordinates):
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
        self.output_EE = "Pildil oleval inimesel on %eyeColour% värvi %eyeShape% kujuga silmad. Tal on  %skinColour% värvi nahk."
        self.output_EN = "The person in the picture has %eyeColour%, %eyeShape% shaped eyes. They have %skinColour% coloured skin."

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
        skinColourRGB = self.describeSkinColour(coordinates)

        #Describe eyecolour
        #params: left eye coordinates, right eye coordinates
        #format: ((lowestX, highestX), (lowestY, highestY))
        self.describeEyeColour(
            crop(coordinates[42:47+1]),
            crop(coordinates[36:41+1]),
            skinColourRGB
        )




        #Return output based on provided language code
        if(self.language=="EE"):
            return self.output_EE
        elif(self.language=="EN"):
            return self.output_EN



    def describeSkinColour(self, coordinates):
        #Take the cheek area and go through every pixel, return the average RGB value and corresponding skin colour

        cheekArea = self.image[
                coordinates[1][1]:coordinates[34+1][1],
                coordinates[4][0]:coordinates[12+1][0]
              ]

        #Convert to correct format
        cheekArea = cv2.cvtColor(cheekArea, cv2.COLOR_BGR2RGB)
        colours = []
        #Gather all the found RGB
        for i in range(len(cheekArea)):
            for j in range(len(cheekArea[i])):
                colours.append(cheekArea[i][j])

        #Find the average
        rTotal = 0
        gTotal = 0
        bTotal = 0
        for (r, g, b) in colours:
            rTotal+=r
            gTotal+=g
            bTotal+=b

        r = round(rTotal/len(colours))
        g = round(gTotal/len(colours))
        b = round(bTotal/len(colours))


        #TODO - compare to hardcoded skin colours


        self.output_EN = self.output_EN.replace("%skinColour%", str((r,g,b)))
        self.output_EE = self.output_EE.replace("%skinColour%", str((r,g,b)))
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