import cv2
import math
import numpy as np





class HairDescriber:

    def __init__(self, image, coordinates, skinColourRGB):

        self.image = image
        self.coordinates = coordinates
        self.skinColourRGB = skinColourRGB

    def describe(self):

        return self.describeHair(self.image, self.coordinates, self.skinColourRGB)


    def describeHair(self, img, coordinates, skinColourRGB):
        #coordinates format: ((lowestX, highestX), (lowestY, highestY))

        #Greyscaling
        mask = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #Detect edges
        mask = cv2.Canny(mask,50,100)

        #Remove vertical lines created on the edges of the image as a result of edge detection
        mask = cropWidth(mask, 5) #5px should be safe for practically all input images


        #Find the y-coordinate of the first white pixel in the result - this is the start of the hairline.
        minY = getYcoordinateOfFirst(mask, 255)


        #Crop the image using the found hairline y-coordinate as the beginning y-coordinate
        #and the provided coordinates (from face-recognition) for ending y-coordinate and x-coordinates.
        mask = mask[
            minY : coordinates[1][1],
            coordinates[0][0] : coordinates[0][1]
        ]


        #Apply morphology to connect the edges, 7px should be enough
        ones = np.ones((7,7), dtype='uint8')
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ones)



        #Find the external edges/contours and fill in the area within them with white
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        mask = cv2.fillConvexPoly(mask, contours[-1], lineType=8, shift=0, color = (255, 255, 255))



        #The resulting image is a black and white image of the forehead and hair, with the background being black
        #and the forehead/hair being white.




        #Crop the original coloured image with the same coordinates
        hairAndForehead = img[
            minY : coordinates[1][1],
            coordinates[0][0] : coordinates[0][1]
        ]


        #Find the pixels of the forehead and pixels of the hair
        hairPixels, foreheadPixels = findHairAndForeheadPixels(hairAndForehead, mask, skinColourRGB)


        #Change hairPixels format from BGR to RGB
        hairPixels = [[r, g, b] for [b, g, r] in hairPixels]


        #Return whether the person in the image has hair based on the ratio of hair to hair+forehead
        return hasHair(hairPixels,
                       foreheadPixels,
                       0.1 #Threshold found by manual finetuning 0.1
                       ), hairPixels #Also return the hair pixels so that we can find the hair colour later


def cropWidth(img, px):
    #Crops the width of the input image by "px" pixels on either side
    h, w = img.shape
    return img[
        : h,
        px : (w-px)
    ]





def getYcoordinateOfFirst(img, color):
    #Finds the y-coordinate of the first pixel with the provided color, starting from the top of the image
    minY = 0
    minYFound = False
    for y in img:
        if(minY < 5): #Ignore the first 5 pixels due to edge detection creating horizontal lines in the top of the image
            minY+=1
            continue
        for x in y:
            if (x == color):
                minYFound = True
                break
        if(minYFound):
            break
        minY+=1

    return minY







def findHairAndForeheadPixels(img, mask, skinColour):
    #Gathers hair and forehead pixels into two separate lists by going over each pixel in the image
    #and the corresponding mask. If the pixel in the mask is white, then the pixel in the original image is either
    #that of the forehead or hair. Comparing the pixel to the skin colour will determine which of the two it is.
    hairPixels = []
    foreheadPixels = []
    for i in range(len(img)):
        for j in range(len(img[i])):
            if(mask[i][j] == 0): #Black pixel in mask/contour image, meaning this pixel belongs to the background
                continue
            if(isForeheadPixel(img[i][j], skinColour, 0.495)): #Threshold found by manual finetuning. If true, then the pixel is close enough to the skin colour,
                #meaning that the pixel belongs to the forehead.
                foreheadPixels.append(img[i][j])
            else:
                hairPixels.append(img[i][j])
    return hairPixels, foreheadPixels






def isForeheadPixel(pixel, skinColour, threshold):
    #Compares pixel to skin colour with the maximum difference allowed being the threshold
    #Get the difference for each r, g, b value - if the average is below the threshold, return true
    rDiff = math.sqrt(math.pow(pixel[0]-skinColour[0], 2)) / skinColour[0]
    gDiff = math.sqrt(math.pow(pixel[1]-skinColour[1], 2)) / skinColour[1]
    bDiff = math.sqrt(math.pow(pixel[2]-skinColour[2], 2)) / skinColour[2]

    return (rDiff+gDiff+bDiff)/3 < threshold



def hasHair(hairPixels, foreheadPixels, threshold):

    #Returns true if the ratio of hair pixels to forehead+hair pixels is at least the provided threshold

    return "false" if len(hairPixels)/(len(hairPixels)+len(foreheadPixels)) < threshold else "true"