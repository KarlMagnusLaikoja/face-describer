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

        #Find RGB values within the image of the eye
        eye = cv2.cvtColor(eye, cv2.COLOR_BGR2RGB)
        eye_pil = Image.fromarray(eye)
        colours = extcolors.extract_from_image(eye_pil, tolerance = 12, limit = 12)[0]
        colours = [rgb[0] for rgb in colours]  #Not all colours are the eye colour specifically


        #Compare the found colours to predefined eye colours (blue, brown etc)
        return self.compareRGB(colours)


    def compareRGB(self, colours):
        #The shortest Euclidean distance in 3 dimensions is considered the correct colour

        #The following are the hardcoded values that are considered as representatives of each eye colour
        #Blue: [78, 113, 132]
        #Brown: [52, 32, 23]
        #Green: [83, 88, 47]
        #Grey: [155, 156, 160]
        #Hazel: [124, 104, 49]
        #Red: [151, 90, 102]

        #Compare all of the found RGB values to the representative values and keep the ones with the smallest distance
        differenceFromBlue = 999999
        differenceFromBrown = 999999
        differenceFromGreen = 999999
        differenceFromGrey = 999999
        differenceFromHazel = 999999
        differenceFromRed = 999999

        for foundRGB in colours:

            #Difference from blue
            foundDifferenceFromBlue = math.sqrt(
                math.pow(foundRGB[0]-78, 2) +
                math.pow(foundRGB[1]-113, 2) +
                math.pow(foundRGB[2]-132, 2)
            )
            if(foundDifferenceFromBlue<differenceFromBlue):
                differenceFromBlue = foundDifferenceFromBlue

            #Difference from brown
            foundDifferenceFromBrown = math.sqrt(
                math.pow(foundRGB[0]-52, 2) +
                math.pow(foundRGB[1]-32, 2) +
                math.pow(foundRGB[2]-23, 2)
            )
            if(foundDifferenceFromBrown<differenceFromBrown):
                differenceFromBrown = foundDifferenceFromBrown

            #Difference from green
            foundDifferenceFromGreen = math.sqrt(
                math.pow(foundRGB[0]-83, 2) +
                math.pow(foundRGB[1]-88, 2) +
                math.pow(foundRGB[2]-47, 2)
            )
            if(foundDifferenceFromGreen<differenceFromGreen):
                differenceFromGreen = foundDifferenceFromGreen

            #Difference from grey
            foundDifferenceFromGrey = math.sqrt(
                math.pow(foundRGB[0]-155, 2) +
                math.pow(foundRGB[1]-156, 2) +
                math.pow(foundRGB[2]-160, 2)
            )
            if(foundDifferenceFromGrey<differenceFromGrey):
                differenceFromGrey = foundDifferenceFromGrey

            #Difference from hazel
            foundDifferenceFromHazel = math.sqrt(
                math.pow(foundRGB[0]-124, 2) +
                math.pow(foundRGB[1]-104, 2) +
                math.pow(foundRGB[2]-49, 2)
            )
            if(foundDifferenceFromHazel<differenceFromHazel):
                differenceFromHazel = foundDifferenceFromHazel

            #Difference from red
            foundDifferenceFromRed = math.sqrt(
                math.pow(foundRGB[0]-151, 2) +
                math.pow(foundRGB[1]-90, 2) +
                math.pow(foundRGB[2]-102, 2)
            )
            if(foundDifferenceFromRed<differenceFromRed):
                differenceFromRed = foundDifferenceFromRed


        #Return the smallest found value, meaning the shortest Euclidean distance
        diffAndColor = {differenceFromBlue: "blue", differenceFromBrown: "brown", differenceFromGreen: "green", differenceFromGrey: "grey", differenceFromHazel: "hazel", differenceFromRed: "red"}
        result = ""
        diff = 9999999
        for key in diffAndColor:
            if(key<diff):
                diff = key
                result = diffAndColor[key]
        return result
