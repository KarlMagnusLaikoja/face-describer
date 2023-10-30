import face_recognition
import cv2
import extcolors
import math
from PIL import Image

class EyeColourDescriber:
    def __init__(self, image):
        self.image = image

    def describe(self):
        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)
        rightEyeCoordinates = face_landmarks_list[0]["right_eye"]
        leftEyeCoordinates = face_landmarks_list[0]["left_eye"]

        rightEyeColour = findEyeColour(rightEyeCoordinates, image)
        leftEyeColour = findEyeColour(leftEyeCoordinates, image)

        return rightEyeColour, leftEyeColour


def findEyeColour(coordinates, image):
    #Find "widest" coordinates to get as much of the eyes as possible
    lowestX = 99999
    highestX = 0
    lowestY = 99999
    highestY = 0
    for coordinatePair in coordinates:
        if(coordinatePair[0]<lowestX):
            lowestX = coordinatePair[0]
        if(coordinatePair[0]>highestX):
            highestX = coordinatePair[0]
        if(coordinatePair[1]<lowestY):
            lowestY = coordinatePair[1]
        if(coordinatePair[1]>highestY):
            highestY = coordinatePair[1]


    #Find RGB values within the image of the eye
    eye = image[lowestY:highestY, lowestX:highestX]
    eye = cv2.cvtColor(eye, cv2.COLOR_BGR2RGB)
    eye_pil = Image.fromarray(eye)
    colours = extcolors.extract_from_image(eye_pil, tolerance = 12, limit = 12)[0]
    colours = [rgb[0] for rgb in colours]  #Not all colours are the eye colour specifically


    #Compare the found colours to predefined eye colours (blue, brown etc)
    #The shortest Euclidean distance is considered the correct colour
    #Blue: [78, 113, 132]
    #Brown: [52, 32, 23]
    #Green: [83, 88, 47]
    #Grey: [155, 156, 160]
    #Hazel: [124, 104, 49]
    #Red: [151, 90, 102]
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


    #Return the smallest found value
    diffAndColor = {differenceFromBlue: "blue", differenceFromBrown: "brown", differenceFromGreen: "green", differenceFromGrey: "grey", differenceFromHazel: "hazel", differenceFromRed: "red"}
    result = ""
    diff = 9999999
    for key in diffAndColor:
        if(key<diff):
            diff = key
            result = diffAndColor[key]
    return result
