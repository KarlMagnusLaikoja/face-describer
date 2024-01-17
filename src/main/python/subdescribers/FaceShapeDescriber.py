import cv2
import numpy as np

class FaceShapeDescriber:
    def __init__(self, image, coordinates):
        self.image = image
        self.coordinates = coordinates

    def describe(self):
        return self.describeFaceShape(self.coordinates)


    def describeFaceShape(self, coordinates):
        #coordinates format: ((lowestX, highestX), (lowestY, highestY))

        #Read in the templates to which we will compare the face to
        templates = readTemplates()

        #Crop the image using the face coordinates
        face = self.image[
               coordinates[1][0]:coordinates[1][1],
               coordinates[0][0]:coordinates[0][1]
               ]

        #Resize the input image to be the same size as the templates
        face = cv2.resize(face, (110, 110))


        #Go over the input with all of the templates, find the best match
        best_template = ""
        best_template_similarity = -9999999
        for key, value in templates.items():
            res = cv2.matchTemplate(face,value,cv2.TM_CCOEFF_NORMED) #Template matches across the entire image
            similarity = np.max(res) #Get the best match
            if(similarity > best_template_similarity): #If that match beats the previous ones, consider this template to be the best match
                best_template_similarity = similarity
                best_template = key
        return best_template


def readTemplates():
    templates = {
        "diamond": None,
        "oblong": None,
        "oval": None,
        "round": None,
        "square": None
    }

    templates["diamond"] = cv2.imread("templates/faceshapes/diamond.png")
    templates["oblong"] = cv2.imread("templates/faceshapes/oblong.png")
    templates["oval"] = cv2.imread("templates/faceshapes/oval.png")
    templates["round"] = cv2.imread("templates/faceshapes/round.png")
    templates["square"] = cv2.imread("templates/faceshapes/square.png")

    return templates


