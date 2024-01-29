import cv2
import math





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



        return (
            self.describeFacialHairThickness(pixels, facialHairPixels),
            self.describeFacialHairColour()
            )








    def describeFacialHairThickness(self, pixels, facialHairPixels):
        #Calculates the proportion of pixels that we deem to be facial hair pixels and classifies the image based on that

        facialHairPercentage = len(facialHairPixels) / len(pixels)



        #<75% - no facial hair
        #75-90% - light facial hair
        #90+% - thick facial hair
        if(facialHairPercentage<0.75):
            return "none"
        elif(facialHairPercentage<0.9):
            return "light"
        else:
            return "thick"







    def describeFacialHairColour(self):
        return "TODO"









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