import json
import glob
from math import log10, sqrt
import cv2
import numpy as np
from skimage.measure import compare_ssim


def get_images_files(path):

    files = glob.glob(path + '/**/*.*', recursive=True)
    return files
  
def PSNR(input, output):

    ground_true = cv2.imread(input)
    process = cv2.imread(output, 1)

    mse = np.mean((ground_true - process) ** 2)

    if(mse == 0):  # MSE is zero means no noise is present in the signal
        return 100

    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))

    return psnr

def SSIM(input, output):

    imageA = cv2.imread(input)
    imageB = cv2.imread(output)

    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, _) = compare_ssim(grayA, grayB, full=True)

    return score

def write_json(data, name_file):

    json_object = json.dumps(data, sort_keys=True, indent=4)

    with open(name_file, "w") as outfile:
        outfile.write(json_object)


def main(input_path, output_path, methods):

    images_files = get_images_files(input_path)


    for method in methods:

        results = {}
        metrics = []

        for image_file in images_files:

            output_image = output_path + '/' + method + image_file[len(input_path):]

            print("process image: ", image_file)

            metrics_image = {}

            metrics_image['image_file'] = image_file

            metrics_image['PSNR'] = str(PSNR(image_file, output_image))
            metrics_image['SSIM'] = str(SSIM(image_file, output_image))

            metrics.append(metrics_image)
        
        results['results'] = metrics

        name_file = method + ".json"

        write_json(results, "../result_metadata/" + name_file)


if __name__ == '__main__':
    input_path = "../dataset"
    output_path = "../results"

    methods = [

        "nlmp",
        "DCTdenoising"
    ]

    main(input_path, output_path, methods)
