import face_recognition
import sys
import cv2
from subdescribers.EyeColourDescriber import EyeColourDescriber
from subdescribers.SkinColourDescriber import SkinColourDescriber
from subdescribers.FaceShapeDescriber import FaceShapeDescriber
from subdescribers.FacialHairDescriber import FacialHairDescriber
from subdescribers.FacialHairColourDescriber import FacialHairColourDescriber
from subdescribers.NoseShapeDescriber import NoseShapeDescriber
from subdescribers.EyeShapeDescriber import EyeShapeDescriber
from subdescribers.EyePlacementDescriber import EyePlacementDescriber
from subdescribers.HairDescriber import HairDescriber
from subdescribers.HairColourDescriber import HairColourDescriber









class FaceDescriber:


    def __init__(self, image, language):

        self.image = cv2.imread("../../../"+image)
        self.language = language

        self.output_EN = {
            "general": {
                "skin_colour": "",
                "face_shape": ""
            },
            "eyes": {
                "shape": "",
                "placement": "",
                "colour_right": "",
                "colour_left": ""
            },
            "nose": {
                "shape": ""
            },
            "facial_hair": {
                "thickness": "",
                "colour": ""
            },
            "hair": {
                "has_hair": "",
                "colour": ""
            }
        }


        self.output_EE = {
            "üldine": {
                "naha_värv": "",
                "näo_kuju": ""
            },
            "silmad": {
                "kuju": "",
                "asetus": "",
                "värv_parem": "",
                "värv_vasak": ""
            },
            "nina": {
                "kuju": ""
            },
            "näokarvad": {
                "tihedus": "",
                "värv": ""
            },
            "juuksed": {
                "on_olemas": "",
                "värv": ""
            }
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
        #params: all the coordinates
        self.describeFaceShape(coordinates)





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






        #Describe facial hair thickness
        #params: coordinates of facial hair areas in format [((lowestX, highestX), (lowestY, highestY)), ((lowestX, highestX), (lowestY, highestY)), ...]
        # and skin colour's RGB value
        facialHairCoordinates = [
            ((coordinates[7][0], coordinates[9][0]), (coordinates[5][1], coordinates[8][1])),
            ((coordinates[7][0], coordinates[9][0]), (coordinates[33][1], coordinates[50][1])),
            ((coordinates[10][0], coordinates[12][0]), (coordinates[57][1], coordinates[12][1])),
            ((coordinates[5][0], coordinates[7][0]), (coordinates[57][1], coordinates[12][1]))
        ]
        facialHairThickness, facialHairPixels = self.describeFacialHair(
            facialHairCoordinates,
            skinColourRGB
        )



        if(facialHairThickness != "none"):
            #Describe facial hair colour
            #params: List of facial hair pixels
            self.describeFacialHairColour(facialHairPixels)







        #Describe nose shape
        #params: nose coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeNoseShape(
            (
                (coordinates[39][0], coordinates[42][0]),
                (coordinates[27][1], coordinates[34][1])
            )
        )




        #Describe eye shape
        #params: left eye, right eye coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeEyeShape(
            getCoordinatesFromPoints(coordinates[42:48]),
            getCoordinatesFromPoints(coordinates[36:42])
        )




        #Describe eye placement
        #params: left eye, right eye coordinates in format ((lowestX, highestX), (lowestY, highestY))
        self.describeEyePlacement(
            getCoordinatesFromPoints(coordinates[42:48]),
            getCoordinatesFromPoints(coordinates[36:42])
        )




        #Describe hair (whether they have it or not)
        #params: coordinates of the face and whatever is above it (starting y-coordinate is 0) in format ((lowestX, highestX), (lowestY, highestY))
        #returns boolean value (whether the person has hair or not) and the list of hair pixels to find the hair colour later
        hasHair, hairPixels = self.describeHair(
            (
                (coordinates[0][0], coordinates[16][0]),
                (0, coordinates[19][1])
            ),
            skinColourRGB
        )




        if(hasHair == "true"):
            #Describe hair colour
            #params: list of hair pixels
            self.describeHairColour(hairPixels)





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


        self.output_EN["general"]["face_shape"] = shape
        self.output_EE["üldine"]["näo_kuju"] = shapeMapping[shape]







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


        self.output_EN["general"]["skin_colour"] = colour
        self.output_EE["üldine"]["naha_värv"] = colourMapping[colour]


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


        self.output_EN["eyes"]["colour_left"] = leftEyeColour
        self.output_EN["eyes"]["colour_right"] = rightEyeColour

        self.output_EE["silmad"]["värv_vasak"] = colourMapping[leftEyeColour]
        self.output_EE["silmad"]["värv_parem"] = colourMapping[rightEyeColour]







    def describeFacialHair(self, facialHairCoordinates, skinColourRGB):

        #Instantiate facial hair describer
        facialHairDescriber = FacialHairDescriber(self.image, facialHairCoordinates, skinColourRGB)

        #Describe facial hair thickness
        thickness, facialHairPixels = facialHairDescriber.describe()


        #Mapping from english to estonian
        thicknessMapping = {
            "none": "puudub",
            "thin": "õhuke",
            "thick": "tihe"
        }


        self.output_EN["facial_hair"]["thickness"] = thickness
        self.output_EE["näokarvad"]["tihedus"] = thicknessMapping[thickness]


        return thickness, facialHairPixels #Return the list of facial hair pixels so the colour can be found




    def describeFacialHairColour(self, facialHairPixels):

        #Instantiate facial hair colour describer
        facialHairColourDescriber = FacialHairColourDescriber(facialHairPixels)

        #Describe facial hair colour
        colour = facialHairColourDescriber.describe()


        #Mapping from english to estonian
        colourMapping = {
            "red": "punane",
            "blonde": "blond",
            "brown": "pruun",
            "black": "must",
            "grey": "hall",
        }



        self.output_EN["facial_hair"]["colour"] = colour
        self.output_EE["näokarvad"]["värv"] = colourMapping[colour]






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


        self.output_EN["nose"]["shape"] = shape
        self.output_EE["nina"]["kuju"] = shapeMapping[shape]




    def describeEyeShape(self, leftEyeCoordinates, rightEyeCoordinates):

        #Instantiate eye shape describer
        eyeShapeDescriber = EyeShapeDescriber(self.image, leftEyeCoordinates, rightEyeCoordinates)

        #Describe eye shape
        shape = eyeShapeDescriber.describe()

        #Mapping from english to estonian
        shapeMapping = {
            "almond": "mandel",
            "round": "ümmargune",
            "monolid": "monoliidne",
            "downturned": "alla suunatud",
            "upturned": "üles suunatud",
            "hooded": "varjatud/kapuutsiga",
        }


        self.output_EN["eyes"]["shape"] = shape
        self.output_EE["silmad"]["kuju"] = shapeMapping[shape]




    def describeEyePlacement(self, leftEyeCoordinates, rightEyeCoordinates):

        #Instantiate eye placement describer
        eyePlacementDescriber = EyePlacementDescriber(leftEyeCoordinates, rightEyeCoordinates)

        #Describe eye placement
        placement = eyePlacementDescriber.describe()

        #Mapping from english to estonian
        placementMapping = {
            "close-set": "lähedal asetsevad",
            "wide-set": "laia asetusega"
        }


        self.output_EN["eyes"]["placement"] = placement
        self.output_EE["silmad"]["asetus"] = placementMapping[placement]




    def describeHair(self, coordinates, skinColourRGB):

        #Instantiate hair describer
        hairDescriber = HairDescriber(self.image, coordinates, skinColourRGB)

        #Describe hair
        hasHair, hairPixels = hairDescriber.describe()

        #Mapping from english to estonian
        mapping = {
            "true": "tõene",
            "false": "väär"
        }


        self.output_EN["hair"]["has_hair"] = hasHair
        self.output_EE["juuksed"]["on_olemas"] = mapping[hasHair]

        return hasHair, hairPixels #Return list of hair pixels to find the colour





    def describeHairColour(self, hairPixels):

        #Instantiate hair colour describer
        hairColourDescriber = HairColourDescriber(hairPixels)

        #Describe hair colour
        colour = hairColourDescriber.describe()

        #Mapping from english to estonian
        colourMapping = {
            "red": "punane",
            "blonde": "blond",
            "brown": "pruun",
            "black": "must",
            "grey": "hall",
        }


        self.output_EN["hair"]["colour"] = colour
        self.output_EE["juuksed"]["värv"] = colourMapping[colour]


def getCoordinatesFromPoints(coordinates):
    #Gets the pair of "lowest" and "highest" coordinates within a list of coordinates/points
    xCoordinates = [pair[0] for pair in coordinates]
    yCoordinates = [pair[1] for pair in coordinates]
    lowestX = min(xCoordinates)
    lowestY = min(yCoordinates)
    highestX = max(xCoordinates)
    highestY = max(yCoordinates)
    return ((lowestX, highestX), (lowestY, highestY))









fileName = sys.argv[1]
language = sys.argv[2]
print(FaceDescriber(fileName, language).describe())







