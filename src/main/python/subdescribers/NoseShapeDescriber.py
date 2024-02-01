import cv2
import numpy as np





class NoseShapeDescriber:

    def __init__(self, image, coordinates):

        self.image = image
        self.coordinates = coordinates





    def describe(self):

        return self.describeNoseShape(self.coordinates)







    def describeNoseShape(self, coordinates):
        #coordinates format: ((lowestX, highestX), (lowestY, highestY))



        #Read in the templates to which we will compare the nose to
        templates = readTemplates()



        #Crop the image using the nose coordinates
        nose = self.image[
               coordinates[1][0]:coordinates[1][1],
               coordinates[0][0]:coordinates[0][1]
               ]



        #Resize the input image to be the same size as the templates
        nose = cv2.resize(nose, (25, 30))


        #Greyscale the input image
        nose = cv2.cvtColor(
            nose,
            cv2.COLOR_BGR2GRAY
        )




        #Go over the input with all of the templates, find the best match
        best_template = ""
        best_template_similarity = -9999999
        for key, value in templates.items():
            res = cv2.matchTemplate(nose,value,cv2.TM_CCOEFF_NORMED) #Template matches across the entire image
            similarity = np.max(res) #Get the best match
            if(similarity > best_template_similarity): #If that match beats the previous ones, consider this template to be the best match
                best_template_similarity = similarity
                best_template = key
        return best_template







def readTemplates():
    #Reads the nose shape templates into a list


    templates = {
        "bulbous": None,
        "button": None,
        "crooked": None,
        "East Asian": None,
        "fleshy": None,
        "Greek": None,
        "hawk": None,
        "Nubian": None,
        "Roman": None,
        "upturned": None
    }


    #Due to input format we need to greyscale the template once more
    templates["bulbous"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/bulbous_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["button"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/button_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["crooked"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/crooked_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["East Asian"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/east_asian_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["fleshy"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/fleshy_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["Greek"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/greek_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["hawk"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/hawk_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["Nubian"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/nubian_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["Roman"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/roman_nose.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["upturned"] = cv2.cvtColor(
        cv2.imread("templates/noseshapes/upturned_nose.png"),
        cv2.COLOR_BGR2GRAY
    )


    return templates


