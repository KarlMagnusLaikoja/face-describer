import cv2
import math






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




        #Gather all the found RGB
        colours = []
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
        #These are found by getting the median RGB values of each skin colour category
        #Categories: https://dermnetnz.org/topics/skin-phototype
        #Skin colour RGB values: https://www.researchgate.net/publication/310443424_Improvement_of_Haar_Feature_Based_Face_Detection_in_OpenCV_Incorporating_Human_Skin_Color_Characteristic
        #Pale white: [255, 218, 190]
        #Fair: [240, 184, 160]
        #Darker white: [195, 149, 130]
        #Light brown: [150, 114, 100]
        #Brown: [105, 80, 70]
        #Dark brown or black: [60, 46, 40]



        #Compare the found RGB values to the representative values and return the smallest found value
        differenceFromPaleWhite = math.sqrt(
            math.pow(colour[0] - 255, 2) +
            math.pow(colour[1] - 218, 2) +
            math.pow(colour[2] - 190, 2)
        )



        differenceFromFair = math.sqrt(
            math.pow(colour[0] - 240, 2) +
            math.pow(colour[1] - 184, 2) +
            math.pow(colour[2] - 160, 2)
        )



        differenceFromDarkerWhite = math.sqrt(
            math.pow(colour[0] - 195, 2) +
            math.pow(colour[1] - 149, 2) +
            math.pow(colour[2] - 130, 2)
        )



        differenceFromLightBrown = math.sqrt(
            math.pow(colour[0] - 150, 2) +
            math.pow(colour[1] - 114, 2) +
            math.pow(colour[2] - 100, 2)
        )



        differenceFromBrown = math.sqrt(
            math.pow(colour[0] - 105, 2) +
            math.pow(colour[1] - 80, 2) +
            math.pow(colour[2] - 70, 2)
        )



        differenceFromDarkBrownOrBlack = math.sqrt(
            math.pow(colour[0] - 60, 2) +
            math.pow(colour[1] - 46, 2) +
            math.pow(colour[2] - 40, 2)
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