import cv2
import sys
import numpy as np

def fixIndexValue(index,maxIndex):
    """fixes an index value to mimic the reflection off the border property, so we do not get an out-of-bounds error when the structuring element is in the corner"""
    if index < 0:
        # if we are trying to access an index less than 0, just invert the index (reflected value)
        return -index
    elif index>=maxIndex:
        # if we are trying to access a number greater than the max, return the reflected value
        return maxIndex-(index-maxIndex)-1
    else:
        # otherwise, just return the value
        return index

def imageErosion(image):
    """performs erosion on an image and returns this"""
    # note: to match cv2's behaviour, when the structuring element is in a corner (overhanging), the non-existant pixel values are the reflections of the existant pixel values.

    # define the structuring element
    structure = np.ones((5,5),np.uint8)
    # get image size using numpy
    height, width = np.shape(image)
    # make a copy of the image to save our eroded image to
    eroded_image = image.copy()
    # iterate over all pixels in the image
    # i is the current horizontal index
    for i in range(0,width):
        # j is the current vertical index
        for j in range(0,height):
            # the current minimum value of the neighbouring pixels (initalised to -1)
            currentMinNeighbour = -1
            # iterate over all neighbours of this pixel to find the minimum
            # k is the current neighbouring pixel horizontal index
            for k in range(i-2,i+3):
                # l is the current neighbouring pixel vertical index
                for l in range(j-2,j+3):
                    # fix the index values so we don't get an out-of-bounds error
                    k = fixIndexValue(k,width)
                    l = fixIndexValue(l,height)
                    # get the pixel value of this neighbouring pixel
                    thisNeighbourPixel = image[k][l]
                    # if we have not yet set the minmum pixel value, set it
                    if currentMinNeighbour==-1:
                        currentMinNeighbour = thisNeighbourPixel
                    # if the neighbouring pixel value is the new lowest, set it
                    elif thisNeighbourPixel<currentMinNeighbour:
                        currentMinNeighbour = thisNeighbourPixel
            # set this minimum neighbour value to be the new value in the new image
            eroded_image[i][j] = currentMinNeighbour
    # return the eroded image
    return eroded_image

# read the image from the filename in greyscale
greyscale_image = cv2.imread(sys.argv[1],0)
# obtain the eroded image
eroded_image = imageErosion(greyscale_image)
# save the eroded image back to disk, with the user-specified filename
cv2.imwrite(sys.argv[2],eroded_image)