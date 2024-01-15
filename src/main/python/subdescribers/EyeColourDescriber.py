import face_recognition
import cv2
import extcolors
import math
from PIL import Image


class EyeColourDescriber:
    def __init__(self, image, leftEyeCoordinates, rightEyeCoordinates, skinColourRGB):
        self.image = image
        self.leftEyeCoordinates = leftEyeCoordinates
        self.rightEyeCoordinates = rightEyeCoordinates
        self.skinColourRGB = skinColourRGB

    def describe(self):
        return self.findEyeColour(self.leftEyeCoordinates, self.skinColourRGB), self.findEyeColour(self.rightEyeCoordinates, self.skinColourRGB)



    def findEyeColour(self, coordinates, skinColourRGB):
        #coordinates format: ((lowestX, highestX), (lowestY, highestY))

        #Crop the image using the eye coordinates so that it only contains the eye
        eye = self.image[
              coordinates[1][0]:coordinates[1][1],
              coordinates[0][0]:coordinates[0][1]
              ]

        #Convert to correct format
        eye = cv2.cvtColor(eye, cv2.COLOR_BGR2RGB)
        colours = []
        #Gather all the found RGB
        for i in range(len(eye)):
            for j in range(len(eye[i])):
                colours.append(eye[i][j])

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


        #Compare the found colour to predefined eye colours
        return self.compareRGB( (r, g, b) )


    def compareRGB(self, colour):
        #The shortest Euclidean distance in 3 dimensions is considered the correct colour

        #The following are the hardcoded values that are considered as representatives of each eye colour
        #These are found by getting the average RGB values of examples of each eye colour
        #Blue: [89, 117, 130]
        #Brown: [62, 48, 40]
        #Green: [70, 70, 42]
        #Grey: [113, 109, 114]
        #Hazel: [118, 99, 63]
        #Red: [158, 114, 120]


        #Compare the found RGB values to the representative values and return the smallest found value
        differenceFromBlue = math.sqrt(
            math.pow(colour[0] - 89, 2) +
            math.pow(colour[1] - 117, 2) +
            math.pow(colour[2] - 130, 2)
        )
        differenceFromBrown = math.sqrt(
            math.pow(colour[0] - 62, 2) +
            math.pow(colour[1] - 48, 2) +
            math.pow(colour[2] - 40, 2)
        )
        differenceFromGreen = math.sqrt(
            math.pow(colour[0] - 70, 2) +
            math.pow(colour[1] - 70, 2) +
            math.pow(colour[2] - 42, 2)
        )
        differenceFromGrey = math.sqrt(
            math.pow(colour[0] - 113, 2) +
            math.pow(colour[1] - 109, 2) +
            math.pow(colour[2] - 114, 2)
        )
        differenceFromHazel = math.sqrt(
            math.pow(colour[0] - 118, 2) +
            math.pow(colour[1] - 99, 2) +
            math.pow(colour[2] - 63, 2)
        )
        differenceFromRed = math.sqrt(
            math.pow(colour[0] - 158, 2) +
            math.pow(colour[1] - 114, 2) +
            math.pow(colour[2] - 120, 2)
        )


        #Return the smallest found value, meaning the shortest Euclidean distance
        diffAndColour = {
            differenceFromBlue: "blue",
            differenceFromBrown: "brown",
            differenceFromGreen: "green",
            differenceFromGrey: "grey",
            differenceFromHazel: "hazel",
            differenceFromRed: "red"
        }
        result = ""
        diff = 9999999
        for key in diffAndColour:
            if(key<diff):
                diff = key
                result = diffAndColour[key]
        return result
