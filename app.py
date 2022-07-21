# basic idea:
# first, processed all images name and put them on a dictionary of the crystal name + List of file names
# Next, for each key in dictionary, apply the code
# What I need to do first:
# - Change the code to list version (there will be no image1, image2, image3, etc.)
# - Write a function to read the file name and put them in the dict
# - Finally, put all together.
# May use the code in app.py.
# File name: NC-DB4_1_1_49_b2_8x_phi1phi2_NJlcblm.png, put key as NC-DB4_1_1_49
# - Save the whole file name in the dict.

from time import sleep
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, redirect, url_for
import numpy as np
from nets.sesf_net import SESF_Fuse
import os
import cv2
from PIL import Image
import time


app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    imageList = []
    outputImageList = []
    # dir = '/home/bui_quang_huy/Documents/Huy/Internship_and_Projects/EOS/Ash App/code/static/images'
    dir = '/var/www/ashapp/static/images'
    for file in os.scandir(dir):
        os.remove(file.path)
    # will be replaced to static/output later. static/images is upload storage folder.
    # for filename in os.listdir("static/images"):
    #     img = os.path.join("static/images/", filename)
    #     if img is not None:
    #         outputImageList.append(img)

    if request.method == 'POST':
        start = time.time()

        files = request.files.getlist("upload-file")
        # print(len(files))
        print(files)
        for file in files:
            print(file.filename)
            if file.filename:
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename))
                # imageList.append("/static/images/" + file.filename)
                imageList.append(file.filename)
        if (len(imageList) > 0):
            # outputImageList = imageList
            outputImageList = mainProcess(imageList)
            print("The result images' links are:")
            for outputAddress in outputImageList:
                print(outputAddress)

        end = time.time()
        print("Total time spent is: ")
        print(end-start)
        # webAddress = "https://ashapp.wovodat.org"
        # for file in os.scandir('/var/www/ashapp/static/output'):
        #     outputImageList.append(
        #         webAddress + "/static/output/" + file.name)
        #     print(file.name)
    return render_template("index.html", outputImageList=outputImageList)


sesf = SESF_Fuse("cse")

print('Intializing...')

# @param ["bbd-fastrcnn", "bbmd-maskrcnn", "None"] {allow-input: false}
preprocessing = "bbd-fastrcnn"
# @param ["u2net", "basnet", "u2netp", "mobile_net_model", "xception_model"] {allow-input: false}
model_name = "u2net"
# @param ["rtb-bnb", "rtb-bnb2", "No"] {allow-input: false}
postprocessing = "rtb-bnb"
# !wget - q - O ./1.jpg "$img_url" > /dev/null

# imageList = []


def arrangeList(imageList):
    imageDict = {}
    txt = imageList[0]
    lastUnderScore = txt.rfind("_")
    for imageAdd in imageList:
        # static/images/NC-DB4_1_1_63_b1_8x_phi1phi2_pg.png
        key = imageAdd[:lastUnderScore]
        # print(key)
        keyList = imageDict.get(key, [])
        keyList.append(imageAdd)
        imageDict[key] = keyList
    for key in imageDict.items():
        print(key)
    print(len(imageDict), " particle(s) were detected.")
    return imageDict


def mainProcess(imageList):
    # imageList is the image address list received from the frontend
    resultImageList = []  # containing the output image address
    particleDict = arrangeList(imageList)
    for particle in particleDict:  # for each particle found
        # remove background:
        particleList = particleDict[particle]
        # this list contains the real image, not addresses
        processedImageList = remove_background(particleList)
        print(len(processedImageList))
        # resize:
        mirrorImage = processedImageList[0]
        width = mirrorImage.shape[1]
        height = mirrorImage.shape[0]
        dim = (width, height)
        # for processedImage in processedImageList:
        #     processedImage = cv2.resize(
        #         processedImage, dim, interpolation=cv2.INTER_AREA)

        for i in range(len(processedImageList)):
            processedImageList[i] = cv2.resize(
                processedImageList[i], dim, interpolation=cv2.INTER_AREA)

        cx1, cy1, im1 = centerFinder(mirrorImage)
        fusedImage = im1
        for processedImage in processedImageList:
            # find center:
            cx2, cy2, im2 = centerFinder(processedImage)
            # shifting:
            M = np.float32([
                [1, 0, (cx1-cx2)/2],
                # mathematically true: cy1-cy2, practically true: 0
                [0, 1, (cy1-cy2)/2]
            ])
            shifted = cv2.warpAffine(im2, M, (im2.shape[1], im2.shape[0]))
            im2 = shifted
            # fusing:
            fusedImage = sesf.fuse(fusedImage, shifted)
        # saving result image:
        result_image = Image.fromarray(fusedImage, 'RGB')
        print(os.getcwd())
        # particle may contains static/ (8 characters) at the beginning
        print(particle)
        # print(particle[7:])
        result_image.save("./static/output/result-" +
                          particle+".png", 'png')
        webAddress = "https://ashapp.wovodat.org"
        resultImageList.append(
            webAddress + "/static/output/result-" + particle+".png")
        # print(webAddress + "/static/output/result-" + particle[7:]+".png")
        # https://ashapp.wovodat.org/static/result789.png
    return resultImageList


def remove_background(imageList):
    processedImageList = []
    # sleep(5)
    for image in imageList:
        os.chdir('image-background-remove-tool')
        imageAddress = "../static/images/"+image  # image should contains .png also
        imageOut = "./images/removed-background-image-" + image
        print(imageAddress)
        if os.path.exists(imageAddress):
            print("Running remove background tool")
            command = "python main.py -i {} -o {} -prep bbd-fastrcnn -postp rtb-bnb -m basnet".format(
                imageAddress, imageOut)
            os.system(command)
            processedImageList.append(cv2.imread(imageOut))

        os.chdir('..')
    return processedImageList


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


if __name__ == "__main__":
    app.run(debug=True, port=9007)
