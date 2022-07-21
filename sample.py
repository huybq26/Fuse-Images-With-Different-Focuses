import os
import numpy as np
from nets.sesf_net import SESF_Fuse

# from repos.SESF-Fuse-master.nets import SESF_Fuse
# Initialize SESF_Fuse in one environment, and then run the code at the second environment


import cv2  # opencv-python
img1 = cv2.imread('../images/image1.png')
img2 = cv2.imread('../images/image2.png')
img3 = cv2.imread('../images/image3.png')

sesf = SESF_Fuse("cse")


# save image?

# Finds the contour for one image
command = "cd {} && python3 {} -i {} -o {} -prep bbd-fastrcnn -postp rtb-bnb -m basnet".format(
    '../repos/image-background-remove-tool-master', "main.py", fused_image, '../output/image1.png')

img_4ch = cv2.imread(path_to_png, cv2.IMREAD_UNCHANGED)
alpha = img_4ch[..., -1]
thr = cv2.threshold

os.system(command)

im = cv2.imread(fused_image)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # color normalization

ret, thresh = cv2.threshold(imgray, 127, 255, 0)  # set threshold

contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours


def findCenter(img):
    print(img.shape, img.dtype)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    cnts = cv2.findContours(threshed, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    M = cv2.moments(cnts[0])
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)


img1 = cv2.imread("img1.jpg")
img2 = cv2.resize(cv2.imread("img2.jpg"), None, fx=0.3, fy=0.3)

# Find centers
pt1 = findCenter(img1)
pt2 = findCenter(img2)

# Calculate the shift between centers
dx = pt1[0] - pt2[0]
dy = pt1[1] - pt2[1]


def get_box_points(img):
    contours, _ = cv2.findContours(img.astype(
        np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    rect = cv2.minAreaRect(cnt)
    box_points = cv2.boxPoints(rect)
    box_points = np.int0(box_points)
    # increase the shape by 20%
    return box_points


img_box_points = get_box_points(img1)
img_paper_box_points = get_box_points(img2)

# Affine transformation matrix
M = cv2.getAffineTransform(img_box_points[0:3].astype(
    np.float32), img_paper_box_points[0:3].astype(np.float32))

# apply M to the original binary image
img_registered = cv2.warpAffine(img1.astype(np.float32), M, dsize=(
    img2.shape[1], img2.shape[0]))

# get the difference
dif = img_registered-img2

# remove minus values
dif[dif < 1] = 0

# Center both images
h, w = img2.shape[:2]

dst = img1.copy()
dst[dy:dy+h, dx:dx+w] = img2


# fuses two images
def fuse_images(img1, img2, img3):
    imgs = []
    first = sesf.fuse(img1, img2)
    second = sesf.fuse(first, img3)
    return second


fused_image = fuse_images(img1, img2, img3)
