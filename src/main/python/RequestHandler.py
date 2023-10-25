import sys
import io
import numpy as np
import cv2
from describer import FaceDescriber

#These have previously been validated already
base64Image = sys.argv[1]
language = sys.argv[2]


#Convert
"""in_memory_file = io.BytesIO()
base64Image.save(in_memory_file)
data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
color_image_flag = 1
img = cv2.imdecode(data, color_image_flag)

#result = FaceDescriber(img).describe()
"""
result = "Placeholder results from RequestHandler.py xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx xxxxxxxxx "
print(result)