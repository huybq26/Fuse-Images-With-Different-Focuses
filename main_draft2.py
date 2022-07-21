# %cd /content/drive/MyDrive/sesf/SESF-Fuse/

# from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
from nets.sesf_net import SESF_Fuse
import os
import cv2
from PIL import Image

# os.chdir('../sesf/SESF-Fuse/')

# Try example fuse
# print(os.getcwd())

# img1 = cv2.imread('../images/image1.png')
# img2 = cv2.imread('../images/image2.png')
# img3 = cv2.imread('../images/image3.png')

# img1 = '../../images/image1.png'
# img2 = '../../images/image2.png'
# img3 = '../../images/image3.png'

sesf = SESF_Fuse("cse")
# first = sesf.fuse(img1, img2)
# imgFirst = Image.fromarray(first, 'RGB')
# imgFirst.save('../images/first.png')
print('Intializing...')

# @param ["bbd-fastrcnn", "bbmd-maskrcnn", "None"] {allow-input: false}
preprocessing = "bbd-fastrcnn"
# @param ["u2net", "basnet", "u2netp", "mobile_net_model", "xception_model"] {allow-input: false}
model_name = "u2net"
# @param ["rtb-bnb", "rtb-bnb2", "No"] {allow-input: false}
postprocessing = "rtb-bnb"
# !wget - q - O ./1.jpg "$img_url" > /dev/null


# print(os.getcwd())
# image_path = '../../images/image2.png'
# image_out = '.../../images/removed-background-image2.png'


def remove_background(image_path, image_out):
    os.chdir('image-background-remove-tool')
    if os.path.exists(image_path):
        print("Running remove background tool")
        command = "python main.py -i {} -o {} -prep bbd-fastrcnn -postp rtb-bnb -m basnet".format(
            image_path, image_out)
        os.system(command)
    os.chdir('..')


first = '22'
second = '23'
third = '24'

remove_background('../../images/image' + first + '.png',
                  './images/removed-background-image' + first + '.png')
remove_background('../../images/image' + second + '.png',
                  './images/removed-background-image' + second + '.png')
remove_background('../../images/image' + third + '.png',
                  './images/removed-background-image' + third + '.png')

print(os.getcwd())
processed_image1 = './image-background-remove-tool/images/removed-background-image' + first + '.png'
processed_image2 = './image-background-remove-tool/images/removed-background-image' + second + '.png'
processed_image3 = './image-background-remove-tool/images/removed-background-image' + third + '.png'

save_processed_image1 = Image.open(processed_image1).convert('RGB')
save_processed_image2 = Image.open(processed_image2).convert('RGB')
save_processed_image3 = Image.open(processed_image3).convert('RGB')
save_processed_image1.save(
    "../../static/removed-background-image" + first + ".png")
save_processed_image2.save(
    "../../static/removed-background-image" + second + ".png")
save_processed_image3.save(
    "../../static/removed-background-image" + third + ".png")

im1 = cv2.imread(processed_image1)
im2 = cv2.imread(processed_image2)
im3 = cv2.imread(processed_image3)
width = im1.shape[1]
height = im1.shape[0]
dim = (width, height)
im2 = cv2.resize(im2, dim, interpolation=cv2.INTER_AREA)
im3 = cv2.resize(im3, dim, interpolation=cv2.INTER_AREA)

# def imageResize (image_url):
#     im = cv2.imread(image_url)


def centerFinder(im):
    # im = cv2.imread(processed_image)

    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # color normalization

    ret, thresh = cv2.threshold(imgray, 127, 255, 0)  # set threshold

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours

    M = cv2.moments(thresh)

    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print(cx, " ", cy)
    return cx, cy, im


cx1, cy1, im1 = centerFinder(im1)
cx2, cx2, im2 = centerFinder(im2)
cx3, cy3, im3 = centerFinder(im3)

print("3 dimensions are: ")
print(im1.shape)
print(im2.shape)
print(im3.shape)

# im1 = cv2.imread(processed_image1)

imgray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)  # color normalization

ret1, thresh1 = cv2.threshold(imgray1, 127, 255, 0)  # set threshold

contours1, hierarchy1 = cv2.findContours(
    thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
# contours1[20][1]

# im2 = cv2.imread(processed_image2)

imgray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)  # color normalization

ret2, thresh2 = cv2.threshold(imgray2, 127, 255, 0)  # set threshold

contours2, hierarchy2 = cv2.findContours(
    thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
# contours2[20][1]

M = cv2.moments(thresh1)

cx1 = int(M['m10']/M['m00'])
cy1 = int(M['m01']/M['m00'])
print(cx1, " ", cy1)

M = cv2.moments(thresh2)

cx2 = int(M['m10']/M['m00'])
cy2 = int(M['m01']/M['m00'])
print(cx2, " ", cy2)

print("Background removed!")


M = np.float32([
    [1, 0, (cx1-cx2)/2],
    [0, 1, (cy1-cy2)/2]  # mathematically true: cy1-cy2, practically true: 0
])
shifted = cv2.warpAffine(im2, M, (im2.shape[1], im2.shape[0]))

im2 = shifted

imgray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)  # color normalization

ret2, thresh2 = cv2.threshold(imgray2, 127, 255, 0)  # set threshold

contours2, hierarchy2 = cv2.findContours(
    thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
# contours2[20][1]
M = cv2.moments(thresh2)

cx2 = int(M['m10']/M['m00'])
cy2 = int(M['m01']/M['m00'])
print("shifted image:", cx2, " ", cy2)
# img2_shifted = Image.fromarray(shifted, 'RGB')
# img2_shifted.save('/content/drive/MyDrive/images/shift2.png')

# os.chdir('./nets')

# img1 = cv2.imread('../../images/out.png')
# img2 = cv2.imread('../../images/out2.png')

# sesf = SESF_Fuse("cse")
print("Fusing images...")
print(shifted.shape)
print(im1.shape)
width = im1.shape[1]
height = im1.shape[0]
dim = (width, height)
shifted = cv2.resize(shifted, dim, interpolation=cv2.INTER_AREA)
print(shifted.shape)
print(im1.shape)
result = sesf.fuse(im1, shifted)

cx12, cy12, result = centerFinder(result)

M = np.float32([
    [1, 0, (cx12-cx3)/2],
    # mathematically true: cy1-cy3, practically true: 0
    [0, 1, (cy12-cy3)/2]
])
shifted2 = cv2.warpAffine(im3, M, (im3.shape[1], im3.shape[0]))

im3 = shifted2

imgray3 = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)  # color normalization

ret3, thresh3 = cv2.threshold(imgray3, 127, 255, 0)  # set threshold

contours3, hierarchy3 = cv2.findContours(
    thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
# contours2[20][1]
M = cv2.moments(thresh3)

cx3 = int(M['m10']/M['m00'])
cy3 = int(M['m01']/M['m00'])
print("shifted image:", cx3, " ", cy3)

print("Fusing images...")
width = result.shape[1]
height = result.shape[0]
dim = (width, height)
shifted2 = cv2.resize(shifted2, dim, interpolation=cv2.INTER_AREA)
result2 = sesf.fuse(result, shifted2)
# w, h = 512, 512
# data = np.zeros((h, w, 3), dtype=np.uint8)
# first[0:256, 0:256] = [0, 0, 0] # red patch in upper left
# imgFirst = Image.fromarray(first, 'RGB')
# imgFirst.save('/content/drive/MyDrive/images/first.png')
# plt.imshow(first2)
print("Saving result image...")
result_image = Image.fromarray(result2, 'RGB')
result_image.save("../../static/result" + first + second + third + ".png")
print("Code compiled successfully!")

print("Image saved as result" + first + second + third + ".png")
