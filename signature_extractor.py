# cite: https://github.com/ahmetozlu/signature_extractor

import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
import sys

# Sử dụng thuật toán connected component, các connected component là
# các pixel liên tiếp kề nhau và có giá trị tương tự nhau
# Sau đó xoá các component nhỏ (có thể là ký tự) và các component lớn (ảnh)

# the parameters are used to remove small size connected pixels outliar
constant_parameter_1 = 84
constant_parameter_2 = 250
constant_parameter_3 = 100

# the parameter is used to remove big size connected pixels outliar
constant_parameter_4 = 18

if len(sys.argv) < 2:
    print("Please provide the path to the image.")
    sys.exit(1)

image_name = sys.argv[1]

path = "./inputs/img/" + image_name

# read the input image
img = cv2.imread(path, 0)

img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary

# connected component analysis by scikit-learn framework
blobs = img > img.mean()
blobs_labels = measure.label(blobs, background=1)
image_label_overlay = label2rgb(blobs_labels, image=img)

the_biggest_component = 0
total_area = 0
counter = 0
average = 0.0
for region in regionprops(blobs_labels):
    if (region.area > 10):
        total_area = total_area + region.area
        counter = counter + 1
    if (region.area >= 250):
        if (region.area > the_biggest_component):
            the_biggest_component = region.area

average = (total_area/counter)
# experimental-based ratio calculation, modify it for your cases
# a4_small_size_outliar_constant is used as a threshold value to remove connected outliar connected pixels
# are smaller than a4_small_size_outliar_constant for A4 size scanned documents
a4_small_size_outliar_constant = (
    (average/constant_parameter_1)*constant_parameter_2)+constant_parameter_3

# experimental-based ratio calculation, modify it for your cases
# a4_big_size_outliar_constant is used as a threshold value to remove outliar connected pixels
# are bigger than a4_big_size_outliar_constant for A4 size scanned documents
a4_big_size_outliar_constant = a4_small_size_outliar_constant*constant_parameter_4

# remove the connected pixels are smaller than a4_small_size_outliar_constant
pre_version = morphology.remove_small_objects(
    blobs_labels, a4_small_size_outliar_constant)
# remove the connected pixels are bigger than threshold a4_big_size_outliar_constant
# to get rid of undesired connected pixels such as table headers and etc.
component_sizes = np.bincount(pre_version.ravel())
too_small = component_sizes > (a4_big_size_outliar_constant)
too_small_mask = too_small[pre_version]
pre_version[too_small_mask] = 0

# save the the pre-version which is the image is labelled with colors
# as considering connected components
plt.imsave('pre_version.png', pre_version)

# read the pre-version
img = cv2.imread('pre_version.png', 0)

# ensure binary
img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# save the the result
cv2.imwrite("output.png", img)

# crop the signature
gray = cv2.imread("output.png", 0)

_, binary_image = cv2.threshold(
    gray, 100, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

contours, _ = cv2.findContours(
    binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) > 0:
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    padding = 10  # Adjust the padding size as needed
    x_pad = max(0, x - padding)
    y_pad = max(0, y - padding)
    x_end = min(img.shape[1], x + w + padding)
    y_end = min(img.shape[0], y + h + padding)

    signature_region = img[y_pad:y_end, x_pad:x_end]
    cv2.imwrite("cropped_image.png", signature_region)
else:
    print("No signature found in the image.")
