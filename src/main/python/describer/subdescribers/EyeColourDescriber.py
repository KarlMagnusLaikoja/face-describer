"""import face_recognition
import cv2
import extcolors
from PIL import Image

class EyeColourDescriber:
    def __init__(self, image, output):
        self.image = image
        self.output = output

    def describe(self):
        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)
        rightEyeCoordinates = face_landmarks_list[0]["right_eye"]
        leftEyeCoordinates = face_landmarks_list[0]["left_eye"]

        rightEyeColour = findEyeColour(rightEyeCoordinates, image)
        leftEyeColour = findEyeColour(leftEyeCoordinates, image)

        if(rightEyeColour==leftEyeColour):
            return self.output.replace("%eyeColour%", rightEyeColour)
        else:
            return self.output.replace("värvi", "").replace("%eyeColour%", "eri värvi (vasak "+leftEyeColour+", parem "+rightEyeColour+")")


def findEyeColour(coordinates, image):
    lowestX = 99999
    highestX = 0
    lowestY = 99999
    highestY = 0
    for coordinatePair in coordinates:
        if(coordinatePair[0]<lowestX):
            lowestX = coordinatePair[0]
        if(coordinatePair[0]>highestX):
            highestX = coordinatePair[0]
        if(coordinatePair[1]<lowestY):
            lowestY = coordinatePair[1]
        if(coordinatePair[1]>highestY):
            highestY = coordinatePair[1]


    eye = image[lowestY:highestY, lowestX:highestX]
    eye = cv2.cvtColor(eye, cv2.COLOR_BGR2RGB)
    eye_pil = Image.fromarray(eye) #https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    colors = extcolors.extract_from_image(eye_pil, tolerance = 12, limit = 12)[0]
    colors = [rgb[0] for rgb in colors]


    differenceFromBlue = 999999
    differenceFromBrown = 999999
    differenceFromGreen = 999999
    differenceFromGrey = 999999
    differenceFromHazel = 999999
    differenceFromRed = 999999
    #Kauguse valem: Absoluutväärtus leitud värvide ja võrreldavate värvide vastavate RGB väärtuste vahede korrutisest.
    for foundRGB in colors:
        #Erinevus sinisest
        if(abs((foundRGB[0]-78)*(foundRGB[1]-113)*(foundRGB[2]-132))<differenceFromBlue):
            differenceFromBlue = abs((foundRGB[0]-78)*(foundRGB[1]-113)*(foundRGB[2]-132))
        #Erinevus pruunist
        if(abs((foundRGB[0]-52)*(foundRGB[1]-32)*(foundRGB[2]-23))<differenceFromBrown):
            differenceFromBrown = abs((foundRGB[0]-52)*(foundRGB[1]-32)*(foundRGB[2]-23))
        #Erinevus rohelisest
        if(abs((foundRGB[0]-83)*(foundRGB[1]-88)*(foundRGB[2]-47))<differenceFromGreen):
            differenceFromGreen = abs((foundRGB[0]-83)*(foundRGB[1]-88)*(foundRGB[2]-47))
        #Erinevus hallist
        if(abs((foundRGB[0]-155)*(foundRGB[1]-156)*(foundRGB[2]-160))<differenceFromGrey):
            differenceFromGrey = abs((foundRGB[0]-155)*(foundRGB[1]-156)*(foundRGB[2]-160))
        #Erinevus pähkelpruunist
        if(abs((foundRGB[0]-124)*(foundRGB[1]-104)*(foundRGB[2]-49))<differenceFromHazel):
            differenceFromHazel = abs((foundRGB[0]-124)*(foundRGB[1]-104)*(foundRGB[2]-49))
        #Erinevus punasest
        if(abs((foundRGB[0]-151)*(foundRGB[1]-90)*(foundRGB[2]-102))<differenceFromRed):
            differenceFromRed = abs((foundRGB[0]-151)*(foundRGB[1]-90)*(foundRGB[2]-102))


    #Väikseima erinevusega värv on antud silma värv
    diffAndColor = {differenceFromBlue: "sinist", differenceFromBrown: "pruuni", differenceFromGreen: "rohelist", differenceFromGrey: "halli", differenceFromHazel: "pähkelpruuni", differenceFromRed: "punast"}
    result = ""
    diff = 9999999
    for key in diffAndColor:
        if(key<diff):
            diff = key
            result = diffAndColor[key]

    return result

"""