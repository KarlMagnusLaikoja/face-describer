import cv2
import numpy as np





class FaceShapeDescriber:

    def __init__(self, image, coordinates):

        self.image = image
        self.coordinates = coordinates





    def describe(self):

        return self.describeFaceShape(self.coordinates)







    def describeFaceShape(self, coordinates):



        #Read in the templates to which we will compare the face to
        templates = readTemplates()



        #Crop the image using some of the face-recognition coordinates and edge detection + manual cropping to get
        #the entire face (including the forehead, which you can't get using just the face-recognition coordinates)
        face = toTemplate(self.image, coordinates)


        #Resize the input image to be the same size as the templates
        face = cv2.resize(face, (110, 163))




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
    #Reads the face shape templates into a list


    templates = {
        "diamond": None,
        "oblong": None,
        "oval": None,
        "round": None,
        "square": None
    }


    #All of the templates need to be greyscaled once again
    templates["diamond"] = cv2.cvtColor(
        cv2.imread("templates/faceshapes/diamond.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["oblong"] = cv2.cvtColor(
        cv2.imread("templates/faceshapes/oblong.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["oval"] = cv2.cvtColor(
        cv2.imread("templates/faceshapes/oval.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["round"] = cv2.cvtColor(
        cv2.imread("templates/faceshapes/round.png"),
        cv2.COLOR_BGR2GRAY
    )

    templates["square"] = cv2.cvtColor(
        cv2.imread("templates/faceshapes/square.png"),
        cv2.COLOR_BGR2GRAY
    )



    return templates





def toTemplate(img, coordinates):
    #Grayscaling
    result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Detect edges
    result = cv2.Canny(result,50,100)

    #Edge detection leaves vertical lines surrounding the image - cutting the image by 5px on each side should suffice
    #and should be safe
    h, w = result.shape
    result = result[
        :h,
        5: (w-5)
        ]

    #Start from the top of the image and find the first white pixels- this is likely
    #to be the first edge (i.e. the hairline), meaning this is where
    #the face actually starts
    minY = 0
    minYFound = False
    for y in result:
        if(minY < 5): #Ignore the first 5 pixels due to horizontal edges being detected at the top of the image
            minY+=1
            continue
        for x in y:
            if (x == 255):
                minYFound = True
                break
        if(minYFound):
            break
        minY+=1

    #Crop the image with the calculated beginning y-coordinate,
    #the x-coordinates and ending y-coordinate can be taken from the coordinates provided by the face-recognition module
    result = result[
             minY: coordinates[8][1],
             coordinates[0][0]:coordinates[16][0]
             ]


    #Result: Black and white image of only the face with the edges detected within the face

    #Even with imperfect conditions such as contours inside the outer contour,
    #the classification should not be affected due to all the templates having their accuracy reduced
    #equally.
    return result