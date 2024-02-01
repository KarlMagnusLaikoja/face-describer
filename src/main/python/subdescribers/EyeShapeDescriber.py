import cv2
import numpy as np





class EyeShapeDescriber:

    def __init__(self, image, leftEyeCoordinates, rightEyeCoordinates):

        self.image = image
        self.leftEyeCoordinates = leftEyeCoordinates
        self.rightEyeCoordinates = rightEyeCoordinates





    def describe(self):

        return self.describeEyeShape(self.leftEyeCoordinates, self.rightEyeCoordinates)







    def describeEyeShape(self, leftEyeCoordinates, rightEyeCoordinates):
        #Coordinates of both eyes in format: ((lowestX, highestX), (lowestY, highestY))



        #Read in the templates to which we will compare the eyes to
        templates = readTemplates()



        #Crop the image using the eye coordinates
        left_eye = self.image[
                   leftEyeCoordinates[1][0]:leftEyeCoordinates[1][1],
                   leftEyeCoordinates[0][0]:leftEyeCoordinates[0][1]
               ]

        right_eye = self.image[
                    rightEyeCoordinates[1][0]:rightEyeCoordinates[1][1],
                    rightEyeCoordinates[0][0]:rightEyeCoordinates[0][1]
                  ]


        #Resize the input images to be the same size as the templates
        left_eye = cv2.resize(left_eye, (16, 6))
        right_eye = cv2.resize(right_eye, (16, 6))


        #Greyscale the input images
        left_eye = cv2.cvtColor(
            left_eye,
            cv2.COLOR_BGR2GRAY
        )

        right_eye = cv2.cvtColor(
            right_eye,
            cv2.COLOR_BGR2GRAY
        )




        #Go over the inputs with all of the templates, find the best match
        best_template = ""
        best_template_similarity = -9999999
        for key, (value_left, value_right) in templates.items():

            #Left
            res_left = cv2.matchTemplate(left_eye,value_left,cv2.TM_CCOEFF_NORMED) #Template matches across the entire image
            similarity_left = np.max(res_left) #Get the best match

            #Right
            res_right = cv2.matchTemplate(right_eye,value_right,cv2.TM_CCOEFF_NORMED)
            similarity_right = np.max(res_right)

            if( (similarity_left+similarity_right)/2 > best_template_similarity): #If that match beats the previous ones, consider this template to be the best match
                best_template_similarity = (similarity_left+similarity_right)/2
                best_template = key
        return best_template







def readTemplates():
    #Reads the eye shape templates into a list
    #Separate templates for left, right eye



    templates = {
        "almond": (None, None),
        "round": (None, None),
        "monolid": (None, None),
        "downturned": (None, None),
        "upturned": (None, None),
        "hooded": (None, None),
    }


    #Due to input format we need to greyscale the templates once more
    templates["almond"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/almond_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/almond_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )



    templates["round"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/round_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/round_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )



    templates["monolid"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/monolid_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/monolid_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )



    templates["downturned"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/downturned_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/downturned_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )



    templates["upturned"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/upturned_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/upturned_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )



    templates["hooded"] = (
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/hooded_left.png"),
            cv2.COLOR_BGR2GRAY
        ),
        cv2.cvtColor(
            cv2.imread("templates/eyeshapes/hooded_right.png"),
            cv2.COLOR_BGR2GRAY
        )
    )






    return templates


