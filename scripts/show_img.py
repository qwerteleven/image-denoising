import sys
import json
import matplotlib.pyplot as plt
import cv2

def main(img_index, methods_list):

    path_metadata_img = '../result_metadata/'
    img_data = get_img_ordered(path_metadata_img, methods_list)

    path_data = '../dataset'
    path_result = '../results'


    f, axarr = plt.subplots(len(img_data), 2, figsize=(25, 15))

    f.suptitle(img_data[0][img_index], fontsize=16)

    for index, method in enumerate(img_data):

        imgfile = method[img_index][2]

        axarr[index, 0].imshow(cv2.imread(imgfile)[:, :, ::-1])
        axarr[index, 0].set_title('Original')

        method_imgfile = path_result + '/' + methods_list[index].split('.')[0] + imgfile[len(path_data):]

        axarr[index, 1].imshow(cv2.imread(method_imgfile)[:, :, ::-1])
        axarr[index, 1].set_title(methods_list[index] + ' PSNR: ' + str(method[img_index][0]) + ' SSIM: ' + str(method[img_index][1]))


    # plt.show()

    plt.savefig('show_img_output.png')


    print('done')



def get_img_ordered(path, methods):

    results = []
    for method_file in methods:
        with open(path + method_file) as f:
            data = json.load(f)

            data = data['results']

            output = []

            for img in data:
                output.append((img['PSNR'], img['SSIM'], img['image_file']))

            results.append(sorted(output,  key=lambda x: x[2]))
    return results


if __name__ == '__main__':
    plt.switch_backend('agg')

    img_index = int(sys.argv[1])

    methods = [
        'DCTdenoising.json',
        'nlmp.json'
    ]

    main(img_index, methods)