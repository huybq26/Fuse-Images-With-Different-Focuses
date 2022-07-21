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
# scp -r /static/images huybq@wovodat.org:/var/www/ashapp/static/images (use after pasting some images inside the foler)

# Running with 16 cores

from pickle import TRUE
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, redirect, url_for
import numpy as np
from nets.sesf_net import SESF_Fuse
import os
import cv2
from PIL import Image
from time import sleep
import time
from mpi4py import MPI
comm = MPI.COMM_WORLD


start = time.time()
# app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# size = comm.Get_size()
NO_OF_CORES = 16
rank = comm.Get_rank()


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
    # Straightforward, no need to optimize here
    for imageAdd in imageList:
        # static/images/NC-DB4_1_1_63_b1_8x_phi1phi2_pg.png
        key = imageAdd[14:][:lastUnderScore]
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
        # use mpi and done here. All 16 processors are ready
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
        # Now use mpi to run the fusing code
        if rank != 0 and rank % 4 != 0:
            length = len(processedImageList)
            remainder = rank % NO_OF_CORES
            remainder -= 1  # since we are not using core 0, need to accomodate for index 0
            indexToProcessList = []
            while remainder < length:
                indexToProcessList.append(remainder)
                remainder += NO_OF_CORES
            imageListToSend = []
            for index in indexToProcessList:
                processedImage = processedImageList[index]
        # for processedImage in processedImageList:
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
                # fusedImage = sesf.fuse(fusedImage, shifted)
                imageListToSend.append(cv2.imread(shifted))
            comm.send(imageListToSend, findNearestDivisibleBy4(
                rank), tag="fuse-image-smallGroup")
        elif rank % 4 == 0 and rank != 0:
            length = len(processedImageList)
            remainder = rank % NO_OF_CORES
            remainder -= 1  # since we are not using core 0, need to accomodate for index 0
            indexToProcessList = []
            while remainder < length:
                indexToProcessList.append(remainder)
                remainder += NO_OF_CORES
            imageListTotal = []
            for index in indexToProcessList:
                processedImage = processedImageList[index]
        # for processedImage in processedImageList:
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
                imageListTotal.append(cv2.imread(shifted))

            fusedImageSmall = imageListTotal[0]
            # fusedImageSmall = shifted
            # fusedImageSmall = comm.recv(
            #     source=lowerDivide4Remain1(rank), tag="fuse-image-smallGroup")
            for i in range(lowerDivide4Remain1(rank)+1, rank, 1):
                processedImageSmallList = comm.recv(
                    source=i, tag="fuse-image-smallGroup")
                imageListTotal.extend(processedImageSmallList)
                # fusedImageSmall = sesf.fuse(fusedImageSmall, processedImage)
            for i in range(len(imageListTotal)):
                if (i != 0):
                    fusedImageSmall = sesf.fuse(
                        fusedImageSmall, imageListTotal[i])
            comm.send(fusedImageSmall, 0, tag="fuse-image-bigGroup")

        else:
            # processedImageList = []
            for i in range(1, NO_OF_CORES, 1):
                if (i % 4 == 0):
                    processedImage = comm.recv(
                        source=i, tag="fuse-image-bigGroup")
                    print("Image received from processor {}".format(i))
                    fusedImage = sesf.fuse(fusedImage, processedImage)
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


def findNearestDivisibleBy4(num):
    while num <= NO_OF_CORES:
        if (num % 4 == 0):
            return num
        num += 1
    return NO_OF_CORES


def lowerDivide4Remain1(num):
    while (num >= 0):
        if num % 4 == 1:
            return num
        num -= 1
    return 1


def remove_background(imageList):
    # processedImageList = []
    # sleep(5)
    if rank != 0:
        length = len(imageList)
        remainder = rank % NO_OF_CORES
        remainder -= 1  # since we are not using core 0, need to accomodate for index 0
        indexToProcessList = []
        while remainder < length:
            indexToProcessList.append(remainder)
            remainder += NO_OF_CORES
    # for image in imageList:
        imageListToSend = []
        for index in indexToProcessList:
            image = imageList[index]
            os.chdir('image-background-remove-tool')
            imageAddress = "../"+image  # image should contains .png also
            imageOut = "./images/removed-background-image-" + image
            print(imageAddress)
            if os.path.exists(imageAddress):
                print("Running remove background tool with index {} in core {}".format(
                    index, rank))
                command = "python main.py -i {} -o {} -prep bbd-fastrcnn -postp rtb-bnb -m basnet".format(
                    imageAddress, imageOut)
                os.system(command)
                # processedImageList.append(cv2.imread(imageOut))
                imageListToSend.append(cv2.imread(imageOut))

            os.chdir('..')
        comm.send(imageListToSend, 0, tag="remove-background")
    else:
        processedImageList = []
        for i in range(1, NO_OF_CORES, 1):
            processedImageSmallList = comm.recv(
                source=i, tag="remove-background")
            print("Image received from processor {}".format(i))
            processedImageList.extend(processedImageSmallList)
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


def index():

    imageList = []
    outputImageList = []

    # dir = '/home/bui_quang_huy/Documents/Huy/Internship_and_Projects/EOS/Ash App/code/static/images'
    dir = '/var/www/ashapp/static/images'
    for filename in os.listdir("static/images"):
        img = os.path.join("static/images/", filename)
        imageList.append(img)
    if (len(imageList) > 0):
        # outputImageList = imageList
        outputImageList = mainProcess(imageList)
        print("The result images' links are:")
        for outputAddress in outputImageList:
            print(outputAddress)
    # will be replaced to static/output later. static/images is upload storage folder.
    # for filename in os.listdir("static/images"):
    #     img = os.path.join("static/images/", filename)
    #     if img is not None:
    #         outputImageList.append(img)

    # if request.method == 'POST':
    #     files = request.files.getlist("upload-file")
    #     # print(len(files))
    #     print(files)
    #     for file in files:
    #         print(file.filename)
    #         if file.filename:
    #             file.save(os.path.join(
    #                 app.config['UPLOAD_FOLDER'], file.filename))
    #             # imageList.append("/static/images/" + file.filename)
    #             imageList.append(file.filename)
    #     if (len(imageList) > 0):
    #         # outputImageList = imageList
    #         outputImageList = mainProcess(imageList)
        # webAddress = "https://ashapp.wovodat.org"
        # for file in os.scandir('/var/www/ashapp/static/output'):
        #     outputImageList.append(
        #         webAddress + "/static/output/" + file.name)
        #     print(file.name)
    return 0


index()
end = time.time()
print("Total time spent is: ")
print(end-start)
