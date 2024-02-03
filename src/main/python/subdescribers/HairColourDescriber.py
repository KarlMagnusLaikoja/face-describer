import cv2
import math
import numpy as np





class HairColourDescriber:

    def __init__(self, hairPixels):

        self.hairPixels = hairPixels

    def describe(self):

        return self.describeHairColour(self.hairPixels)


    def describeHairColour(self, hairPixels):
        #Compares the average RGB value within the "hair pixels" to representatives and classifies the image based on that

        #Get the average RGB value of the hair pixels
        (r, g, b) = getAverageRGB(hairPixels)


        #Compare it to representatives
        return compareRGB( (r, g, b) )
        #return str((r, g, b))





def getAverageRGB(pixels):
    #Calculates the average RGB value from a list of pixels

    rTotal = 0
    gTotal = 0
    bTotal = 0

    for (r, g, b) in pixels:
        rTotal += r
        gTotal += g
        bTotal += b


    r = np.round(rTotal/len(pixels))
    g = np.round(gTotal/len(pixels))
    b = np.round(bTotal/len(pixels))
    return (r, g, b)












def compareRGB(colour):
    #The shortest Euclidean distance in 3 dimensions is considered the correct colour

    #The following are the hardcoded values that are considered as representatives of each hair colour
    #These are found by getting the average RGB values of examples of each such hair colour
    #Red: (136.0, 74.0, 35.0)
    #Blonde: (182.0, 151.0, 123.0)
    #Brown: (89.0, 66.0, 58.0)
    #Black: (52.0, 57.0, 62.0)
    #Grey: (186.0, 182.0, 176.0)



    #Compare the found RGB values to the representative values and return the smallest found value
    differenceFromRed = math.sqrt(
        math.pow(colour[0] - 136, 2) +
        math.pow(colour[1] - 74, 2) +
        math.pow(colour[2] - 35, 2)
    )



    differenceFromBlonde = math.sqrt(
        math.pow(colour[0] - 182, 2) +
        math.pow(colour[1] - 151, 2) +
        math.pow(colour[2] - 123, 2)
    )



    differenceFromBrown = math.sqrt(
        math.pow(colour[0] - 89, 2) +
        math.pow(colour[1] - 66, 2) +
        math.pow(colour[2] - 58, 2)
    )



    differenceFromBlack = math.sqrt(
        math.pow(colour[0] - 52, 2) +
        math.pow(colour[1] - 57, 2) +
        math.pow(colour[2] - 62, 2)
    )



    differenceFromGrey = math.sqrt(
        math.pow(colour[0] - 186, 2) +
        math.pow(colour[1] - 182, 2) +
        math.pow(colour[2] - 176, 2)
    )




    #Return the smallest found value, meaning the shortest Euclidean distance
    diffAndColour = {
        differenceFromRed: "red",
        differenceFromBlonde: "blonde",
        differenceFromBrown: "brown",
        differenceFromBlack: "black",
        differenceFromGrey: "grey",
    }
    result = ""
    diff = 9999999
    for key in diffAndColour:
        if(key<diff):
            diff = key
            result = diffAndColour[key]
    return result