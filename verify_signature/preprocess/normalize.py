import cv2
import numpy as np
from scipy import ndimage
from scipy.misc import imresize
from PIL import Image, ImageStat
from imageio import imread, imsave

def detect_color_image(file, thumb_size=40, MSE_cutoff=22, adjust_color_bias=True):
    pil_img = Image.open(file)
    bands = pil_img.getbands()
    if(bands == ('R','G','B') or bands== ('R','G','B','A')):
            thumb = pil_img.resize((thumb_size,thumb_size))
            SSE, bias = 0, [0,0,0]
            if adjust_color_bias:
                    bias = ImageStat.Stat(thumb).mean[:3]
                    bias = [b - sum(bias)/3 for b in bias ]
                    for pixel in thumb.getdata():
                            mu = sum(pixel)/3
                            SSE += sum((pixel[i] - mu - bias[i])*(pixel[i] - mu - bias[i]) for i in [0,1,2])
                            MSE = float(SSE)/(thumb_size*thumb_size)
                            if MSE <= MSE_cutoff:
                                    return False
                            else:
                                    return True
            elif len(bands)==1:
                    return False
            else:
                    return False

def remove_background(img):
        """ Remove noise using OTSU's method.

        :param img: The image to be processed
        :return: The normalized image
        """
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        img = img.astype(np.uint8)
        # Binarize the image using OTSU's algorithm. This is used to find the center
        # of mass of the image, and find the threshold to remove background noise
        threshold, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Remove noise - anything higher than the threshold. Note that the image is still grayscale
        img[img > threshold] = 255

        return img

def remove_background1(img):
        """ Remove noise using OTSU's method.

        :param img: The image to be processed
        :return: The normalized image
        """
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.astype(np.uint8)
        # Binarize the image using OTSU's algorithm. This is used to find the center
        # of mass of the image, and find the threshold to remove background noise
        threshold, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Remove noise - anything higher than the threshold. Note that the image is still grayscale
        img[img > threshold] = 255

        return img