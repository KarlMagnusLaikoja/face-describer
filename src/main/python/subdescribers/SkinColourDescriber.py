import face_recognition
import cv2
import extcolors
import math
from PIL import Image


class SkinColourDescriber:
    def __init__(self, image, coordinates):
        self.image = image
        self.coordinates = coordinates

    def describe(self):
        return self.describeSkinColour(self.coordinates)


    def describeSkinColour(self, coordinates):
        #coordinates format: ((lowestX, highestX), (lowestY, highestY))

        #Crop the image using the left cheek area coordinates and go through every pixel, return the average RGB value and corresponding skin colour
        cheekArea = self.image[
              coordinates[1][0]:coordinates[1][1],
              coordinates[0][0]:coordinates[0][1]
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


        return ((r, g, b),
                #Compare the found colour to predefined skin colours
                self.compareRGB( (r, g, b) ))



    def compareRGB(self, colour):
        #The shortest Euclidean distance in 3 dimensions is considered the correct colour

        #The following are the hardcoded values that are considered as representatives of each skin colour
        #These are found by getting the average RGB values of examples of each skin colour
        #Pale white: [245, 186, 164]
        #Fair: [148, 115, 106]
        #Darker white: [146, 101, 78]
        #Light brown: [159, 122, 110]
        #Brown: [160, 112, 109]
        #Dark brown or black: [50, 37, 32]

        #Compare the found RGB values to the representative values and return the smallest found value
        differenceFromPaleWhite = math.sqrt(
            math.pow(colour[0] - 245, 2) +
            math.pow(colour[1] - 186, 2) +
            math.pow(colour[2] - 164, 2)
        )
        differenceFromFair = math.sqrt(
            math.pow(colour[0] - 148, 2) +
            math.pow(colour[1] - 115, 2) +
            math.pow(colour[2] - 106, 2)
        )
        differenceFromDarkerWhite = math.sqrt(
            math.pow(colour[0] - 146, 2) +
            math.pow(colour[1] - 101, 2) +
            math.pow(colour[2] - 78, 2)
        )
        differenceFromLightBrown = math.sqrt(
            math.pow(colour[0] - 159, 2) +
            math.pow(colour[1] - 122, 2) +
            math.pow(colour[2] - 110, 2)
        )
        differenceFromBrown = math.sqrt(
            math.pow(colour[0] - 160, 2) +
            math.pow(colour[1] - 112, 2) +
            math.pow(colour[2] - 109, 2)
        )
        differenceFromDarkBrownOrBlack = math.sqrt(
            math.pow(colour[0] - 50, 2) +
            math.pow(colour[1] - 37, 2) +
            math.pow(colour[2] - 32, 2)
        )


        #Return the smallest found value, meaning the shortest Euclidean distance
        diffAndColour = {
            differenceFromPaleWhite: "pale white",
            differenceFromFair: "fair",
            differenceFromDarkerWhite: "darker white",
            differenceFromLightBrown: "light brown",
            differenceFromBrown: "brown",
            differenceFromDarkBrownOrBlack: "dark brown or black"
        }
        result = ""
        diff = 9999999
        for key in diffAndColour:
            if(key<diff):
                diff = key
                result = diffAndColour[key]
        return result