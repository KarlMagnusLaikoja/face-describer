import cv2
import math
import numpy as np





class FacialHairDescriber:

    def __init__(self, image, coordinates, skinColourRGB):

        self.image = image
        self.coordinates = coordinates
        self.skinColourRGB = skinColourRGB

    def describe(self):

        return self.describeFacialHair(self.coordinates)


    def describeFacialHair(self, coordinates):
        #coordinates format: [((lowestX, highestX), (lowestY, highestY)), ((lowestX, highestX), (lowestY, highestY)), ...] for
        #the chin, upper lip and both cheeks



        #Crop the image using the coordinates and make a list
        images = [
            self.image[
                lowestY:highestY,
                lowestX:highestX
            ]
            for ((lowestX, highestX), (lowestY, highestY)) in coordinates
        ]



        #Gather all of the pixels within the images into a list
        pixels = getAllPixels(images)



        #From the pixels, pick the ones which differ from the skin colour by at least the provided threshold (25%).
        facialHairPixels = getFacialHairPixels(pixels, self.skinColourRGB, 0.25)


        thickness = self.describeFacialHairThickness(pixels, facialHairPixels)
        colour = ""
        if(thickness != "none"):
            colour = self.describeFacialHairColour(facialHairPixels)
        return (
            thickness,
            colour
            )








    def describeFacialHairThickness(self, pixels, facialHairPixels):
        #Calculates the proportion of pixels that we deem to be facial hair pixels and classifies the image based on that

        facialHairPercentage = len(facialHairPixels) / len(pixels)



        #<75% - no facial hair
        #75-90% - thin facial hair
        #90+% - thick facial hair
        if(facialHairPercentage<0.75):
            return "none"
        elif(facialHairPercentage<0.9):
            return "thin"
        else:
            return "thick"







    def describeFacialHairColour(self, facialHairPixels):
        #Compares the average RGB values within the "facial hair pixels" to representatives and classifies the image based on that

        #Get the average RGB value of the facial hair pixels
        (r, g, b) = getAverageRGB(facialHairPixels)


        #Compare it to representatives
        return compareRGB( (r, g, b) )









def getAllPixels(images):
    #Function to gather all pixels (RGB values) within a list of images

    colours = []
    for x in range(len(images)):
        image = None
        try: #Sometimes we can't crop all 4 locations, then continue with those that we can
            image = cv2.cvtColor(images[x], cv2.COLOR_BGR2RGB)
        except:
            continue
        for i in range(len(image)):
            for j in range(len(image[i])):
                colours.append(image[i][j])
    return colours








def getFacialHairPixels(pixels, skinColour, threshold):
    #Get all pixels that differ from the skin colour by at least the provided threshold
    #These will be considered pixels containing facial hair

    facialHairPixels = []
    for i in range(len(pixels)):
        isFacialHairPixel = pixelDiffersOverThreshold(pixels[i], skinColour, threshold)
        if(isFacialHairPixel):
            facialHairPixels.append(pixels[i])

    return facialHairPixels









def pixelDiffersOverThreshold(colour1, colour2, threshold):
    #Find out if colour1 differs from colour2 by at least the provided threshold
    #Get the difference for each r, g, b value - if the average exceeds the threshold, return true


    rDiff = math.sqrt(math.pow(colour1[0]-colour2[0], 2)) / colour2[0]
    gDiff = math.sqrt(math.pow(colour1[1]-colour2[1], 2)) / colour2[1]
    bDiff = math.sqrt(math.pow(colour1[2]-colour2[2], 2)) / colour2[2]

    return (rDiff+gDiff+bDiff)/3 >= threshold












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