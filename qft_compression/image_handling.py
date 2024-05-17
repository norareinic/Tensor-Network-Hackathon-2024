"""
Example to read and write a png file with python
"""

import os
import numpy as np
from PIL import Image

if __name__ == "__main__":
    filename = "image_compression.png"

    # Load image
    if os.path.isfile(filename):
        image = Image.open(filename)
    else:
        raise IOError(f"File {filename} is not present.")

    # Convert image to numpy array
    original = np.array(image)

    # Here you would do the modifications to the image

    # Get PIL image from numpy array
    image = Image.fromarray(original)

    # Save image
    image.save(filename)
