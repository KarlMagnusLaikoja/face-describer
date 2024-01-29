import face_recognition
import sys
import cv2
from subdescribers.EyeColourDescriber import EyeColourDescriber
from subdescribers.SkinColourDescriber import SkinColourDescriber
from subdescribers.FaceShapeDescriber import FaceShapeDescriber
from subdescribers.FacialHairDescriber import FacialHairDescriber
from subdescribers.NoseShapeDescriber import NoseShapeDescriber









def getCoordinatesFromPoints(coordinates):
    #Gets the pair of "lowest" and "highest" coordinates within a set of coordinates/points
    xCoordinates = [pair[0] for pair in coordinates]
    yCoordinates = [pair[1] for pair in coordinates]
    lowestX = min(xCoordinates)
    lowestY = min(yCoordinates)
    highestX = max(xCoordinates)
    highestY = max(yCoordinates)
    return ((lowestX, highestX), (lowestY, highestY))

class FaceDescriber:


    def __init__(self, image, language):

        self.image = cv2.imread("../../../"+image)
        self.language = language

        self.output_EN = {
            "face shape": "",
            "skin colour": "",
            "right eye colour": "",
            "left eye colour": "",
            "facial hair thickness": "",
            "facial hair colour": "",
            "nose shape": ""
        }

        self.output_EE = {
            "näo kuju": "",
            "naha värv": "",
            "parema silma värv": "",
            "vasaku silma värv": "",
            "näokarvade tihedus": "",
            "näokarvade värv": "",
            "nina kuju": ""
        }




    def assertSingleFace(self, face_landmarks_list):

        if(len(face_landmarks_list)==0):

            if(self.language=="EE"):
                print("Pildilt ei tuvastatud ühtegi nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Couldn't detect any faces.")
                sys.exit(101)

        elif(len(face_landmarks_list)>1):

            if(self.language=="EE"):
                print("Pildilt tuvastati mitu nägu.")
                sys.exit(101)
            elif(self.language=="EN"):
                print("Multiple faces were detected.")
                sys.exit(101)




    def describe(self):

        image = self.image
        face_landmarks_list = face_recognition.face_landmarks(image)

        #Verify that the image only contains a single face
        self.assertSingleFace(face_landmarks_list)
        face_landmarks = face_landmarks_list[0]

        #Gather all the coordinates into a single list
        coordinates = []
        for k, v in face_landmarks.items():
            for (x, y) in v:
                coordinates.append((x, y))




        #Describe face shape
        #params: entire face coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeFaceShape(
            (
                (coordinates[0][0], coordinates[16][0]),
                (coordinates[24][1], coordinates[8][1])
            )
        )





        #Describe skin colour
        #params: left cheek area coordinates in format ((lowestX, highestX), (lowestY, highestY))
        skinColourRGB = self.describeSkinColour(
            (
                (coordinates[10][0], coordinates[13][0]),
                (coordinates[1][1], coordinates[35][1])
            )
        )





        #Describe eyecolour
        #params: left eye coordinates, right eye coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeEyeColour(
            (
                (coordinates[43][0], coordinates[46][0]),
                (coordinates[43][1], coordinates[46][1])
            ),
            (
                (coordinates[37][0], coordinates[40][0]),
                (coordinates[37][1], coordinates[40][1])
            )
        )






        #Describe facial hair
        #params: coordinates of facial hair areas in format [((lowestX, highestX), (lowestY, highestY)), ((lowestX, highestX), (lowestY, highestY)), ...]
        # and skin colour's RGB value
        facialHairCoordinates = [
            ((coordinates[7][0], coordinates[8+1][0]), (coordinates[5][1], coordinates[7+1][1])),
            ((coordinates[7][0], coordinates[8+1][0]), (coordinates[33][1], coordinates[49+1][1])),
            ((coordinates[10][0], coordinates[11+1][0]), (coordinates[57][1], coordinates[11+1][1])),
            ((coordinates[5][0], coordinates[6+1][0]), (coordinates[57][1], coordinates[11+1][1]))
        ]
        self.describeFacialHair(
            facialHairCoordinates,
            skinColourRGB
        )




        #Describe nose shape
        #params: nose coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeNoseShape(
            (
                (coordinates[39][0], coordinates[41+1][0]),
                (coordinates[27][1], coordinates[33+1][1])
            )
        )







        #Return output based on provided language code
        if(self.language=="EE"):
            return self.output_EE
        elif(self.language=="EN"):
            return self.output_EN







    def describeFaceShape(self, coordinates):

        #Instantiate face shape describer
        faceShapeDescriber = FaceShapeDescriber(self.image, coordinates)

        #Describe face shape
        shape = faceShapeDescriber.describe()

        #Mapping from english to estonian
        shapeMapping = {
            "diamond": "teemant",
            "oblong": "oblong",
            "oval": "ovaal",
            "round": "ümmargune",
            "square": "ruut",
        }


        self.output_EN["face shape"] = shape
        self.output_EE["näo kuju"] = shapeMapping[shape]







    def describeSkinColour(self, coordinates):

        #Instantiate skin colour describer
        skinColourDescriber = SkinColourDescriber(self.image, coordinates)

        #Describe skin colour
        (r, g, b), colour = skinColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "pale white": "kahvatu valge",
            "fair": "hele",
            "darker white": "tumedam valge",
            "light brown": "helepruun",
            "brown": "pruun",
            "dark brown or black": "tumepruun või must"
        }


        self.output_EN["skin colour"] = colour
        self.output_EE["naha värv"] = colourMapping[colour]


        return (r, g, b)


    def describeEyeColour(self, leftEyeCoordinates, rightEyeCoordinates):

        #Instantiate eye colour describer
        eyeColourDescriber = EyeColourDescriber(self.image, leftEyeCoordinates, rightEyeCoordinates)

        #Describe both eyes
        #Return format: ("blue", "brown")
        leftEyeColour, rightEyeColour = eyeColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "blue": "sinine",
            "brown": "pruun",
            "green": "roheline",
            "grey": "hall",
            "hazel": "pähkelpruun",
            "red": "punane"
        }


        self.output_EN["left eye colour"] = leftEyeColour
        self.output_EN["right eye colour"] = rightEyeColour

        self.output_EE["vasaku silma värv"] = colourMapping[leftEyeColour]
        self.output_EE["parema silma värv"] = colourMapping[rightEyeColour]







    def describeFacialHair(self, facialHairCoordinates, skinColourRGB):

        #Instantiate facial hair describer
        facialHairDescriber = FacialHairDescriber(self.image, facialHairCoordinates, skinColourRGB)

        #Describe facial hair thickness and colour
        thickness, colour = facialHairDescriber.describe()


        #Mapping from english to estonian
        thicknessMapping = {
            "none": "puudub",
            "thin": "õhuke",
            "thick": "tihe"
        }
        colourMapping = {
            "red": "punane",
            "blonde": "blond",
            "brown": "pruun",
            "black": "must",
            "grey": "hall",
            "": ""
        }



        self.output_EN["facial hair thickness"] = thickness
        self.output_EN["facial hair colour"] = colour

        self.output_EE["näokarvade tihedus"] = thicknessMapping[thickness]
        self.output_EE["näokarvade värv"] = colourMapping[colour]









    def describeNoseShape(self, coordinates):

        #Instantiate nose shape describer
        noseShapeDescriber = NoseShapeDescriber(self.image, coordinates)

        #Describe nose shape
        shape = noseShapeDescriber.describe()

        #Mapping from english to estonian
        shapeMapping = {
            "bulbous": "sibulakujuline",
            "button": "nööpnina",
            "crooked": "kõver",
            "East Asian": "Ida-Aasia",
            "fleshy": "lihav",
            "Greek": "Kreeka",
            "hawk": "kull/kongus",
            "Nubian": "Nuubia",
            "Roman": "Rooma",
            "upturned": "ülespööratud"
        }


        self.output_EN["nose shape"] = shape
        self.output_EE["nina kuju"] = shapeMapping[shape]














fileName = sys.argv[1]
language = sys.argv[2]
print(FaceDescriber(fileName, language).describe())



