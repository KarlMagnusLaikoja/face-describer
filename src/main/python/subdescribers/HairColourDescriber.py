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
    #Red: (161.0, 104.0, 80.0)
    #Blonde: (145.0, 116.0, 91.0)
    #Brown: (87.0, 74.0, 64.0)
    #Black: (46.0, 52.0, 51.0)
    #Grey: (186.0, 182.0, 176.0)



    #Compare the found RGB values to the representative values and return the smallest found value
    differenceFromRed = math.sqrt(
        math.pow(colour[0] - 161, 2) +
        math.pow(colour[1] - 104, 2) +
        math.pow(colour[2] - 80, 2)
    )



    differenceFromBlonde = math.sqrt(
        math.pow(colour[0] - 145, 2) +
        math.pow(colour[1] - 116, 2) +
        math.pow(colour[2] - 91, 2)
    )



    differenceFromBrown = math.sqrt(
        math.pow(colour[0] - 87, 2) +
        math.pow(colour[1] - 74, 2) +
        math.pow(colour[2] - 64, 2)
    )



    differenceFromBlack = math.sqrt(
        math.pow(colour[0] - 46, 2) +
        math.pow(colour[1] - 52, 2) +
        math.pow(colour[2] - 51, 2)
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