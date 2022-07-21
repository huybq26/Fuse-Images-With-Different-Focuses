# %cd /content/drive/MyDrive/sesf/SESF-Fuse/

# from IPython.display import display
from flask import Flask, request, jsonify, render_template, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
from nets.sesf_net import SESF_Fuse
import os
import cv2
from PIL import Image

# os.chdir('../sesf/SESF-Fuse/')

# Try example fuse
# print(os.getcwd())

# Make sure that after executing a function, the current path is always /code.


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_file = request.files["upload-file"]
        if input_file.filename != '':
            input_file.save("./file/example.xlsx")
    return render_template("index.html")


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


def remove_background(num):
    os.chdir('image-background-remove-tool')
    # display(Image.open(image_path))
    image_input = '../../images/image'+num+'.png'
    image_out = './images/removed-background-image' + num + '.png'
    if os.path.exists(image_input):
        #f = "1.jpg"
        print("Running remove background tool")
        command = "python main.py -i {} -o {} -prep bbd-fastrcnn -postp rtb-bnb -m basnet".format(
            image_input, image_out)
        os.system(command)
        # image = Image.open(image_out).convert("RGBA")
        # new = Image.new("RGB", image.size, (255, 255, 255))
        # new.paste(image, (0, 0), image)
        # display(new)
        # display(image)
    os.chdir('..')


print(os.getcwd())


def get_center(num):
    processed_image = './image-background-remove-tool/images/removed-background-image' + num + '.png'
    save_processed_image = Image.open(processed_image)
    save_processed_image.save(
        "../../static/removed-background-image" + num + ".png")
    im1 = cv2.imread(processed_image)
    imgray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)  # color normalization
    ret1, thresh1 = cv2.threshold(imgray1, 127, 255, 0)  # set threshold

    contours1, hierarchy1 = cv2.findContours(
        thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours

    M = cv2.moments(thresh1)

    cx1 = int(M['m10']/M['m00'])
    cy1 = int(M['m01']/M['m00'])
    print(cx1, " ", cy1)
    return cx1, cy1


def shift_and_fuse(ref_image, image2, x_ref, y_ref, cx1, cy1):
    M = np.float32([
        [1, 0, x_ref-cx1],
        [0, 1, 0]  # mathematically true: y_ref-cy1, practically true: 0
    ])
    shifted = cv2.warpAffine(image2, M, (image2.shape[1], image2.shape[0]))

    image2 = shifted

    imgray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)  # color normalization

    ret2, thresh2 = cv2.threshold(imgray2, 127, 255, 0)  # set threshold

    contours2, hierarchy2 = cv2.findContours(
        thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours

    result = sesf.fuse(ref_image, shifted)

    return result  # return result image


def full_process(list_of_names):
    unique_names = []
    no_of_images = list_of_names.len()
    ref_image = None
    x_ref = None
    y_ref = None
    for i in range(no_of_images):
        image_name = list_of_names[i]
        identity = image_name[0:13]
        print("particle: ", identity)
        if identity not in unique_names:
            unique_names.append(identity)

    for i in range(1, no_of_images+1):
        remove_background(i)
        cx, cy = get_center(i)
        if i == 1:
            ref_image = cv2.imread(
                './image-background-remove-tool/images/removed-background-image1.png')
            x_ref, y_ref = get_center(i)
        elif i != 1:
            image2 = cv2.imread(
                './image-background-remove-tool/images/removed-background-image' + i+'.png')
            # fuse to existing variable.
            ref_image = shift_and_fuse(ref_image, image2, x_ref, y_ref, cx, cy)

    result_image = Image.fromarray(ref_image, 'RGB')
    result_image.save("../../static/result.png")
    return ref_image


if __name__ == "__main__":
    app.run(debug=True, port=9007)
