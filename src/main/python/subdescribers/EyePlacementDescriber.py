




class EyePlacementDescriber:

    def __init__(self,leftEyeCoordinates, rightEyeCoordinates):

        self.leftEyeCoordinates = leftEyeCoordinates
        self.rightEyeCoordinates = rightEyeCoordinates





    def describe(self):

        return self.describeEyePlacement(self.leftEyeCoordinates, self.rightEyeCoordinates)







    def describeEyePlacement(self, leftEyeCoordinates, rightEyeCoordinates):

        #Coordinates of both eyes in format: ((lowestX, highestX), (lowestY, highestY))

        #Distance between eyes divided by eye width
        ratio = getDistanceBetweenEyes(leftEyeCoordinates, rightEyeCoordinates) / getAverageEyeWidth(leftEyeCoordinates, rightEyeCoordinates)

        #Due to face-recognition coordinates being somewhat off (the corners of the eyes are left out to a degree),
        #we need to apply a constant in order to get more accurate results.
        #This number was found by simple trial and error.
        const = 0.66

        #Close-set: < 1 eye width between eyes
        #Wide-set: >= 1 eye width between eyes
        return "close-set" if ratio*const < 1 else "wide-set"



def getDistanceBetweenEyes(leftEyeCoordinates, rightEyeCoordinates):

    #Gets the distance between eyes in pixels

    return leftEyeCoordinates[0][0] - rightEyeCoordinates[0][1]




def getAverageEyeWidth(leftEyeCoordinates, rightEyeCoordinates):

    #Gets the average eye width in pixels

    return  (
            (leftEyeCoordinates[0][1] - leftEyeCoordinates[0][0]) +
            (rightEyeCoordinates[0][1] - rightEyeCoordinates[0][0])
            ) / 2


