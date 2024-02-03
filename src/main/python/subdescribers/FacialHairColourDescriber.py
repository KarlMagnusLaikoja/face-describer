import cv2
import math
import numpy as np





class FacialHairColourDescriber:

    def __init__(self, facialHairPixels):

        self.facialHairPixels = facialHairPixels

    def describe(self):

        return self.describeFacialHairColour(self.facialHairPixels)




    def describeFacialHairColour(self, facialHairPixels):
        #Compares the average RGB values within the "facial hair pixels" to representatives and classifies the image based on that

        #Get the average RGB value of the facial hair pixels
        (r, g, b) = getAverageRGB(facialHairPixels)


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

    #The following are the hardcoded values that are considered as representatives of each facial hair colour
    #These are found by getting the average RGB values of examples of each facial hair colour
    #Red: (147.0, 87.0, 66.0)
    #Blonde: (129.0, 109.0, 90.0)
    #Brown: (126.0, 70.0, 55.0)
    #Black: (24.0, 26.0, 27.0)
    #Grey: (137.0, 137.0, 142.0)



    #Compare the found RGB values to the representative values and return the smallest found value
    differenceFromRed = math.sqrt(
        math.pow(colour[0] - 147, 2) +
        math.pow(colour[1] - 87, 2) +
        math.pow(colour[2] - 66, 2)
    )



    differenceFromBlonde = math.sqrt(
        math.pow(colour[0] - 129, 2) +
        math.pow(colour[1] - 109, 2) +
        math.pow(colour[2] - 90, 2)
    )



    differenceFromBrown = math.sqrt(
        math.pow(colour[0] - 126, 2) +
        math.pow(colour[1] - 70, 2) +
        math.pow(colour[2] - 55, 2)
    )



    differenceFromBlack = math.sqrt(
        math.pow(colour[0] - 24, 2) +
        math.pow(colour[1] - 26, 2) +
        math.pow(colour[2] - 27, 2)
    )



    differenceFromGrey = math.sqrt(
        math.pow(colour[0] - 137, 2) +
        math.pow(colour[1] - 137, 2) +
        math.pow(colour[2] - 142, 2)
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